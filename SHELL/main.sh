#!/bin/bash

########################################################################
# Lee el token generado a palo alto, manda una query a palo alto 	   #
# pidiendo los ataques del día, busca a cada segundo la respuesta del  #
# xml, convierte el xml a JSON y arregla la sintaxis                   #
########################################################################

maxcalls=1000;
firewall='10.2.8.121';
mkdir $HOME/pewpew/XML &>2
token=$(cat $HOME/pewpew/SHELL/.tok.tmp);

lasth=$(date -d '15 minutes ago' '+%Y/%m/%d %H:%M:%S');
query="(receive_time geq '"$lasth"')";
echo $query
query=$(echo $query | sed 's/(/%28/g ; s/)/%29/g ; s/ /%20/g');
job=$(curl -skX GET \
  'https://'$firewall'/api/?type=log&log-type=threat&query='$query'&nlogs='$maxcalls'&key='$token \
  -H 'Cache-Control: no-cache' \
  -H 'Postman-Token: 8551531d-7d00-42d9-933a-79063c6efacd' | \
  grep -Po '<line>.*</line>' | cut -d'>' -f 2 | cut -d'<' -f 1 | \
  awk '{print $6}');
echo 'job #'$job' processing...';

#Espera a que haya terminado el  trabajo
status1="Loading..."
echo $status1

while [ "$progress" != "100" ]; do
  status2=$(curl -skX GET \
    'https://'$firewall'/api/?type=log&action=get&job-id='$job'&nlogs='$maxcalls'&key='$token \
    -H 'Cache-Control: no-cache' \
    -H 'Postman-Token: e3d6a799-1580-48a5-b6aa-e1db3972226a');

  status1=$(echo $status2| grep -Po "<status>.*</status>" | grep -Po '[A-Z]+')

  progress=$(echo $status2 | grep -Po 'progress="\d+"' | grep  -Po '\d+')

  if [ "$progress" -eq "100" ]; then
    echo "Finished!"
    echo "$status1"
  else
    echo -n "$progress%...";
    sleep 1
  fi
done


# Get xml file
curl -skX GET \
  'https://'$firewall'/api/?type=log&action=get&job-id='$job'&nlogs='$maxcalls'&key='$token \
  -H 'Cache-Control: no-cache' \
  -H 'Postman-Token: e3d6a799-1580-48a5-b6aa-e1db3972226a' > $HOME/pewpew/XML/LastHour.xml;

# Convert xml into json
python3 ~/pewpew/SHELL/New_Parser.py
#rm $HOME/pewpew/XML/LastHour.xml

# Prettify Json with python
cp $HOME/pewpew/XML/_LastHour.json $HOME/pewpew/XML/LastHour
cat $HOME/pewpew/XML/LastHour | python -m json.tool > $HOME/pewpew/XML/LastHour.json
rm $HOME/pewpew/XML/LastHour
