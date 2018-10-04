#!/bin/bash

########################################################################
# Lee el token generado a palo alto, manda una query a palo alto 	   #
# pidiendo los ataques del día, busca a cada segundo la respuesta del  #
# xml, convierte el xml a JSON y arregla la sintaxis                   #
########################################################################

echo "Getting xml file"
python3 $HOME/NorsePi/SHELL/PaloAltoXML.py

echo "Beautifying JSON"
cp $HOME/NorsePi/XML/LastHour.json $HOME/NorsePi/XML/LastHour.tmp
cat $HOME/NorsePi/XML/LastHour.tmp | python -m json.tool > $HOME/NorsePi/XML/LastHour.json
rm $HOME/NorsePi/XML/LastHour.tmp
