#!/usr/bin/env python3
# coding: utf-8

import configparser
import requests
import os
import datetime
from elasticsearch import Elasticsearch


def getFile(sansURL,sansFile):
    url = sansURL
    level = ""

    try :    
        response = requests.request("GET", url, verify=True)
    except :
        print("I couldn't get the info, quitting !")
        return False
    level = response.text
    #level = "red"
    return level

def writeToES(info) :
    config = configparser.ConfigParser()    
    config.read(os.path.expanduser('~/code/NorsePi/config.ini'))
    elastic = list()
    elastic.append( config["ELASTIC"]["elkHost"] )
    indeces = config["SANS"]["esIndex"]
    doc = {
    'source': 'sans',
    'level': info,
    'timestamp': datetime.datetime.now(),
    }
    client = Elasticsearch( elastic )
    client.index(index=indeces,doc_type="tslevel",body=doc )

if __name__ == '__main__':

    # Getting requirements
    config = configparser.ConfigParser()
    config.read(os.path.expanduser('~/code/NorsePi/config.ini'))
    sansFile = config["SANS"]['sansPath']
    sansURL = config["SANS"]['sansURL']
    level = getFile(sansURL,sansFile)
    #Send the job and wait it to get done
    if level :
        writeToES(level)
        print("Done")
    
    else :
        print("Failed")