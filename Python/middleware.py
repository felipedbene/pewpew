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
    try :
        if number <= 5000 :
            engine = getDBEngine()
            ev = pd.read_sql("events",con=engine).sort_values("time_received",ascending=False).head(number)
            country = pd.read_sql("paises",engine)
            campi = pd.read_sql("campi",engine)
            color = pd.read_sql("color",engine)
            pslat = pd.merge(ev,country,how="inner",on=["srcloc"])
            sincolor = pd.merge(pslat,campi,how="inner",on=["device_name"])
            final = pd.merge(sincolor,color,how="inner",on=["severity"])
            final.drop(['level_0','index_x','@logid','srcloc','index_y','src','dst'],axis=1,inplace=True)
        else :
            return r"""{"0":{"severity":"critical","threatid":"Worm\/Win32.docdl.idgaf","device_name":"CP-SLP-1","subtype":"virus","srclat":39,"srclong":22,"name_x":"Greece","dstlat":22.127502,"dstlong":-101.038102,"name_y":"Nuevo Sur","index":2,"color":"#d9ff7f"}}"""
    except :
            return r"""{"0":{"severity":"critical","threatid":"Worm\/Win32.docdl.idgaf","device_name":"CP-SLP-1","subtype":"virus","srclat":39,"srclong":22,"name_x":"Greece","dstlat":22.127502,"dstlong":-101.038102,"name_y":"Nuevo Sur","index":2,"color":"#d9ff7f"}}"""

    
    
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

@route('/topatck/<lim>')
def topatck(lim):

    engine = getDBEngine()
    # get the events table
    ev = pd.read_sql("events",con=engine).sort_values("time_received",ascending=False)

    # filter last 24 hours
    #last24hev = ev[ev['time_received']>=(datetime.now()-timedelta(hours=24))]
    last24hev = ev[ev['time_received']>=( datetime(datetime.today().year, datetime.today().month, datetime.today().day, 0, 0, 0) )]
    #group the attacks by source location and count them
    l24gby = last24hev.groupby("srcloc").count()
    
    #read the countries table
    country = pd.read_sql("paises",engine)

    #cross names and c. codes
    merged = pd.merge(l24gby,country,how="inner",on=["srcloc"])

    #sort based on the number so we can return the info ordered
    merged.sort_values("dst",ascending=False,inplace=True)

    #rename the colunms and send to json
    temp = merged[["name","dst"]].rename(index=str, columns={"name": "pais", "dst": "#at"}).to_dict(orient="records")

    resultado = []
    lim = int(lim)
    for i in temp :
       resultado.append({"y" : i["#at"] , "label" : i["pais"] })
    if lim < len(resultado):
        return(json.dumps(resultado[0:lim]))
    else :
        resultado = { "error":"invalid number of countries"}
        return(json.dumps(resultado))

@route('/blkday/')
def blkday():

    engine = getDBEngine()

    # get the events table
    ev = pd.read_sql("events",con=engine).sort_values("time_received",ascending=False)

    # filter for events since 0:00 of the current day
    last24hev = ev[ev['time_received']>=( datetime(datetime.today().year, datetime.today().month, datetime.today().day, 0, 0, 0) )]
    #last24hev = ev[ev['time_received']>=(datetime.now()-timedelta(hours=24))]
    #group the attacks by source location and count them
    l24gby = last24hev["dst"].count()

    resultado = [ { "label" : "País", "y" : 0}]
    resultado[0]["y"] =  int(l24gby)
    return( json.dumps(resultado))

@route('/topsev/')
def topsev():

    engine = getDBEngine()
    ev = pd.read_sql("events",con=engine).sort_values("time_received",ascending=False)
    #last24hev = ev[ev['time_received']>=(datetime.now()-timedelta(hours=24))]
    last24hev = ev[ev['time_received']>=( datetime(datetime.today().year, datetime.today().month, datetime.today().day, 0, 0, 0) )]
    l24gby = last24hev.groupby("severity").count()
    temp = l24gby["dst"].to_dict()

    resultado = [{ "y" : 0, "label" : "Critical" }
    ,  {"y" : 0, "label" : "High" }
    ,  {"y" : 0, "label" : "Medium"}
    ,  {"y" : 0, "label" : "Low"}
    ,  {"y" : 0, "label" : "Informational"}
    ]

    if "critical" in temp :
        resultado[0]["y"] = temp["critical"]
    if "high" in temp :
        resultado[1]["y"] = temp["high"]
    if "medium" in temp :
        resultado[2]["y"] = temp["medium"]
    if "low" in temp :
        resultado[3]["y"] = temp["low"]
    if "informational" in temp :
        resultado[4]["y"] = temp["informational"]

    return(json.dumps(resultado))

@route('/topcat/')
def topcat():

    engine = getDBEngine()
    ev = pd.read_sql("events",con=engine).sort_values("time_received",ascending=False)
    #last24hev = ev[ev['time_received']>=(datetime.now()-timedelta(hours=24))]
    last24hev = ev[ev['time_received']>=( datetime(datetime.today().year, datetime.today().month, datetime.today().day, 0, 0, 0) )]
    l24gby = last24hev.groupby("subtype").count()
    temp = l24gby["dst"].to_dict()

    resultado = [{ "y" : 0, "label" : "Wildfire Virus" }
    ,  {"y" : 0, "label" : "Vulnerability" }
    ,  {"y" : 0, "label" : "Virus"}
    ,  {"y" : 0, "label" : "Spyware"}
    ]

    if "wildfire-virus" in temp :
        resultado[0]["y"] = temp["wildfire-virus"]
    if "vulnerability" in temp :
        resultado[1]["y"] = temp["vulnerability"]
    if "virus" in temp :
        resultado[2]["y"] = temp["virus"]
    if "spyware" in temp :
        resultado[3]["y"] = temp["spyware"]
   
    
    return(json.dumps(resultado))


if __name__ == "__main__" :
    run(host='0.0.0.0', port=8081, debug=True)
else:
    application = default_app()