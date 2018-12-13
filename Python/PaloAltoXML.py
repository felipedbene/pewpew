#!/usr/bin/env python3

# coding: utf-8



import configparser
import os
import random
import sys
import time
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import pgcli as psycopg2
import requests
import sqlalchemy
import urllib3
import xmltodict
from dateutil import parser
from sqlalchemy import create_engine
import json


def getJob(firewall, token, maxlogs, N=15):

    print('Getting last ' + N +' minutes job...')
    last_hour_date_time = datetime.now() - timedelta(minutes = int(N))
    last_hour_date_time = last_hour_date_time.strftime('%Y/%m/%d %H:%M:%S')
    query="(receive_time geq '{}' and !( addr.src in 10.0.0.0/8 ) )".format(last_hour_date_time)
    print("Doing the query : '" + query + "'")
    url = "https://{}/api/".format(firewall)

    querystring = {"type":"log",
                   "log-type":"threat",
                   "query":"{}".format(query),
                   "nlogs":"{}".format(maxlogs),
                   "key":"{}".format(token)}
    headers = {
        'Cache-Control': "no-cache",
        'Postman-Token': "6d9f5953-46da-4ec6-a965-e539279c2d66"
        }

    try :    
        response = requests.request("GET", url, headers=headers, params=querystring,verify=False)
        #print(response.url)
    except :
        print("I couldn't schedule the first job, quitting !")
        return False


    xml = response.text
    jsonDict = xmltodict.parse(xml)
    if jsonDict["response"]["@status"] == "success" :
        job = jsonDict["response"]["result"]["job"]
    else :
        return False
    print('Finished.')
    print('#job:{}'.format(job))
    return job



def waitXML(firewall, token, job, maxlogs,timeout=180):

    print('Waiting for XML...')
    url = "https://{}/api/".format(firewall)
    querystring = {"type":"log",
                   "action":"get",
                   "job-id":"{}".format(job),
                   "nlogs":"{}".format(maxlogs),
                   "key":"{}".format(token)}

    headers = {
        'Cache-Control': "no-cache",
        'Postman-Token': "073a8ee1-8d6f-4e46-b051-f14eaca30de2"
        }

    jobstatus = ''
    a = datetime.now() + timedelta(seconds = timeout)
    
    # Wait for the FIN and/or Timeout
    while jobstatus != 'FIN' and datetime.now() < a:
        try :
            response = requests.request("GET", url, headers=headers, params=querystring,verify=False)
            xml = response.text
            jsonDict = xmltodict.parse(xml)
            resultstatus = jsonDict["response"]["@status"]
            #print(response.url)
            if resultstatus == "success" :
                jobstatus = jsonDict["response"]["result"]["job"]["status"]
                print( "Status:" + str(jobstatus) )

            else :
                jobstatus = "fail"
                return False
            time.sleep(1)
            if datetime.now() > a:
                print('Timeout Error!')
                return False
        except :
            print("Couldn't get job status")
            return False

    print('.{}'.format(jobstatus))
    return True




def getDBEngine() :

    # Getting requirements
    config = configparser.ConfigParser()    # Getting requirements

    # Reading config file
    config.read(os.path.expanduser('~/code/NorsePi/config.ini'))

    #Setting Parameters based on the config files
    dbName = config["DB"]['dbName']
    dbUser= config["DB"]['dbUser']
    dbPass= config["DB"]['dbPass']
    dbHost= config["DB"]['dbHost']
    dbPort= config["DB"]['dbPort']
    engine = create_engine('postgres://' + dbUser + ':' + dbPass + "@" + dbHost+ ":"+ dbPort +"/"+ dbName)

    return engine

def normalizeQr(df) :
    qr = df[ ['time_received','severity','threatid','device_name','src','dst','subtype','@logid','srcloc']]

    for idx,i in enumerate(qr['srcloc']):
        qr['srcloc'][idx] = i['@cc']
    
    qr['time_received'] = pd.to_datetime(df.time_received)

    return qr

def writeToDB2(entry) :
    engine = getDBEngine()
    qr = pd.DataFrame.from_dict(entry)
    dfb = pd.read_sql("events",con=engine)

    print("Writing to DB")
    if not qr.empty :
        qrdf = normalizeQr(qr)
        dfbN = dfb.drop(['level_0','index'],axis=1)
        print("Query not empty, proceed")
        print( "Qr shape : " +  str(qrdf.shape)  )
        print( "Dfb shape : " +  str(dfbN.shape)  )
        qrdf.sort_index(inplace=True).sort_index(axis=1)
        dfbN.sort_index(inplace=True).sort_index(axis=1)
        print( list(qrdf.columns.values)  )
        print( list(dfbN.columns.values)  )
        print(dfbN)
        print(qrdf)
        print(qrdf == dfbN)
        delta = qrdf[ dfbN != qrdf ].dropna(how="all")
        dfbN.append(delta)
        return True
    else :
        print("Empty query, not proceeding")
        return False


def getThreats(firewall, token, job, maxlogs):

    print('Getting XML...')
    threats = {}
    url = "https://{}/api/".format(firewall)
    querystring = {"type":"log",
                   "action":"get",
                   "job-id":"{}".format(job),
                   "nlogs":"{}".format(maxlogs),
                   "key":"{}".format(token)}
    headers = {
        'Cache-Control': "no-cache",
        'Postman-Token': "ccde3eea-27cc-4594-802a-6d4a721d6895"
        }

    try :
        response = requests.request("GET", url, headers=headers, params=querystring,verify=False)
        
    except :
        print("Error trying to get the resulting xml")
        return False
 
    
    xml = response.text
    jsonDict = xmltodict.parse(xml)
    total = int(jsonDict["response"]["result"]["log"]["logs"]["@count"])
    
    if total > 0 :
        threats = jsonDict["response"]["result"]["log"]["logs"]["entry"]                             

    else :
        print("No threats returned from query")
        threats = 0
    print("Returning {} threats...".format(str(total) )) 
    return threats



def getSetTime(tiempo = 15):
    return str(tiempo)



def getToken(tokenFile):
    with open(tokenFile,'r') as file:
        token = file.read()
    return token



if __name__ == '__main__':

    # Getting requirements
    config = configparser.ConfigParser()
    urllib3.disable_warnings()

    # Reading config file
    config.read(os.path.expanduser('~/code/NorsePi/config.ini'))

    #Setting Parameters based on the config files
    firewall = config["DEFAULT"]['Panorama']
    maxlogs=config["LOGS"]['maxlogs']
    tokenFile=os.path.expanduser(config["DEFAULT"]["tokenFile"])

    #Calculate remaing Parameters
    try :
        tiempo = getSetTime(sys.argv[1])

    except :
        tiempo = getSetTime(15)

    token = getToken(tokenFile)
    # Start do stuff
    # Get JobID
    job = getJob(firewall,token,maxlogs,N=tiempo)

    #Send the job and wait it to get done
    if job and waitXML(firewall,token,job,maxlogs) :
        print ("Done waiting")
        #This is the sucess part to finally get the results
        threats = getThreats(firewall,token,job,maxlogs)
        if threats :
            # Write all to DB in one shot
            try :
                print("Got candidates, will de-dup and write")
                writeToDB2(threats)
            except Exception as e:
                print("Exception writing to db : " + str(e))
    else :
        print("Nothing returned from panorama!!!")