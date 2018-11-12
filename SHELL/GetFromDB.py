#!/usr/bin/env python
# coding: utf-8

# In[1]:


from datetime import datetime, timedelta
from dateutil import parser
from sqlalchemy import create_engine
import os
import pandas as pd
import pgcli as psycopg2
import random
import sqlalchemy
import sys


# In[ ]:


def getLastDB(minutos=3*60,
              engine = create_engine('postgres://dashboard:U7h2cQ73JH@10.98.99.167:5432/logs'),
              table='tec'):
    

    df = pd.read_sql(table,con=engine)

    cp = df.copy()
    tiempo = (datetime.now() - timedelta(minutes=minutos))#.strftime('%Y-%m-%d %H:%M:%S')

    df.set_index('time_generated',inplace=True)

    df.index = pd.to_datetime(df.index)

    df = df[df.index > tiempo]


    if len(df) == 0:
        filename = 'PaloAltoError'
        log = f"Database returned empty at {datetime.now().ctime()}"

        a = open(os.path.expanduser(f'~/{filename}.log'),'a')
        print(log,file=a)
        print("="*len(log),file=a)
        a.close()

    else:

        df['time_generated'] = df.index.astype(str)
        df.reset_index(drop=True,inplace=True)
        df.to_json(os.path.expanduser('~/NorsePi/XML/LastHour.json'),orient='index')

    return df


# In[240]:


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
        print(f'Tiempo encontrado en los argumentos! Buscando últimos {tiempo} minutos')
        getLastDB(tiempo)
    else:
        print(f'Tiempo no encontrado en los argumentos. Imprimiendo últimos {3*60} minutos')
        getLastDB(3*60)

