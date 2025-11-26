#!/bin/bash -e
if whoami | grep -qv root; then
  echo "This script must be run as root."
  exit 1
fi

if [ ! -f /etc/docker/daemon.json ]; then
    cat << EOF > /etc/docker/daemon.json
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
  jq '. + {"log-driver":"syslog","log-opts":{"syslog-address":"unixgram:///dev/log","tag":"docker/{{.Name}}"}}' /etc/docker/daemon.json \
    | sponge /etc/docker/daemon.json
fi
systemctl restart docker
