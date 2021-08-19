#!/bin/bash

# Zontromat - Zonal Electronic Automation

# Copyright (C) [2020] [POLYGONTeam Ltd.]

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Go to home dir.
# ========================================================================
sudo cd ~

# Preset for the test BCVT envirenmont.
# ========================================================================
host="host = https://test.bcvt.eu/"
erp_id="erp_id = 0082-4140-0042-4216"

# Update and Upgrade the system
# ========================================================================
# Initial Update
sudo apt update && sudo apt upgrade -y
# Remove linked packages which are outdated
sudo apt autoremove -y

# Add repo for the Any Desk.
# ========================================================================
# Add anydes repo.
wget -qO - https://keys.anydesk.com/repos/DEB-GPG-KEY | sudo apt-key add -
echo "deb http://deb.anydesk.com/ all main" | sudo tee /etc/apt/sources.list.d/anydesk-stable.list
sudo apt update

# Initial Any Desk
sudo apt install anydesk -y

# Install tools.
# ========================================================================
# Install ifconfig
sudo apt install net-tools -y

# Install Git client.
sudo apt install git -y

# Install python env.
sudo apt install python3-pip -y

# Install dmidecode
sudo apt install python3-dmidecode -y

# Install the app.
# ========================================================================
# Clone the Zontromat Repo
sudo mkdir -p Git
cd ./Git
sudo git clone https://github.com/bgerp/ztm
cd ./ztm

# Copy the project to opt/ folder.
sudo cp ./ /opt/ztm -r

# Install dependacies.
sudo python3 -m pip install -r /opt/ztm/requirements.txt

# Run the project. This will create the default setings.
sudo python3 /opt/ztm/Zontromat/main.py

settings_file="/opt/ztm/settings.ini"
ts=$(sudo date +%s)
section="[ERP_SERVICE]"
config_time="config_time = "$ts
timeout="timeout = 5"

# Add settings for the ERP.
sudo echo $section >> $settings_file
sudo echo $host >> $settings_file
sudo echo $config_time >> $settings_file
sudo echo $erp_id >> $settings_file
sudo echo $timeout >> $settings_file

# Remove he old repo.
sudo rm -rf ~/Git/ztm

# Daemonize the app.
# ========================================================================
# Copy the servie file.
sudo cp /opt/ztm/sh/zontromat.service /etc/systemd/system/

# Enabe the daemon.
sudo systemctl enable zontromat

# Reload the daemons.
sudo systemctl daemon-reload

# Start the zontromat daemon.
sudo systemctl start zontromat

# System screen session.
# ========================================================================
# Enter autologin mode.
ssdm="/etc/sddm.conf"
section="[Autologin]"
user="User=zontromat"
session="Session=Lubuntu"

sudo echo "" > $ssdm
sudo echo $section >> $ssdm
sudo echo $user >> $ssdm
sudo echo $session >> $ssdm

# Set KIOSK screen session.
# ========================================================================
# Copy the autorun file file.
sudo cp /opt/ztm/sh/ztm-kiosk.desktop ~/.config/autostart/ztm-kiosk.desktop
