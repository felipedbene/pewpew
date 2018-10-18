#!/bin/bash

########################################################################
# Lee el token generado a palo alto, manda una query a palo alto 	   #
# pidiendo los ataques del día, busca a cada segundo la respuesta del  #
# xml, convierte el xml a JSON y arregla la sintaxis                   #
########################################################################

echo "Getting xml file"
python3 $HOME/NorsePi/SHELL/PaloAltoXML.py maxlogs=5000 tiempo=15
echo "Cleaning file"
cat $HOME/NorsePi/XML/LastHour.json | python3 -m json.tool | tee $HOME/NorsePi/XML/LastHourReadable.json
echo "putting on DB"
python3 $HOME/NorsePi/SHELL/SaveToPostgres.py
echo "Clearing cache"
rm -rf $HOME/.config/chromium/Default/*Cache*
#echo "Refreshing Browser"
#bash $HOME/refreshChrome.sh
