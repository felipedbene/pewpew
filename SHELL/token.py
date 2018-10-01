#!/usr/bin/env python
# coding: utf-8

# In[48]:


import requests
import os
import getpass


# In[49]:


if __name__ == '__main__':
    """
    Programa utilizado para generar tokens de palo alto.
    Generado por Postman
    """
    ip = input('IP de palo alto (e.g. 8.8.8.8):')

    url = "https://{}/api/".format(ip)

    querystring = {"type":"keygen"}
    querystring["user"] = input('Usuario:')
    querystring["password"] = getpass.getpass('Contraseña:')
    
    headers = {
        'Cache-Control': "no-cache",
        'Postman-Token': "63c1fdd6-6792-4498-b423-72ee6a5e152e"
        }
    response = requests.request("GET", url, headers=headers, params=querystring,verify=False)
    xml = response.text
    
    if 'key' in xml:
        print('Key found! Printing to hidden file...')
        token = xml.split('key')[1].split('>')[1].split('<')[0]
        with open(os.path.expanduser('~/NorsePi/SHELL/.tok.tmp'),'w') as file:
            file.write(token)
    else:
        print('key not found. Check if username and password are correct and try again')
        print('response:\n{}'.format(xml))
    

