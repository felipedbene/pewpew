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
    #level = "yellow"
    return level

def writeToES(info) :
    config = configparser.ConfigParser()    
    config.read(os.path.expanduser('~/code/NorsePi/config.ini'))
    elastic = list()
    elastic.append( config["ELASTIC"]["elkHost"] )
    indeces = config["SANS"]["esIndex"]
    
    if info == "green" :
        reason = "Everything is normal. No significant new threat known."
    elif info == "yellow" :
        reason = "We are currently tracking a significant new threat. The impact is either unknown or expected to be minor to the infrastructure. However, local impact could be significant. Users are advised to take immediate specific action to contain the impact."
    elif info == "orange" :
        reason = "A major disruption in connectivity is imminent or in progress. Examples: Code Red on its return, and SQL Slammer worm during its first half day"
    else :
        reason = "Loss of connectivity across a large part of the internet."
 
    
    
    doc = {
    'source': 'sans',
    'level': info,
    'time': datetime.datetime.now() + datetime.timedelta(hours=6),
    'reason' : reason
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
