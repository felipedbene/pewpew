#!/bin/bash
###############################################################################
# Lee los argumentos del comando, que deben de ser IP y usuario (con opción   #
# de poner contraseña como tercero (no recomendado). En caso de que se manden #
# dos argumentos, el script va pedir por la contraseña de palo alto antes de  #
# seguir.                                                                     #
# Los pasos que siguen son: descargar dependencias, clonar directorio del     #
# programa, generar token, modificar scripts con ip de palo alto, generar     #
# iniciador de programa, hacerlo ejecutable, generar ejecución automática de  #
# fondo de daemon de no-sleep y la ejecución de la app en fullscreen          #
###############################################################################

sudo apt update
sudo apt install chromium-browser git curl xdotool -y

#Instalación administrador paquetes python
echo "Instalación administrador paquetes python"
/usr/bin/yes | sudo apt install python3-pip python3-pandas python3-xmltodict python3-requests


#Generación de token
echo "Generación de token"
#python3 $HOME/NorsePi/SHELL/Token.py

# Creación del script que mueve mouse e inicia chromium en fullscreen
cd $HOME
cat > start.sh << EOF
#!/bin/bash
###############################################################################
# El siguiente programa hace con que se ejecute la descarga de logs a cada 10 #
# minutos, inicia el servidor local y mueve el ratón a la parte inferior      #
# izquierda de la pantalla. Debe ser la primera cosa al iniciar después de    #
# prender.                                                                    #
###############################################################################

#Downloading logs
bash \$HOME/NorsePi/SHELL/main.sh
watch -n 900 bash \$HOME/NorsePi/SHELL/main.sh & #downloads every 5 minutes

#Starting server
cd \$HOME/NorsePi
python3 -m http.server 3245 &
#Moves mouse and start browser
xdotool mousemove \$(xdpyinfo | awk '/dimensions/{print \$2}' | sed -e 's/x/ /g') && chromium-browser --kiosk --anonymous --app=http://localhost:3245
EOF

chmod +x start.sh
# echo "@xset s off" > $HOME/.config/lxsession/Lubuntu/autostart
echo "Hacer configuración de screensaver manualmente"
echo "@bash $HOME/start.sh" >> $HOME/.config/lxsession/Lubuntu/autostart
