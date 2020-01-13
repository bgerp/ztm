#!/bin/bash
echo "Doing apt update and upgrade"
apt update -y
apt upgrade -y

echo "Installing git and salt-minion"
apt install git salt-minion -y

echo "Adding unipi repositories"
wget https://repo.unipi.technology/debian/unipi.list -O /etc/apt/sources.list.d/unipi.list
wget https://repo.unipi.technology/debian/unipi_pub.gpg -O - | apt-key add -

apt update -y

apt-get install python3 neuron-kernel uuid-runtime unipi-firmware python3-pip unipi-modbus-tools -y

UNIQUE_ID="$(uuidgen)"

echo "Unique id generated: $UNIQUE_ID"

echo "  master: 176.33.1.15" >> /etc/salt/minion

echo "  id: $UNIQUE_ID" >> /etc/salt/minion

systemctl enable salt-minion

#Set timezone
timedatectl set-timezone Europe/Sofia


#Setup evok
apt-get install nginx -y
rm -f /etc/nginx/sites-enabled/default
apt-get install evok -y
systemctl enable evok
reboot


