FROM ubuntu:24.04

RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y wget lsb-release adduser auditd && \
	apt-get clean && rm -rf /var/lib/apt/lists/*
RUN wget https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-agent/wazuh-agent_4.14.1-1_amd64.deb && \
		WAZUH_MANAGER="wazuh.manager" WAZUH_AGENT_NAME="ping-service" dpkg -i wazuh-agent_4.14.1-1_amd64.deb && \
		rm wazuh-agent_4.14.1-1_amd64.deb

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app
RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y python3 iputils-ping && \
	apt-get clean && rm -rf /var/lib/apt/lists/*

COPY app.py .
COPY templates/ templates/

RUN echo "flag{command_injection_is_bad_mkay}" > /app/flag.txt && chmod 111 /app/flag.txt

RUN sed -i '$d' /var/ossec/etc/ossec.conf && \
	echo << EOF >> /var/ossec/etc/ossec.conf
	<localfile>
		<log_format>audit</log_format>
		<location>/var/log/audit/audit.log</location>
	</localfile>
</ossec_config>
EOF

RUN useradd -m appuser
EXPOSE 5000

RUN cat << EOF > /entrypoint.sh
#!/bin/bash
set -e

echo "-w /app/flag.txt -p r -k audit-wazuh-r" >> /etc/audit/audit.rules
APP_UID="$(id -u appuser)"
echo "-a exit,always -F euid=${APP_UID} -F arch=b64 -S execve -k audit-wazuh-c" >> /etc/audit/audit.rules
echo "-a exit,always -F euid=${APP_UID} -F arch=b32 -S execve -k audit-wazuh-c" >> /etc/audit/audit.rules
auditctl -R /etc/audit/audit.rules && auditctl -l

/var/ossec/bin/wazuh-control start

# Drop user privileges and run the app
su appuser -c "uv run /app/app.py"
EOF
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
