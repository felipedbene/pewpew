from bottle import Bottle,route, run
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
    if number < 1000 :
        engine = getDBEngine()
        ev = pd.read_sql("events",con=engine).sort_values("time_received",ascending=False).head(number)
        country = pd.read_sql("paises",engine)
        campi = pd.read_sql("campi",engine)
        color = pd.read_sql("color",engine)
        pslat = pd.merge(ev,country,how="inner",on=["srcloc"])
        sincolor = pd.merge(pslat,campi,how="inner",on=["device_name"])
        final = pd.merge(sincolor,color,how="inner",on=["severity"])
        final.drop(['level_0','index_x','@logid','srcloc','index_y','time_received','src','dst'],axis=1,inplace=True)
    else :
        return 0
    print(ev)
    print(pslat)
    print(final)
    return(final.to_json(date_format=True,orient='index'))

@route('/sans/<tipo>')
def sans(tipo) :
    # Getting requirements
    config = configparser.ConfigParser()    # Getting requirements

    # Reading config file
    config.read(os.path.expanduser('~/code/NorsePi/config.ini'))

    #Setting Parameters based on the config files
    sansFile = config["SANS"]['sansPath']

    with open(os.path.expanduser(sansFile),"r") as f :
        level = f.read()
    f.close()

    level = level.split(",")
    levelDic = { "level" : level[0] , "last-updated" : level[1] }

    if str(tipo).strip().lower() == "astext" :
        return json.dumps(levelDic,sort_keys=True)

    elif str(tipo).strip().lower() == "asnumber" :
        
        if level[0] == "green" :
            levelDic = { "level" : 25 , "last-updated" : level[1] }
        elif level[0] == "yellow" :
            levelDic = { "level" : 50 , "last-updated" : level[1] }
        elif level[0] == "orange" :
            levelDic = { "level" : 75 , "last-updated" : level[1] }
        elif level[0] == "red" :
            levelDic = { "level" : 100 , "last-updated" : level[1] }

        return( json.dumps(levelDic,sort_keys=True) )


run(host='localhost', port=8080, debug=True)