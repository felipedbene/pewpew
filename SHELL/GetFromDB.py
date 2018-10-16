#!/usr/bin/env python
# coding: utf-8

# In[111]:


from datetime import datetime, timedelta
from dateutil import parser
from sqlalchemy import create_engine
import os
import pandas as pd
import pgcli as psycopg2
import random
import sqlalchemy
import sys


# In[222]:


def fixTime():
    tiempo = timedelta(seconds=random.Random().randrange(0,15*60))#.strftime('%Y-%m-%d %H:%M:%S')
    ahora = datetime.now()#.strftime('%Y-%m-%d %H:%M:%S')
    return (ahora-tiempo).replace(microsecond=0)


# In[195]:


def getLastDB(minutos=3*60,
              engine = create_engine('postgres://dashboard:U7h2cQ73JH@10.98.99.167:5432/logs'),
              table='tec'):
    """
    crear engine
    acceder a la base de datos
    grabar con indice como tiempo
    filtrar el indice
    poner en orden
    imprimir hora actual, primer y ultimo tiempo
    poner como string el tiempo
    grabar en archivo JSON
    regresar df
    """
    df = pd.read_sql(table,con=engine)
#     df.set_index(['time_generated'],inplace=True)
    if len(df) == 0:
        """
        'Fix' time with 15 minutes before
        """
        print('no log found, generating new one...')
        df['time_generated'] = fixTime()
    else:
        tiempo = (datetime.now() - timedelta(minutes=minutos))#.strftime('%Y-%m-%d %H:%M:%S')
        ahora = datetime.now()#.strftime('%Y-%m-%d %H:%M:%S')
        mask = (df['time_generated'] > tiempo) & (df['time_generated'] <= ahora)
        df = df[mask]
    df['time_generated'] = df['time_generated'].astype(str)
    df.reset_index(drop=True,inplace=True)
    df.to_json(os.path.expanduser('~/NorsePi/XML/LastHour.json'),orient='index')
    return df
    


# sys.argv.append('tiempo=15')

# In[197]:


if __name__ == '__main__':
    """Poner como argumento el tiempo que se desea tomar de la base de datos en minutos
    e.g.: python3 GetFromDB.py tiempo=130"""
    argum = [x for x in sys.argv if 'tiempo' in x]
    try:
        tiempo = argum[-1].split('=')[-1]
        tiempo = int(tiempo)
    except: 
        tiempo = ''
    if type(tiempo) == int:
        print(f'Tiempo encontrado! Imprimiendo últimos {tiempo} minutos')
        getLastDB(tiempo)
    else:
        print(f'Tiempo no encontrado. Imprimiendo últimos {3*60} minutos')
        getLastDB(3*60)

