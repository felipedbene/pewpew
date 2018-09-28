#!/usr/bin/env python
# coding: utf-8

# In[59]:


import xmltodict
import pandas as pd
import os
"""
	El código toma el archivo recibido de palo alto como xml y lo 
	convierte a un archivo JSON que puede ser leído de manera más 
	sencilla por el programa de mapa de ataques o cualquier otro que
	consuma la info por JS
"""


# In[106]:


home = os.path.expanduser('~')

color_code = {'critical':'red',
              'high':'orange',
             'medium':'yellow',
             'low':'green',
             'informational':'blue'}
default_country = 'MX'


# In[107]:


with open('{}/NorsePi/XML/LastHour.xml'.format(home)) as fd:
	doc = xmltodict.parse(fd.read())

reform = {(outerKey, innerKey): values for outerKey, innerDict in doc.items() for innerKey, values in innerDict.items()}
a = pd.DataFrame(reform)
reform = a['response']['result']['log']
a = pd.DataFrame(reform)
total = a['logs']['@count']
reform = a['logs']['entry']
df = pd.DataFrame(reform)
#df = df.drop_duplicates(subset=['threatid','src']).reset_index(drop=True)


# In[108]:


df = df[['direction','device_name','time_generated',"src",'srcloc','dst','dstloc','subtype','threatid','severity']]
df1 = df['device_name'].map(lambda x : x.split('-')[1])


# In[109]:


countries = pd.read_csv(os.path.expanduser('~/NorsePi/CSV/all_countries.csv'),sep='\t',index_col=0)
# countries['country'] = countries['country'].map(lambda x: x.strip())


# In[110]:


Tec = pd.read_csv(os.path.expanduser('~/NorsePi/CSV/GPSTec.csv'))


# In[111]:


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
    


# In[112]:


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


# In[113]:


df = df[a]


# In[114]:


df = df.sort_values('time_generated')


# In[115]:


df.reset_index(drop=True,inplace=True)


# In[118]:


df.to_json(os.path.expanduser('~/NorsePi/XML/_LastHour.json'),orient='index')

