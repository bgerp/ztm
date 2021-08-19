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
sudo cd /opt

# Remove Zontromat app folder.
echo "Remove the Zontromat app."
sudo rm -rf ./ztm
echo "Zontromat app removed."

# Go to home.
sudo cd ~

# Remove the Git folder.
sudo rm -rf ./Git

sudo rm -rf ~/.config/autostart/ztm-kiosk.desktop