#!/bin/bash

sudo apt install openssh-server -y
sudo sed -ie 's/^.*Port.*$/Port 1337/g' /etc/ssh/sshd_config
sudo ufw allow 1337
sudo service ssh restart
