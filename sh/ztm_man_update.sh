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

echo "Stopping Zontromat service."
# Stop the zontromat service.
sudo systemctl stop zontromat
echo "Zontromat service stoped."

# Go to home.
sudo cd ~

echo "Creating git directory."
# Creating git directory.
sudo mkdir Git
echo "Git directory created."

echo "Pulling new files."
# Go to the repo.
cd Git/

# Pull the Zontromat Repo
sudo git clone http://github.com/bgerp/ztm
echo "New files pulled."

echo "Copping new files."
# Copy the project to opt/ folder.
sudo cp . /opt/ -r
echo "New files copyd."

echo "Copping new daemon."
# Copy the servie file.
sudo cp /opt/ztm/sh/zontromat.service /etc/systemd/system/
echo "New daemon coped."

echo "Enabling new daemon."
# Enabe the daemon.
sudo systemctl enable zontromat
echo "New daemon enabled."

echo "Updateing daemons."
# Reload the daemons.
sudo systemctl daemon-reload

echo "Starting Zontromat service."
# Start the zontromat daemon.
sudo systemctl start zontromat
echo "Zontromat service started."

# Go to home.
cd ~

# Remove he old repo.
echo "Removing old repo."
sudo rm -rf ~/Git/ztm
echo "Old repo removed."
