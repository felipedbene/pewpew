#!/usr/bin/env python3
# coding: utf-8

# In[48]:


import requests
import os
import getpass


# In[50]:


if __name__ == '__main__':
    """
    Programa utilizado para generar Tokens de palo alto.
    Generado por Postman
    """
    ip = input('IP de palo alto (e.g. 8.8.8.8):')
    
    # Reemplazando IP en los documentos necesarios
    # result = ""
    # with open(os.path.expanduser('~/code/NorsePi/Python/PaloAltoXML.py')) as f:
    #     for line in f:
    #         if 'firewall=' in line:
    #             aaa = line.split("'")
    #             aaa[1] = ip
    #             line = "'".join(aaa)
    #         result += line + '\n'
    # f = open(os.path.expanduser('~/code/NorsePi/SHELL/PaloAltoXML.py'),'w')
    # f.write(result)
    # f.close()

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
        Token = xml.split('key')[1].split('>')[1].split('<')[0]
        with open(os.path.expanduser('~/code/NorsePi/Python/.tok.tmp'),'w') as file:
            file.write(Token)
    else:
        print('key not found. Check if username and password are correct and try again')
        print('response:\n{}'.format(xml))
    

