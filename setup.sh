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

echo "Creación de actualizador"
cat > att <<EOF
sudo apt update
sudo apt dist-upgrade -y
sudo apt autoclean
sudo apt autoremove -y
EOF

echo "Actualización inicial"
chmod +x att
sudo mv att /bin/
att

echo "Instalación de dependencias"
sudo apt install chromium-browser git curl xdotool python3-pip -y

cd $HOME
echo "Downloading NorsePi"
git clone https://gogvale:e64a7d2d02b10bd8d07d047a64f902b54518224f@github.com/MicroplusOfficial/NorsePi

echo "Instalación dependenicas python"
yes | sudo pip3 install -r $HOME/NorsePi/requirements.txt

#/usr/bin/yes | sudo apt install python3-pip python3-pandas python3-xmltodict python3-requests

echo "Generación de token"
python3 $HOME/NorsePi/SHELL/Token.py

echo "Creación del script que mueve mouse e inicia chromium en fullscreen"
cp $HOME/NorsePi/start.sh $HOME/

echo "Creación de daemon para descargar logs"
echo "*/15 * * * * $USER bash $HOME/NorsePi/SHELL/main.sh" | sudo tee -a /etc/crontab

echo "Creación de job de arranque"
echo "@bash $HOME/NorsePi/start.sh" | tee -a $HOME/.config/lxsession/Lubuntu/autostart


echo "Hacer configuración de screensaver manualmente"


