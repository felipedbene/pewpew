#!/usr/bin/env python3
# coding: utf-8

import configparser
import requests
import os
# In[2]:

def getFile(sansURL,sansFile):

    url = sansURL
    level = ""

    try :    
        response = requests.request("GET", url, verify=True)
    except :
        print("I couldn't get the info, quitting !")
        return False
    level = response.text
    f = open(os.path.expanduser(sansFile),"w")
    f.writelines(level)
    f.close()
    return True

if __name__ == '__main__':

    # Getting requirements
    config = configparser.ConfigParser()
    config.read(os.path.expanduser('~/code/NorsePi/config.ini'))
    sansFile = config["SANS"]['sansPath']
    sansURL = config["SANS"]['sansURL']

    #Send the job and wait it to get done
    if getFile(sansURL,sansFile) :
        print("Done")
    
    else :
        print("Failed")