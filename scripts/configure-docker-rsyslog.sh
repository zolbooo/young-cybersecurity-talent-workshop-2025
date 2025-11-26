#!/bin/bash

if [ -! /etc/docker/daemon.json ]; then
    sudo touch /etc/docker/daemon.json
    cat << EOF | sudo tee /etc/docker/daemon.json
{
  "log-driver": "syslog",
  "log-opts": {
    "syslog-address": "unixgram:///dev/log",
    "tag": "docker/{{.Name}}"
  }
}
EOF
else
  sudo jq '. + {"log-driver":"syslog","log-opts":{"syslog-address":"unixgram:///dev/log","tag":"docker/{{.Name}}"}}' /etc/docker/daemon.json \
    | sudo sponge /etc/docker/daemon.json
fi
sudo systemctl restart docker
