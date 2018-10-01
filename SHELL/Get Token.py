#!/usr/bin/env python
# coding: utf-8

# In[14]:


import requests
import os
from datetime import datetime, timedelta


# In[23]:


firewall='10.4.29.121'


# In[12]:


maxcalls=1000


# In[17]:


with open(os.path.expanduser('~/NorsePi/SHELL/.tok.tmp'),'r') as file:
    token = file.read()


# In[11]:


last_hour_date_time = datetime.now() - timedelta(minutes = 15)
last_hour_date_time = last_hour_date_time.strftime('%Y/%m/%d %H:%M:%S')
query="(receive_time geq '{}')".format(last_hour_date_time)
# print(query)


# In[24]:


url = "https://{}/api/".format(firewall)


# In[18]:


querystring = {"type":"log",
               "log-type":"threat",
               "query":"{}".format(query),
               "nlogs":"{}".format(maxcalls),
               "key":"{}".format(token)}


# In[20]:


headers = {
    'Cache-Control': "no-cache",
    'Postman-Token': "6d9f5953-46da-4ec6-a965-e539279c2d66"
    }


# In[ ]:


response = requests.request("GET", url, headers=headers, params=querystring,verify=False)


# In[ ]:


xml = response.text


# In[ ]:


print('response:\n{}'.format(xml))


# In[ ]:


job = xml.split('line')[1].split('>')[1].split('<')[0]


# In[ ]:


print('job:'.format(job))

