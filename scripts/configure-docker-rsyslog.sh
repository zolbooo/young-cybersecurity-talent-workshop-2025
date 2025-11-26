#!/bin/bash

if [ ! -f /etc/docker/daemon.json ]; then
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
  # Note: sponge is part of moreutils package
  sudo jq '. + {"log-driver":"syslog","log-opts":{"syslog-address":"unixgram:///dev/log","tag":"docker/{{.Name}}"}}' /etc/docker/daemon.json \
    | sudo sponge /etc/docker/daemon.json
fi
sudo systemctl restart docker
