#!/usr/bin/env python
# coding: utf-8

# In[49]:


from datetime import datetime, timedelta
import numpy as np
import os
import pandas as pd
import requests
import time
import xmltodict


# # Captura de Job

# In[54]:


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


# # Wait XML
# 
#     Espera a que se termine de generar el log y despliega status en pantalla
# 

# In[52]:


def waitXML(firewall, token, job, maxlogs):
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
    while status != 'FIN':
        response = requests.request("GET", url, headers=headers, params=querystring,verify=False)
        xml = response.text
        status = xml.split('<status>')[1].split('</status>')[0]
        progress = int(xml.split('progress="')[1].split('"')[0])
        print('Status:{}%\t{}'.format(progress,status),end='\r')
        time.sleep(3)
    print('Status:{}%\t{}'.format(progress,status))
    print('Done!')


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


# # New_Parser.py

# In[56]:


def xmlParser():
    """
        El código toma el archivo recibido de palo alto como xml y lo 
        convierte a un archivo JSON que puede ser leído de manera más 
        sencilla por el programa de mapa de ataques o cualquier otro que
        consuma la info por JS
    """
    color_code = {'critical':'red',
                  'high':'orange',
                 'medium':'yellow',
                 'low':'green',
                 'informational':'blue'}
    default_country = 'MX'
    with open(os.path.expanduser('~/NorsePi/XML/LastHour.xml'),'r') as fd:
        doc = xmltodict.parse(fd.read())
    reform = {(outerKey, innerKey): values for outerKey, innerDict in doc.items() for innerKey, values in innerDict.items()}
    a = pd.DataFrame(reform)
    reform = a['response']['result']['log']
    a = pd.DataFrame(reform)
    total = a['logs']['@count']
    reform = a['logs']['entry']
    df = pd.DataFrame(reform)
    df = df[['direction','device_name','time_generated',"src",'srcloc','dst','dstloc','subtype','threatid','severity']]
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
            df['dstname'][idx] = countries[countries['country3'] == df1.iloc[idx]]['name'].reset_index(drop=True)[0]
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
    df
    df.to_json(os.path.expanduser('~/NorsePi/XML/_LastHour.json'),orient='index')
    atacantes = df['srcname']
    a = dict()
    for i in df.srcname.unique():
        a[i] = df[df.srcname == i].count()[0]
    a = pd.DataFrame.from_dict(a,orient='index').sort_values([0],ascending=False).head(9)
    a.reset_index(inplace=True)
    a.rename(index=str, columns={"index": "Country", 0: "Count"},inplace=True)
    def perc(i):
        i = int(i)
        return str(int(i*10000/len(df))/100)+'%'
    a['Perc']=a['Count'].map(perc)
    tmp = len(df) - a['Count'].sum()
    a = a.append({'Country':'Otros','Count':tmp,'Perc':perc(tmp)},ignore_index=True)
    a.to_json(os.path.expanduser('~/NorsePi/XML/TopAttackers.json'),orient='index')
    a = pd.DataFrame(df.dstname.value_counts().head(9)).reset_index().rename(index=str, columns={"index": "Campus", 'dstname': "Count"})
    a['Perc']=a['Count'].map(perc)
    tmp = len(df) - a['Count'].sum()
    a = a.append({'Campus':'Otros','Count':tmp,'Perc':perc(tmp)},ignore_index=True)
    a.to_json(os.path.expanduser('~/NorsePi/XML/TopAttacked.json'),orient='index')
    a = pd.DataFrame(df.threatid.value_counts().head(9)).reset_index().rename(index=str, columns={"index": "Attack", 'threatid': "Count"})
    a['Perc']=a['Count'].map(perc)
    tmp = len(df) - a['Count'].sum()
    a = a.append({'Attack':'Otros','Count':tmp,'Perc':perc(tmp)},ignore_index=True)
    a.to_json(os.path.expanduser('~/NorsePi/XML/TopAttacks.json'),orient='index')


# # Main program

# In[57]:


if __name__ == '__main__':
    
    firewall='10.4.29.121'

    maxlogs=1000

    with open(os.path.expanduser('~/NorsePi/SHELL/.tok.tmp'),'r') as file:
        token = file.read()

    job = getJob(firewall,token,maxlogs)

    waitXML(firewall,token,job,maxlogs)

    getXML(firewall,token,job,maxlogs)
    
    xmlParser()

