#!/bin/bash

#Set timezone
timedatectl set-timezone Europe/Sofia

SERIAL_NUMBER=$(python3 /opt/Zontromat/info.py -s)

cat /dev/null > /etc/salt/minion

echo "  master: 109.199.153.86" >> /etc/salt/minion

echo "  id: sn$SERIAL_NUMBER" >> /etc/salt/minion

systemctl restart salt-minion
sh generate_settings.sh
echo "Done!"
