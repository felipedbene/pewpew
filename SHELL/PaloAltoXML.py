#!/usr/bin/env python
# coding: utf-8

# In[1]:


from datetime import datetime, timedelta
import urllib3
import numpy as np
import requests
import time
import random
import sys
import xmltodict
import os
import pandas as pd


# In[2]:


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
    df['srcname'] = ''
    df['srclat'] = ''
    df['srclong'] = ''
    df['dstname'] = ''
    df['dstlat'] = ''
    df['dstlong'] = ''
    df['src_alpha2'] = ''
    df['dst_alpha2'] = ''
    df['color_ataque'] = ''

    for idx,i in enumerate(df['dstloc']):
        df['dst_alpha2'][idx] = i['@cc']
    for idx,i in enumerate(df['srcloc']):
        df['src_alpha2'][idx] = i['@cc']
    for idx in range(len(df)):
        df.iloc[idx]['color_ataque'] = color_code[df.iloc[idx]['severity']]


    paises = pd.read_csv(os.path.expanduser('~/NorsePi/CSV/country_centroids_primary.csv'),sep='\t')

    campi = pd.read_csv(os.path.expanduser('~/NorsePi/CSV/GPSTec _copy.csv'))

    campi = pd.read_csv(os.path.expanduser('~/NorsePi/CSV/GPSTec.csv'))

    # TODO Ler lista Felipe
    campusDevice = pd.read_csv(os.path.expanduser('/home/gabriel/NorsePi/CSV/GPSTec.csv'))

    notFound = set()
    for idx in range(len(df)):
        # Source
        try:
                # Checa si el origen es un pais
            tmp = paises[paises['FIPS10'] == df.iloc[idx]['src_alpha2']] # Intenta con un campo de CSV
            if len(tmp) == 0: # Intenta con otro campo
                tmp = paises[paises['ISO3136'] == df.iloc[idx]['src_alpha2']]
            if len(tmp) != 0: # Si encontró un pais...
                df.iloc[idx]['srclat'] = tmp['LAT'].values[0]
                df.iloc[idx]['srclong'] = tmp['LONG'].values[0]
                df.iloc[idx]['srcname'] = tmp['SHORT_NAME'].values[0]
            else: # Si no encuentra, la fuente es un campus (Pondremos como MTY el default)
                tmp = campusDevice[campusDevice['Device'] == 'CP-MTY-1']
                notFound.add(idx)
                print('src MTY:',idx)
                df.iloc[idx]['srclat'] = tmp['latitud'].values[0]
                df.iloc[idx]['srclong'] = tmp['longitud'].values[0]
                df.iloc[idx]['srcname'] = tmp['Nombre'].values[0]
        except Exception as e:
            notFound.add(idx)
            print('source:',idx,e)
        # Destiny
        try:
                # Checa si el destino es un pais
            tmp = paises[paises['FIPS10'] == df.iloc[idx]['dst_alpha2']] # Intenta con un campo de CSV
            if len(tmp) == 0: # Intenta con otro campo
                tmp = paises[paises['ISO3136'] == df.iloc[idx]['dst_alpha2']]
            if len(tmp) != 0: # Si encontró un pais...
                df.iloc[idx]['dstlat'] = tmp['LAT'].values[0]
                df.iloc[idx]['dstlong'] = tmp['LONG'].values[0]
                df.iloc[idx]['dstname'] = tmp['SHORT_NAME'].values[0]
            else: # Si no encuentra, el destino es un campus (Tabla Felipe)
                tmp = campusDevice[campusDevice['Device'] == df.iloc[idx]['device_name']]
                if len(tmp) == 0: # Si no encuentra, pondremos como MTY el default
                    notFound.add(idx)
                    print('dst MTY:',idx)   
                    tmp = campusDevice[campusDevice['Device'] == 'CP-MTY-1'] 
                df.iloc[idx]['dstlat'] = tmp['latitud'].values[0]
                df.iloc[idx]['dstlong'] = tmp['longitud'].values[0]
                df.iloc[idx]['dstname'] = tmp['Nombre'].values[0]

        except Exception as e:
            notFound.add(idx)
            print('destiny:',idx,e)   

    df.to_json(os.path.expanduser('~/NorsePi/XML/LastHour.json'),orient='index')
    return df


# In[3]:


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


# In[4]:


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


# In[5]:


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


# In[6]:


def timeRandom(tiempo):
    ahora = datetime.now()
    randomTime = timedelta(seconds = random.uniform(0, tiempo*60))
    return ahora - randomTime


# In[7]:


def stringify(tiempo):
    return tiempo.strftime('%Y-%m-%d %H:%M:%S')


# In[8]:


def fixTime2(df:pd.DataFrame,tiempoMin=15):
    """
    Tiempo actual -15 mas valor aleatorio
    """
    b = df['time_generated']
    c = b.map(lambda x : timeRandom(15))
    df['time_generated'] = c
    df = df.sort_values(['time_generated'])
    df['time_generated'] = df['time_generated'].map(stringify)
    df.to_json(os.path.expanduser('~/NorsePi/XML/LastHour.json'),orient='index')
    return df


# In[9]:


if __name__ == '__main__':
    print(sys.argv)
    urllib3.disable_warnings()
    firewall='10.4.29.122'
    maxlogs=[x for x in sys.argv if 'maxlogs' in x]
    if len(maxlogs) == 0:
        maxlogs = 1000
    else:
        maxlogs = maxlogs[0]
        maxlogs = int(maxlogs.split('=')[-1])
    tiempo=[x for x in sys.argv if 'tiempo' in x]
    if len(tiempo) == 0:
        tiempo = 15
    else:
        tiempo = tiempo[0]
        tiempo = int(tiempo.split('=')[-1])
    with open(os.path.expanduser('~/NorsePi/SHELL/.tok.tmp'),'r') as file:
        token = file.read()
    job = getJob(firewall,token,maxlogs,N=tiempo)
    if waitXML(firewall,token,job,maxlogs):
        print('error!!')
        fixTime2(pd.read_json(os.path.expanduser('~/NorsePi/XML/LastHour.json'),orient='index'))
    else:
        getXML(firewall,token,job,maxlogs)
        xmlParser()


# In[10]:


df = xmlParser()

