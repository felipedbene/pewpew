#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os


# In[2]:


level = {
    'critical':4,
    'high':3,
    'medium':2,
    'low':1,
    'informational':0    
}


# In[3]:


color_code = {'critical':"#d21231", #red
                  'high':"#ff6500",  #orange
                 'medium': "#e0ec00", #yellow
                 'low':"#69a892", #green
                 'informational':"#5992bf"} #blue


# In[4]:


def getTop(df,column):
    
    b = a[column]

    c = b.value_counts()

    d = c.to_frame()

    d['label'] = d.index

    d.rename(index=str,columns={column:'y'},inplace=True)

    d.reset_index(drop=True,inplace=True)
    
    return d


# In[5]:


a = pd.read_json(os.path.expanduser('~/NorsePi/XML/LastHour.json'),orient='index')


# In[6]:


total = a.count()[0]


# In[7]:


subtype = getTop(a,'subtype')


# In[8]:


countries = getTop(a,'srcname').head()


# In[9]:


category = getTop(a,'severity')

category.rename(columns={'label':'color'},inplace=True)

category['y']=category['y'].map(lambda x : round(x/category['y'].sum()*100,2))


# In[10]:


subtype.to_json(os.path.expanduser('~/NorsePi/XML/TopType.json'),orient='records')
countries.to_json(os.path.expanduser('~/NorsePi/XML/TopCountries.json'),orient='records')
category.to_json(os.path.expanduser('~/NorsePi/XML/TopCategory.json'),orient='records')

with open(os.path.expanduser('~/NorsePi/XML/TotalAttacks.txt'), "w") as text_file:
    print(f"{total}", file=text_file)


# In[ ]:




