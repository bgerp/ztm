#!/bin/bash

echo "Stopping Zontromat service."
# Stop the zontromat service.
sudo systemctl stop zontromat
echo "Zontromat service stoped."

# Go to home.
cd ~

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
