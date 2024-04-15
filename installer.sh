#!/bin/bash

# Ensure the script is run as root
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

# Install necessary packages
apt-get update
apt-get install -y python3 python3-pip
pip3 install requests configparser

# Create the necessary directory
mkdir -p /opt/SlackNotify

# Copy files from the current directory to the target directory
cp SlackNotify.py /opt/SlackNotify/SlackNotify.py
cp config.txt /opt/SlackNotify/config.txt
cp SlackNotify.service /etc/systemd/system/SlackNotify.service

# Make the Python script executable
chmod +x /opt/SlackNotify/SlackNotify.py

# Reload systemd to recognize the new service file
systemctl daemon-reload

# Enable and start the service
systemctl enable SlackNotify.service
systemctl start SlackNotify.service

echo "Installation complete. SlackNotify is set to run on system startup."
