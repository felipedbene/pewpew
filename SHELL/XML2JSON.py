import xmltodict
import pandas as pd
import os
"""
	El código toma el archivo recibido de palo alto como xml y lo 
	convierte a un archivo JSON que puede ser leído de manera más 
	sencilla por el programa de mapa de ataques o cualquier otro que
	consuma la info por JS
"""

home = os.path.expanduser('~')
with open('{}/pewpew/XML/LastHour.xml'.format(home)) as fd:
	doc = xmltodict.parse(fd.read())

reform = {(outerKey, innerKey): values for outerKey, innerDict in doc.items() for innerKey, values in innerDict.items()}
a = pd.DataFrame(reform)
reform = a['response']['result']['log']
a = pd.DataFrame(reform)
total = a['logs']['@count']
reform = a['logs']['entry']
df = pd.DataFrame(reform)
#df = df.drop_duplicates(subset=['threatid','src']).reset_index(drop=True)
df.to_json('{}/pewpewXML/LastHour.json'.format(home),orient='index')

