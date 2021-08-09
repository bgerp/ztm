#!/bin/bash

# DeDaemonize the app.
# ========================================================================
# Stop the Zontromat daemon.
echo "Stop the Zontromat daemon."
sudo systemctl stop zontromat
echo "Zontromat daemon is stoped."

# Disable the daemon.
echo "Disable the Zontromat daemon."
sudo systemctl disable zontromat
echo "Zontromat daemon is disabled."

# Remove the servie file.
echo "Remove the Zontromat daemon."
sudo rm /etc/systemd/system/zontromat.service
echo "Zontromat daemon removed."

echo "Updateing daemons."
# Reload the daemons.
sudo systemctl daemon-reload

# Go to Zontromat
cd /opt

# Remove Zontromat app folder.
echo "Remove the Zontromat app."
sudo rm -rf ./ztm
echo "Zontromat app removed."

# Go to home.
cd ~

# Remove the Git folder.
sudo rm -rf ./Git

