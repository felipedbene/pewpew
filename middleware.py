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

app = Bottle()



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

@route('/sans/<type>')
def sans(type) :
    # Getting requirements
    config = configparser.ConfigParser()    # Getting requirements

    # Reading config file
    config.read(os.path.expanduser('~/code/NorsePi/config.ini'))

    #Setting Parameters based on the config files
    sansFile = config["SANS"]['sansPath']

    with open(os.path.expanduser(sansFile),"r") as f :
            level = f.read()
    f.close()
    
    if str(type).strip().lower() == "astext" :
        return level
    elif str(type).strip().lower() == "asnumber" :
        if level == "green" :
            return str(25)
        elif level == "yellow" :
            return str(50)
        elif level == "orange" :
            return str(75)
        elif level == "red" :
            return str(100)

run(host='localhost', port=8080, debug=True)