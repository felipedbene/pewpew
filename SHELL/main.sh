#!/bin/bash

########################################################################
# Lee el token generado a palo alto, manda una query a palo alto 	   #
# pidiendo los ataques del día, busca a cada segundo la respuesta del  #
# xml, convierte el xml a JSON y arregla la sintaxis                   #
########################################################################

# Get xml file
python3 ~/NorsePi/SHELL/PaloAltoXML.py

# Prettify Json with python
cp $HOME/NorsePi/XML/_LastHour.json $HOME/NorsePi/XML/LastHour
cat $HOME/NorsePi/XML/LastHour | python -m json.tool > $HOME/NorsePi/XML/LastHour.json
rm $HOME/NorsePi/XML/LastHour
