#!/bin/bash

###############################################################################
# Genera token de palo alto al ingresar credenciales como					  #
# argumentos (no usar directamente para no grabar en el						  #
# historial de comandos!!!)													  #
###############################################################################

firewall="$1";
user="$2"
pw="$3"

token=$( wget --no-check-certificate --quiet \
  --method GET \
  --header 'Cache-Control: no-cache' \
  --header 'Postman-Token: c19f7bc7-dc04-436c-9aa7-9bdeb6867851' \
  --output-document \
  - 'https://'$firewall'/api/?type=keygen&user='$user'&password='$pw\
  | grep -Po '<key>(.*)</key>' | cut -d'>' -f 2 | cut -d'<' -f 1);

echo $token > $HOME/NorsePi/SHELL/.tok.tmp;
