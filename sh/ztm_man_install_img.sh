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

# Remove zsys, there is a bug when creating image.
# See also: https://answers.launchpad.net/cubic/+question/695399
# ========================================================================
apt remove zsys -y

# Update and Upgrade the system
# ========================================================================
# Initial Update
apt update -y
apt upgrade -y

sources_list="/etc/apt/sources.list"
echo "deb http://archive.ubuntu.com/ubuntu bionic main universe" >> $sources_list
echo "deb http://archive.ubuntu.com/ubuntu bionic-security main universe" >> $sources_list
echo "deb http://archive.ubuntu.com/ubuntu bionic-updates main universe" >> $sources_list

# Remove linked packages which are outdated
apt autoremove -y

# Add repo for the Any Desk and nesicery software.
# ========================================================================
# Add anydes repo.
wget -qO - https://keys.anydesk.com/repos/DEB-GPG-KEY | apt-key add -
echo "deb http://deb.anydesk.com/ all main" | tee /etc/apt/sources.list.d/anydesk-stable.list
apt update -y

# Initial Any Desk
apt install anydesk -y

# Install ifconfig
apt install net-tools -y

# Install python env.
apt install python3-pip -y

# Install dmidecode.
apt install python3-dmidecode -y

# Install unclutter.
apt install unclutter -y

# Install Open SSH server.
apt install openssh-server -y

# Install git client.
apt install git -y

# Install caffein to keep the PC wakeup.
apt install caffeine -y

# Install Salt Minion.
# apt install python3-tornado
# apt install salt-common -y
# apt install salt-minion -y

# Remove all unesicery software.
# ========================================================================
apt remove --purge libreoffice* -y
apt remove --purge thunderbird* -y
apt remove --purge aisleriot* -y
apt remove --purge remmina -y
apt remove --purge gnome-sudoku -y
apt remove --purge gnome-todo -y
apt remove --purge gnome-mines -y
apt remove --purge gnome-calendar -y
apt remove --purge gnome-mahjongg -y
apt remove --purge transmission-gtk -y
apt remove --purge cheese -y
apt remove --purge shotwell -y
apt remove --purge gnome-screenshot -y
apt remove --purge usb-creator-gtk -y
apt remove --purge rhythmbox -y
apt remove --purge totem totem-plugins -y
apt remove --purge gnome-disk-utility -y
apt remove --purge gedit -y
apt remove --purge eog -y
apt remove --purge gnome-calculator -y
apt remove --purge gnome-characters -y
apt remove --purge gnome-power-manager -y
apt remove --purge evince -y
apt remove --purge gparted -y

apt autoremove -y
apt autoclean


# Install the Zontromat Software.
# ========================================================================
# Go to home dir.
cd ~

# Clone the Zontromat Repo
mkdir -p Git
cd ./Git
git clone https://github.com/bgerp/ztm
cd ./ztm

# Copy the project to opt/ folder.
cp ./ /opt/ztm -r

# Install dependacies.
python3 -m pip install -r /opt/ztm/requirements.txt

# Run the project. This will create the default setings.
python3 /opt/ztm/Zontromat/main.py

# Go to home dir.
# ========================================================================
cd ~

# Remove he old repo.
rm -rf ./Git

# Daemonize the app.
# ========================================================================
# Copy the servie file.
cp /opt/ztm/sh/zontromat.service /etc/systemd/system/

# Add Zontromat user.
adduser zontromat

# Add Zontromat user to sudo.
usermod -aG sudo zontromat

# Make auto login of the user.
nano /etc/gdm3/custom.conf

# Create autostart directory if it is not created.
# ========================================================================
mkdir -p /home/zontromat/.config/autostart/

# Set KIOSK screen session.
# ========================================================================
# Copy the KIOSK browser autorun. (KIOSK browser autorun file.)
cp /opt/ztm/sh/ztm-kiosk.desktop /home/zontromat/.config/autostart/ztm-kiosk.desktop

# Copy the unclutter autorun. (Hide cursor pointer in 10 ms affter usage the pointing device.)
cp /opt/ztm/sh/ztm-unclutter.desktop /home/zontromat/.config/autostart/ztm-unclutter.desktop

# Copy the caffeinie autorun. (Keep screen ON of the device.)
cp /opt/ztm/sh/ztm-caffeine.desktop /home/zontromat/.config/autostart/ztm-caffeine.desktop

# Stop sleep and screen saver.
# ========================================================================
# systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
