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
git clone https://gogvale:2195e5f778ca2c86f3b26cc2b5deec4ad281bc30@github.com/MicroplusOfficial/NorsePi

echo "Instalación dependenicas python"
yes | sudo pip3 install -r $HOME/NorsePi/requirements.txt

#/usr/bin/yes | sudo apt install python3-pip python3-pandas python3-xmltodict python3-requests

echo "Generación de token"
python3 $HOME/NorsePi/SHELL/Token.py

echo "Creación del script que mueve mouse e inicia chromium en fullscreen"
cp $HOME/NorsePi/start_slave.sh $HOME/

echo "Creación de daemon para descargar logs"
echo "*/10 * * * * $USER bash $HOME/NorsePi/SHELL/main_slave.sh" | sudo tee -a /etc/crontab

echo "Creación de job de arranque"
echo "@bash $HOME/NorsePi/start_slave.sh" | tee -a $HOME/.config/lxsession/Lubuntu/autostart

echo "Configuración de SSH"
sudo apt install openssh-server -y
sudo sed -ie 's/^#Port.*$/Port 1337/g' /etc/ssh/sshd_config
sudo ufw allow 1337
sudo service ssh restart

echo "Hacer configuración de screensaver manualmente"
