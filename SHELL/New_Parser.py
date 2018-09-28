#!/usr/bin/env python
# coding: utf-8

# In[1]:


import xmltodict
import pandas as pd
import os
"""
	El código toma el archivo recibido de palo alto como xml y lo 
	convierte a un archivo JSON que puede ser leído de manera más 
	sencilla por el programa de mapa de ataques o cualquier otro que
	consuma la info por JS
"""


# In[2]:


home = os.path.expanduser('~')

color_code = {'critical':'red',
              'high':'orange',
             'medium':'yellow',
             'low':'green',
             'informational':'blue'}
default_country = 'MX'


# In[3]:


with open('{}/pewpew/XML/LastHour.xml'.format(home)) as fd:
	doc = xmltodict.parse(fd.read())

reform = {(outerKey, innerKey): values for outerKey, innerDict in doc.items() for innerKey, values in innerDict.items()}
a = pd.DataFrame(reform)
reform = a['response']['result']['log']
a = pd.DataFrame(reform)
total = a['logs']['@count']
reform = a['logs']['entry']
df = pd.DataFrame(reform)
#df = df.drop_duplicates(subset=['threatid','src']).reset_index(drop=True)


# In[4]:


df = df[['direction','device_name','time_generated',"src",'srcloc','dst','dstloc','subtype','threatid','severity']]
df1 = df['device_name'].map(lambda x : x.split('-')[1])


# In[5]:


countries = pd.read_csv(os.path.expanduser('~/pewpew/CSV/all_countries.csv'),sep='\t',index_col=0)
countries['country'] = countries['country'].map(lambda x: x.strip())


# In[6]:


Tec = pd.read_csv(os.path.expanduser('~/pewpew/CSV/GPSTec.csv'))


# In[7]:


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
#     if len(df['dstloc'][idx]) > 2:
#         #print('{}:{}->"MX"'.format(idx,df['dstloc'][idx]))
#         df['dstloc'][idx] = df['device_name'][idx].split('-')[1]
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
    df['srcname'][idx] = str(countries[countries['country'] == df['srcloc'][idx]]['name']).split()[1]
    
    tmp = str(Tec[Tec['Campus'] == df['dstloc'][idx]]['Nombre']).split()[1] #!!!!!!!!!!!!!!!!!
    
    if tmp != 'Name:':
        df['dstname'][idx] = tmp
    else:
        df['dstname'][idx] = str(countries[countries['country'] == df['dstloc'][idx]]['name']).split()[1]
    

    """
    TODO
    Cambia cordinadas de destino de acuerdo al nombre del dispositivo
    """
    tmp = str(Tec[Tec['Campus'] == df1.iloc[idx]]['longitud']).split()[1]
    if tmp == 'Name:':
        tmp = str(countries[countries['country'] == df['dstloc'][idx]]['longitude']).split()[1]
    df['dstlong'][idx] = tmp
    tmp = str(Tec[Tec['Campus'] == df1.iloc[idx]]['latitud']).split()[1]
    if tmp == 'Name:':
        tmp = str(countries[countries['country'] == df['dstloc'][idx]]['latitude']).split()[1]
    df['dstlat'][idx] = tmp    
    
    """
    Cambia cordinadas de fuente 
    """
    tmp = str(countries[countries['country'] == df['srcloc'][idx]]['longitude']).split()[1]
    df['srclong'][idx] = tmp
    tmp = str(countries[countries['country'] == df['srcloc'][idx]]['latitude']).split()[1]
    df['srclat'][idx] = tmp    
    


# In[8]:


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


# In[9]:


df = df[a]


# In[10]:


df


# In[12]:


df.to_json(os.path.expanduser('~/pewpew/XML/_LastHour.json'),orient='index')

