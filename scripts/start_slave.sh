#!/bin/bash
###############################################################################
# El siguiente programa hace con que se ejecute la descarga de logs a cada 10 #
# minutos, inicia el servidor local y mueve el ratón a la parte inferior      #
# izquierda de la pantalla. Debe ser la primera cosa al iniciar después de    #
# prender.                                                                    #
###############################################################################

echo "Sleeping 10 secs so docker can start, moves mouse and start browser"
sleep 10
xdotool mousemove $(xdpyinfo | awk '/dimensions/{print $2}' | sed -e 's/x/ /g') && chromium-browser --disable-web-security --user-data-dir=cache/ --kiosk --anonymous --app=http://localhost:3248/Pantalla_1.html
