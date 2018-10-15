#!/usr/bin/env python
# coding: utf-8

# # Metodo para pedir ultimos N minutos:

# In[ ]:


from datetime import datetime, timedelta
from dateutil import parser
from sqlalchemy import create_engine
import os
import pandas as pd
import pgcli as psycopg2
import sqlalchemy
import sys


# In[ ]:

def readDB(engine,table:str='AtaquesTec'):
    a = pd.read_sql(table,con=engine)
    return a

def stringify(tiempo):
    return tiempo.strftime('%Y-%m-%d %H:%M:%S')

def getLastTime(minutos:int):
    """Regresa tiempo hace X minutos"""
    now = datetime.now()
    lilback = timedelta(minutes = minutos)
    return now - lilback

def saveLastResults(time:int,string=''):
    """Toma los logs de los ultimos <time> minutos de la base de datos <string>"""
    if len(string) == 0:
        print('tomando valores de la base de datos del tec...')
        engine = create_engine('postgres://dashboard:U7h2cQ73JH@10.98.99.167:5432/logs')
    else:
        engine = create_engine(string)
    print(f"tomando los ultimos {time} minutos...")
    tmp = getLastDB(time,readDB(engine,'tec'))
    print("grabando en la memoria como JSON...")
    tmp.to_json(os.path.expanduser('~/NorsePi/XML/LastHour.json'),orient='index')
    print("finished!")
    return tmp


# In[ ]:


def fixDate(df:pd.DataFrame):
    """toma la fecha y regresa en el formato apropiado, como tiempo"""
    a = df['time_generated'].copy()
    a = a.map(str)
    df['time_generated'] = a.map(lambda x : parser.parse(x)).copy()
    return df


# In[ ]:


def sortDate(df:pd.DataFrame):
    """Convierte columna a tiempo, hace un sort con los valores,
    reset del indice y convierte al formato convencional
    """
    a = df['time_generated'].copy()
    df['time_generated'] = pd.to_datetime(a,infer_datetime_format=True)
    df2 = df.copy().sort_values(['time_generated'],ascending=True)
    df2 = df2.reset_index(drop=True)
    df2['time_generated'] = df2['time_generated'].map(lambda x : stringify(x))
    return df2


# In[ ]:


def getLastDB(tiempo:int,df:pd.DataFrame):
    """Arregla el tiempo y busca los ultimos logs basados en la hora actual"""
    df = fixDate(df)
    df = df.set_index('time_generated')
    df2 = df.loc[stringify(getLastTime(tiempo)):].copy()
    df2['time_generated'] = df2.index
    df2 = df2.reset_index(drop=True)
    df = sortDate(df2)
    return df


# In[ ]:


if __name__ == '__main__':
    """Poner como argumento el tiempo que se desea tomar de la base de datos"""
    if type(sys.argv[-1]) == int:
        saveLastResults(sys.argv[-1])
    elif len(sys.argv) > 1:
        try:
            tmp = int(sys.argv[-1])
            saveLastResults(tmp)
        except Exception as e:
            print('Por favor, dame el tiempo que necesitas de la base de datos. \nSaliendo...')
            print(e)
            pass
    else:
        saveLastResults(3*60)
