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

# touch example.txt

# echo "Test" > example.txt

# echo $1 >> example.txt

# echo $2 >> example.txt

# echo $3 >> example.txt

# Stop the zontromat service.
sudo systemctl stop zontromat

# Go to home.
cd ~

# Remove if there is old direcotry.
sudo rm -rf Git

# Creating git directory.
sudo mkdir Git

# Go to the repo.
cd Git/

# Clone the Zontromat repo.
sudo git clone $1

# Clone the Zontromat Repo
git checkout $2 $3

# Copy the new file to opt/ folder.
sudo cp . /opt/ -r

# Copy the servie file.
sudo cp /opt/ztm/sh/zontromat.service /etc/systemd/system/

# Enabe the daemon.
sudo systemctl enable zontromat

# Reload the daemons.
sudo systemctl daemon-reload

# Start the zontromat daemon.
sudo systemctl start zontromat

# Go to home.
cd ~

# Remove he old repo.
sudo rm -rf ./Git
