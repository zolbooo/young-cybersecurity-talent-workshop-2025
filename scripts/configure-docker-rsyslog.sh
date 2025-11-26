#!/bin/bash -e
if whoami | grep -qv root; then
  echo "This script must be run as root."
  exit 1
fi

if [ ! -d /etc/docker ]; then
  mkdir -p /etc/docker
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

if [ ! -f /etc/rsyslog.d/wazuh-docker.conf ]; then
    cat << EOF > /etc/rsyslog.d/wazuh-docker.conf
$FileCreateMode 0644
$template DockerDaemonLogFileName,"/var/log/docker/docker.log"
$template DockerContainerLogFileName,"/var/log/docker/%SYSLOGTAG:R,ERE,1,FIELD:docker/(.*)\[--end:secpath-replace%.log"
if $programname == 'dockerd' then {
  ?DockerDaemonLogFileName
  stop
}
if $programname == 'containerd' then {
  ?DockerDaemonLogFileName
  stop
}
if $programname == 'docker' then {
  if $syslogtag contains 'docker/' then {
  ?DockerContainerLogFileName
  stop
  }
}
$FileCreateMode 0600
EOF
fi
systemctl restart rsyslog
