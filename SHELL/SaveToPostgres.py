#!/usr/bin/env python
# coding: utf-8

# # Usar el siguiente programa para agregar el último log sacado de Palo Alto a la base de datos
# - Se eliminan valores duplicados
# - Se ajusta el texto para que se vea igual el tiempo
# - Entrega los valores en orden creciente

# # Imports

# In[1]:


from sqlalchemy import create_engine
import sqlalchemy
import pandas as pd
import os
from datetime import datetime, timedelta
import pgcli as psycopg2
from dateutil import parser


# # Read JSON

# In[2]:


def readJSON(path:str='~/NorsePi/XML/LastHour.json'):
    df = pd.read_json(os.path.expanduser(path),orient='index')
    return df


# # Read DB

# In[3]:


def readDB(engine,table:str='AtaquesTec'):
    a = pd.read_sql(table,con=engine)
    return a


# # Concatenate DB and JSON
# (and fix incompatibilities)
# - '-'→'/' 
# - str to datetime

# In[4]:


def concat(db:pd.DataFrame,json:pd.DataFrame):
    """
    Junta los dos dataframes en uno
    """
    df = db.append(json,ignore_index=True)
    return df


# In[5]:


def fixDate(df:pd.DataFrame):
    """toma la fecha y regresa en el formato apropiado, como tiempo"""
    a = df['time_generated'].copy()
    a = a.map(str)
    df['time_generated'] = a.map(lambda x : parser.parse(x)).copy()
#     df['time_generated'] = df['time_generated'].map(lambda x : stringify(x))
    return df
#     df['time_generated'] = pd.to_datetime(df['time_generated'],infer_datetime_format=True)
        


# In[6]:


def stringifyNW(tiempo):
    """Regresa en formato de tiempo con error"""
    return tiempo.strftime('%Y-%m-%d %H:%M:%S')


# In[7]:


def stringify(tiempo):
    """Regresa tiempo en formato de tiempo como str"""
    return str(tiempo.strftime('%d/%m/%Y %H:%M:%S'))


# # Sort by date

# In[8]:


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


# # Overwrite DB

# In[9]:


def overDB(df:pd.DataFrame,engine,table:str='AtaquesTec'):
    """Sobrescribe la información de la base de datos con el dataframe"""
    df.to_sql(name=table,con=engine,if_exists='replace',index=False)


# # Read range from DB

# In[10]:


def getLastTime(minutos:int):
    """Regresa tiempo hace X minutos"""
    now = datetime.now()
    lilback = timedelta(minutes = minutos)
    return now - lilback


# In[11]:


def getLastDB(tiempo:int,df:pd.DataFrame):
    """Arregla el tiempo y busca los ultimos logs basados en la hora actual"""
    df = fixDate(df)
    df = df.set_index('time_generated')
    df2 = df.loc[stringify(getLastTime(tiempo)):].copy()
    df2['time_generated'] = df2.index
    df2 = df2.reset_index(drop=True)
    df = sortDate(df2)
    return df


# # Eliminate Duplicates

# In[12]:


def elimDup(df:pd.DataFrame,columns:list=['src','threatid','time_generated']):
    """Elimina valores duplicados"""
    df2 = df.drop_duplicates(subset=columns)
    return df2


# # Main

# In[20]:


if __name__ == '__main__':
    engine = create_engine('postgres://dashboard:U7h2cQ73JH@localhost:5432/logs')
#     engine = create_engine('postgres://postgres:Microplus@localhost:5432/postgres', echo=False)
    json = readJSON()
    try:
        db = readDB(engine,'tec')
    except:
        db = pd.DataFrame() #En caso de que no haya nada o la tabla no exista, olvidar ese paso. 
            #En cualquier otro caso, poner tabla nueva
    df = concat(db,json)
    df = fixDate(df)
    df = elimDup(df)
    df = sortDate(df)
    df = fixDate(df)
    overDB(df,engine,'tec')

