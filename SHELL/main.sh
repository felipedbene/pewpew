#!/bin/bash

########################################################################
# Lee el token generado a palo alto, manda una query a palo alto 	   #
# pidiendo los ataques del día, busca a cada segundo la respuesta del  #
# xml, convierte el xml a JSON y arregla la sintaxis                   #
########################################################################

echo "Getting xml file"
python3 $HOME/NorsePi/SHELL/PaloAltoXML.py

echo "Beautifying JSON"
cat $HOME/NorsePi/XML/LastHour.json | python -m json.tool | tee $HOME/NorsePi/XML/LastHourReadable.json
