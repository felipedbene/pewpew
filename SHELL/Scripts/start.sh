#!/bin/bash
###############################################################################
# El siguiente programa hace con que se ejecute la descarga de logs a cada 10 #
# minutos, inicia el servidor local y mueve el ratón a la parte inferior      #
# izquierda de la pantalla. Debe ser la primera cosa al iniciar después de    #
# prender.                                                                    #
###############################################################################

#Downloading logs
bash $HOME/NorsePi/SHELL/main.sh
#watch -n 300 "bash $HOME/NorsePi/SHELL/main.sh" & #downloads every 5 minutes

#Starting server
cd $HOME/NorsePi
python3 -m http.server 3245 &
#Moves mouse and start browser
xdotool mousemove $(xdpyinfo | awk '/dimensions/{print $2}' | sed -e 's/x/ /g') && chromium-browser --kiosk --anonymous --app=http://localhost:3245
