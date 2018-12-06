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



# In[2]:












def getJob(firewall, token, maxlogs, N=15):

    print('Getting last ' + N +'minutes job...')
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



def waitXML(firewall, token, job, maxlogs,timeout=60):

    print('Waiting for XML...')
    progress = 0
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



def writeToDB(entry):
    engine = getDBEngine()
    #read what is already there

    df = pd.DataFrame.from_dict(entry)
    df3 = df[ ["srcloc",'@logid'] ]
 
    for idx,i in enumerate(df['srcloc']):
        df3['srcloc'][idx] = i['@cc']

    df2 = df[ ['time_received','severity','threatid','device_name','src','dst','subtype','@logid']]
    df4 = pd.concat( [df2,df3],axis=1 )
    df4['time_received'] =  pd.to_datetime(df4.time_received)
    df4.to_sql(name="events",con=engine,schema="public",if_exists="append",index=False)

def removeDup() :
    try :
        engine = getDBEngine()
        # sorting 
        data = pd.read_sql("events",con=engine)
        data.sort_values("time_received", inplace = True, ascending=True)
        data.drop_duplicates(subset = ["time_received","threatid","src","dst"], keep = 'first', inplace = True)
        data.to_sql(name="events",con=engine,schema="public",if_exists="replace",index=False)
        return True
    except :
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
        threats = {}
        print("No new threats for now")

    return threats



def getSetTime(tiempo = 150):
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
        print ("Done waiting :)")
        #This is the sucess part to finally get the results
        threats = getThreats(firewall,token,job,maxlogs)
        if threats :
            # Write all to DB in one shot
            try :
                newThreats = len(threats)
                print("Got " + str(newThreats) + " candidates .")
                writeToDB(threats)
                #Remove Duplicates from Database
                removeDup()
            except Exception as e:
                print("Not writing to DB, no new data")
                print(e)
    else :
        print("Fail to get XML: Job failed !!!")


