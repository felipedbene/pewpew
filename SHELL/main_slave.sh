#!/bin/bash

########################################################################
# Lee el token generado a palo alto, manda una query a palo alto 	   #
# pidiendo los ataques del día, busca a cada segundo la respuesta del  #
# xml, convierte el xml a JSON y arregla la sintaxis                   #
########################################################################

echo "Getting xml file"
python3 $HOME/NorsePi/SHELL/GetFromDB.py tiempo=1440
echo "Parsing values for dashboard"
python3 $HOME/NorsePi/SHELL/GetDatamapStatus.py
echo "Cleaning file"
teste=$(cat $HOME/NorsePi/XML/LastHour.json);
if [[ $teste =~ "\{\}" ]]; then #if is empty
    date | tee -a ~/log.txt 
else # if there's something on json
    cat $HOME/NorsePi/XML/LastHour.json | python3 -m json.tool | tee $HOME/NorsePi/XML/LastHourReadable.json
fi
echo "Clearing cache"
rm -rf $HOME/.config/chromium/Default/*Cache*
echo "Refreshing Browser"
bash $HOME/refreshChrome.sh
