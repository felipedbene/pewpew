#!/usr/bin/env python
# coding: utf-8

# In[6]:


from datetime import datetime, timedelta
import urllib3
import numpy as np
import os
import pandas as pd
import requests
import xmltodict
import time


# In[7]:


def getJob(firewall, token, maxlogs, N=15):
    print('Getting last {} minutes job...'.format(N))
    last_hour_date_time = datetime.now() - timedelta(minutes = N)
    last_hour_date_time = last_hour_date_time.strftime('%Y/%m/%d %H:%M:%S')
    query="(receive_time geq '{}')".format(last_hour_date_time)
    # print(query)

    url = "https://{}/api/".format(firewall)

    querystring = {"type":"log",
                   "log-type":"threat",
                   "query":"{}".format(query),
                   "nlogs":"{}".format(maxlogs),
                   "key":"{}".format(token)}

    headers = {
        'Cache-Control': "no-cache",
        'Postman-Token': "6d9f5953-46da-4ec6-a965-e539279c2d66"
        }

    response = requests.request("GET", url, headers=headers, params=querystring,verify=False)

    xml = response.text

    job = xml.split('line')[1].split()[-1].split('<')[0]
    
    print('Finished.')

    print('#job:{}'.format(job))
    
    return job


# In[8]:


def waitXML(firewall, token, job, maxlogs,timeout=120):
    print('Waiting for XML...')
    progress = 0
    import requests

    url = "https://{}/api/".format(firewall)

    querystring = {"type":"log",
                   "action":"get",
                   "job-id":"{}".format(job),
                   "nlogs":"{}".format(maxlogs),
                   "key":"{}".format(token)}

    headers = {
        'Cache-Control': "no-cache",
        'Postman-Token': "073a8ee1-8d6f-4e46-b051-f14eaca30de2"
        }

    status = ''
    a = datetime.now() + timedelta(seconds = timeout)
    while progress < 100 and status != 'FIN' and datetime.now() < a:
        response = requests.request("GET", url, headers=headers, params=querystring,verify=False)
        xml = response.text
        status = xml.split('<status>')[1].split('</status>')[0]    
        progress = int(xml.split('progress="')[1].split('"')[0])
        print('Status:{}%\t{}'.format(progress,status),end='\r')
        time.sleep(3)
        if datetime.now() > a:
            print('Timeout Error!')
            return True
    print('Status:{}%\t{}'.format(progress,status))
    print('Done!')
    return False


# In[9]:


def getXML(firewall, token, job, maxlogs):
    print('Getting XML...',end='')
    url = "https://{}/api/".format(firewall)

    querystring = {"type":"log",
                   "action":"get",
                   "job-id":"{}".format(job),
                   "nlogs":"{}".format(maxlogs),
                   "key":"{}".format(token)}

    headers = {
        'Cache-Control': "no-cache",
        'Postman-Token': "ccde3eea-27cc-4594-802a-6d4a721d6895"
        }

    response = requests.request("GET", url, headers=headers, params=querystring,verify=False)

    xml = response.text
    
    with open(os.path.expanduser('~/NorsePi/XML/LastHour.xml'),'w') as file:
        file.write(xml)
        
    print('Finished.')


# In[10]:


