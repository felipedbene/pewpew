#!/bin/bash
###############################################################################
# El siguiente programa hace con que se ejecute la descarga de logs a cada 10 #
# minutos, inicia el servidor local y mueve el ratón a la parte inferior      #
# izquierda de la pantalla. Debe ser la primera cosa al iniciar después de    #
# prender.                                                                    #
###############################################################################

echo "Moves mouse and start browser and wait for docker to start running"
sleep 9
xdotool mousemove $(xdpyinfo | awk '/dimensions/{print $2}' | sed -e 's/x/ /g') && chromium-browser --kiosk --anonymous --app=http://localhost:3247
