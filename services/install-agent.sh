#!/bin/bash

WAZUH_MANAGER="<YOUR_MANAGER_IP>"

echo "Installing Wazuh Agent for Docker Monitoring…"

curl -sO https://packages.wazuh.com/4.7/wazuh-agent.sh
sudo bash wazuh-agent.sh -a -m $WAZUH_MANAGER

echo "Applying Docker monitoring configuration..."
sudo cp ossec.conf /var/ossec/etc/ossec.conf

sudo usermod -aG docker ossec
sudo systemctl restart wazuh-agent

echo "Done! Agent installed."