def xmlParser(file=''):
    """
        El código toma el archivo recibido de palo alto como xml y lo 
        convierte a un archivo JSON que puede ser leído de manera más 
        sencilla por el programa de mapa de ataques o cualquier otro que
        consuma la info por JS
    """
    color_code = {'critical':'#ff4660', #red
                  'high':'#f48154',  #orange
                 'medium':'#d9ff7f', #yellow
                 'low':'#42ff58', #green
                 'informational':'#54ba8a'} #blue
    default_country = 'MX'
    if file == '':
        with open(os.path.expanduser('~/NorsePi/XML/LastHour.xml'),'r') as fd:
            doc = xmltodict.parse(fd.read())
    else:
        with open(os.path.expanduser(file),'r') as fd:
            doc = xmltodict.parse(fd.read())
    reform = {(outerKey, innerKey): values for outerKey, innerDict in doc.items() for innerKey, values in innerDict.items()}
    a = pd.DataFrame(reform)
    reform = a['response']['result']['log']
    a = pd.DataFrame(reform)
    total = a['logs']['@count']
    reform = a['logs']['entry']
    df = pd.DataFrame(reform)
    df = df[['direction','device_name','time_generated',"src",'srcloc','dst','dstloc','subtype','threatid','severity']]
    print('Generating First JSON...')
    df.to_json('LastHour_1.json',orient='index')
    print('Finished. Moving on...')
    
    df1 = df['device_name'].map(lambda x : x.split('-')[1])
    countries = pd.read_csv(os.path.expanduser('~/NorsePi/CSV/all_countries.csv'),sep='\t',index_col=0)
    Tec = pd.read_csv(os.path.expanduser('~/NorsePi/CSV/GPSTec.csv'))
    df['srcname'] = ''
    df['srclat'] = ''
    df['srclong'] = ''
    df['dstname'] = ''
    df['dstlat'] = ''
    df['dstlong'] = ''
    a = len(df)
    for idx in range(a):
        try:
            print('{}/{}'.format(idx+1,a),end='\r')

            """
            Pone el codigo alpha-2 como identificador de source y destiny
            """
            df['dstloc'][idx] = df['device_name'][idx].split('-')[1]
            df['srcloc'][idx] = df['srcloc'][idx]['@cc']

            """
            Si viene como rango de IP, cambia por el default ('MX')

            Checar aqui las ubicaciones del TEC!!!!

            """
            if len(df['srcloc'][idx]) > 2:
                #print('{}->"MX"'.format(df['srcloc'][idx]))
                df['srcloc'][idx] = default_country ######################################3

            """
            Cambia severidad por codigo de colores
            """
            df['severity'][idx] = color_code[df['severity'][idx]]

            """
            Cambia el nombre del pais de acuerdo al codigo alpha-2
            """
            try:
                df['srcname'][idx] = countries[countries['country'] == df['srcloc'][idx]]['name'].reset_index(drop=True)[0]
            except:
                print('Pais no encontrado: alpha2={}, indice={}'.format(df['srcloc'][idx],idx))
                df['srcloc'][idx] = default_country
                df['srcname'][idx] = 'INTERNO'

            """Ideia: Botar uma flag em caso de que nao seja pais atacado! :D"""
            tmp = Tec[Tec['Campus'] == df['dstloc'][idx]]['Nombre'] #!!!!!!!!!!!!!!!!!
            if len(tmp) == 0:
                print('Campus no encontrado: {}, indice={}'.format(df['dstloc'][idx],idx))
                try:
                    df['dstname'][idx] = countries[countries['country3'] == df1.iloc[idx]]['name'].reset_index(drop=True)[0]
                except:
                    df['dstname'][idx] = default_country
            else:
                tmp = tmp.reset_index(drop=True)[0]
            df['dstname'][idx] = tmp

            """
            TODO
            Cambia cordinadas de destino de acuerdo al nombre del dispositivo
            """
            tmp = Tec[Tec['Campus'] == df1.iloc[idx]]['longitud']
            if len(tmp) == 0:
                tmp = countries[countries['country3'] == df['dstloc'][idx]]['longitude'].reset_index(drop=True)[0]
            else:
                tmp = tmp.reset_index(drop=True)[0]

            df['dstlong'][idx] = tmp
            ################# consertar os splits########################l
            tmp = Tec[Tec['Campus'] == df1.iloc[idx]]['latitud']
            if len(tmp) != 0:
                tmp = tmp.reset_index(drop=True)[0]
            else:
                tmp = countries[countries['country3'] == df['dstloc'][idx]]['latitude'].reset_index(drop=True)[0]
            df['dstlat'][idx] = tmp    

            """
            Cambia cordinadas de fuente 
            """
            tmp = str(countries[countries['country'] == df['srcloc'][idx]]['longitude']).split()[1]
            df['srclong'][idx] = tmp
            tmp = str(countries[countries['country'] == df['srcloc'][idx]]['latitude']).split()[1]
            df['srclat'][idx] = tmp    
        except Exception as e:
            pass
    a = ['device_name',
     'direction',
     'src',
     'srclat',
     'srclong',
     'srcloc',
     'srcname',
     'dst',
     'dstlat',
     'dstlong',
     'dstloc',
     'dstname',
     'severity',
     'subtype',
     'threatid',
     'time_generated']
    df = df[a]
    df = df.sort_values('time_generated',ascending=False)
    df.reset_index(drop=True,inplace=True)
    df.to_json(os.path.expanduser('~/NorsePi/XML/LastHour.json'),orient='index')
    


# In[19]:


def fixTime(df=pd.read_json(os.path.expanduser('~/NorsePi/XML/LastHour.json'),orient='index'),tiempoMin=15):
    b = df['time_generated']
    try:
        c = b.map(lambda x : datetime.strptime(b[0],'%Y/%m/%d %H:%M:%S') + timedelta(minutes = tiempoMin))
    except:
        c = b.map(lambda x : datetime.strptime(b[0],'%Y-%m-%d %H:%M:%S') + timedelta(minutes = tiempoMin))
    df['time_generated'] = c
    df['time_generated']=df['time_generated'].astype(str)
    df.to_json(os.path.expanduser('~/NorsePi/XML/LastHour.json'),orient='index')
    return df


# In[22]:


def fixTime2(df=pd.read_json(os.path.expanduser('~/NorsePi/XML/LastHour.json'),orient='index'),tiempoMin=15):
    """
    Tiempo actual -15 mas valor aleatorio
    """
    b = df['time_generated']
    c = b.map(lambda x : (datetime.now() - timedelta(seconds = round(random.uniform(0, tiempoMin*60)))).strftime('%Y-%m-%d %H:%M:%S'))
    df['time_generated'] = c
    df = df.sort_values(['time_generated'])
    df['time_generated']=df['time_generated'].astype(str)
    df.to_json(os.path.expanduser('~/NorsePi/XML/LastHour.json'),orient='index')
    return df


# In[20]:


if __name__ == '__main__':
    
    urllib3.disable_warnings()
    
    firewall='10.4.29.121'

    maxlogs=1000

    with open(os.path.expanduser('~/NorsePi/SHELL/.tok.tmp'),'r') as file:
        token = file.read()

    job = getJob(firewall,token,maxlogs)

    if waitXML(firewall,token,job,maxlogs,1):
        ### Send email on error
        print('error!!')
        fixTime2()
    else:
        getXML(firewall,token,job,maxlogs)
        xmlParser()


# In[17]:


xmlParser()


# In[ ]:




