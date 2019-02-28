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
    elastic = list()
    elastic.append( config["ELASTIC"]["elkHost"] )
    indeces = str(config["ELASTIC"]["index"])
    print (indeces)
    client = Elasticsearch( elastic )
    response = client.search(
    index = "palogs*",
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
        #print(hit)
        if "SourceLocation" in  hit['_source'].keys() :
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
    
    return json.dumps(resultado)



app = Bottle()
        
@route('/events/<number>')
def events(number):
    number = int(number)

    # Getting requirements
    config = configparser.ConfigParser()    
    config.read(os.path.expanduser('~/code/NorsePi/config.ini'))

    fileCampi = config["CSV"]["campi"]
    filePaises = config["CSV"]["paises"]
    fileColor = config["CSV"]["color"]

    if number <= 5000 :
        #Event Data from ES
        ev = pd.read_json( getEvFromEs(number) )

        #Event campi,country,color data
        country = pd.read_csv(filePaises,",")
        campi = pd.read_csv(fileCampi,",")
        color = pd.read_csv(fileColor,",")

        # Inner join the data
        pslat = pd.merge(ev,country,how="inner",on=["name"])
        sincolor = pd.merge(pslat,campi,how="inner",on=["device_name"])
        final = pd.merge(sincolor,color,how="inner",on=["severity"])
        final.drop(['index_x','index_y','src','dst'],axis=1,inplace=True)
    return(final.to_json(date_format=True,orient='index'))

if __name__ == "__main__" :
    run(host='0.0.0.0', port=8081, debug=True)
else:
    application = default_app()