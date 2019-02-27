from datetime import datetime
from elasticsearch import Elasticsearch
from bottle import Bottle,route, run, default_app
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



def getEvFromEs(size=100):
    # Getting requirements
    config = configparser.ConfigParser()    
    config.read(os.path.expanduser('~/code/NorsePi/config.ini'))
    #elastic = config["elastic"]
    client = Elasticsearch( [ "10.97.28.4" ] )
    response = client.search(
    index="palogs*",
    body={"size" : size,
      "sort": [
        {
          "@timestamp": {
            "order": "desc"
          }
        }
      ],
        "query" : {
            "bool" : {
                "must_not" : [{"match" : {"SourceLocation" + ".keyword": "10.0.0.0-10.255.255.255"}}]
            }
        }
    })

    resultado = list()
    line = dict()

    for hit in response['hits']['hits'] :
        line["name"] = hit["_source"]["SourceLocation"] 
        line["timereceived"]  = hit["_source"]["ReceiveTime"]
        line["device_name"] = hit["_source"]["DeviceName"] 
        line["threatid"] =  hit["_source"]["Threatid"] 
        line["subtype"] = hit["_source"]["ThreatType"] 
        line["severity"] = hit["_source"]["Severity"]
        line["src"] = hit["_source"]["SourceIP"] 
        line["dst"] = hit["_source"]["DestinationIP"]
        resultado.append(line)
        line = dict()
    #print(resultado)
    return json.dumps(resultado)



app = Bottle()
        
def getDBEngine() :

    # Getting requirements
    config = configparser.ConfigParser()    
    config.read(os.path.expanduser('~/code/NorsePi/config.ini'))

    #Setting Parameters based on the config files
    dbName = config["DB"]['dbName']
    dbUser= config["DB"]['dbUser']
    dbPass= config["DB"]['dbPass']
    dbHost= config["DB"]['dbHost']
    dbPort= config["DB"]['dbPort']

    engine = create_engine('postgres://' + dbUser + ':' + dbPass + "@" + dbHost+ ":"+ dbPort +"/"+ dbName)
    
    return engine


@route('/events/<number>')
def events(number):
    number = int(number)
    if number <= 5000 :
        engine = getDBEngine()
        ev = pd.read_json( getEvFromEs(number) )
        country = pd.read_sql("paises",engine)
        campi = pd.read_sql("campi",engine)
        color = pd.read_sql("color",engine)
        pslat = pd.merge(ev,country,how="inner",on=["name"])
        #print(pslat)
        sincolor = pd.merge(pslat,campi,how="inner",on=["device_name"])
        #print(sincolor)
        final = pd.merge(sincolor,color,how="inner",on=["severity"])
        #print(final)
        final.drop(['index_x','index_y','src','dst'],axis=1,inplace=True)
    return(final.to_json(date_format=True,orient='index'))

if __name__ == "__main__" :
    run(host='0.0.0.0', port=8081, debug=True)
else:
    application = default_app()