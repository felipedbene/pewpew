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

#Argumentos: IP User (Pw)

if [ -z "$3"]
  then
    echo -n Password:
    read -s pw
  else
    pw=$3
fi

sudo apt update
sudo apt install chromium-browser git curl xdotool xscreensaver -y

cd $HOME/

#wget https://raw.githubusercontent.com/MicroplusOfficial/raspberrypi-remove-apps/master/remove-apps.sh
#/usr/bin/yes | remove-apps.sh

#Instalación administrador paquetes python
echo "Instalación administrador paquetes python"
/usr/bin/yes | sudo apt install python3-pip python3-pandas python3-xmltodict

#Descarga de programa de mapa de ataques
echo "Descarga de programa de mapa de ataques"
git clone http://github.com/MicroplusOfficial/NorsePi

cd NorsePi/SHELL

#Generación de token
echo "Generación de token"
bash token.sh $1 $2 $pw

#Reemplazando IP en los documentos necesarios
echo "Reemplazando IP en los documentos necesarios"
sed -i "0,/firewall/{s/'.*'/'$1'/g}" main.sh

# Creación del script que mueve mouse e inicia chromium en fullscreen
cd $HOME
cat >> start.sh << EOF
#!/bin/bash
###############################################################################
# El siguiente programa hace con que se ejecute la descarga de logs a cada 10 #
# minutos, inicia el servidor local y mueve el ratón a la parte inferior      #
# izquierda de la pantalla. Debe ser la primera cosa al iniciar después de    #
# prender.                                                                    #
###############################################################################

#Downloading logs
watch -n 600 bash \$HOME/NorsePi/SHELL/main.sh & #downloads every 5 minutes

#Starting server
cd \$HOME/NorsePi
python3 -m http.server 3245 &
#Moves mouse and start browser
xdotool mousemove \$(xdpyinfo | awk '/dimensions/{print \$2}' | sed -e 's/x/ /g') && chromium-browser --kiosk --anonymous --app=http://localhost:3245
EOF

chmod +x start.sh
sudo sh -c "echo 'xscreensaver -no-splash &' > $HOME/.config/lxsession/Lubuntu/autostart"
sudo sh -c "echo 'bash $HOME/start.sh' >> $HOME/.config/lxsession/Lubuntu/autostart"


#cp $HOME/NorsePi/downloader.sh $HOME/

