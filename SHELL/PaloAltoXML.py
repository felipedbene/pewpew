#!/usr/bin/env python
# coding: utf-8

# In[1]:


import xmltodict
import os
import pandas as pd


# In[2]:


color_code = {'critical':'#ff4660', #red
              'high':'#f48154',  #orange
             'medium':'#d9ff7f', #yellow
             'low':'#42ff58', #green
             'informational':'#54ba8a'} #blue


# In[3]:


with open(os.path.expanduser('~/NorsePi/XML/LastHour.xml'),'r') as fd:
    doc = xmltodict.parse(fd.read())


# In[4]:


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
    print(idx)
    df.iloc[idx]['color_ataque'] = color_code[df.iloc[idx]['severity']]
    


# In[5]:


paises = pd.read_csv(os.path.expanduser('~/NorsePi/CSV/country_centroids_primary.csv'),sep='\t')

campi = pd.read_csv(os.path.expanduser('~/NorsePi/CSV/GPSTec _copy.csv'))


# In[6]:


# TODO Ler lista Felipe
campusDevice = pd.read_csv(os.path.expanduser('/home/gabriel/NorsePi/CSV/GPSTec.csv'))


# In[19]:


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


# In[20]:


campusDevice[campusDevice['Device'] == 'CP-MTY-1'] 


# In[21]:


df.to_json(os.path.expanduser('~/NorsePi/XML/LastHour.json'),orient='index')


# In[16]:


df[df['srcname'] == 'MTY']


# In[14]:


df[df['dstname'] == 'Hospital San Jose']


# In[9]:


df[df['severity']=='critical']


# In[10]:


df.iloc[58]

