FROM ubuntu:24.04

RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y wget lsb-release adduser && \
	apt-get clean && rm -rf /var/lib/apt/lists/*
RUN wget https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-agent/wazuh-agent_4.14.1-1_amd64.deb && \
		WAZUH_MANAGER="wazuh.manager" WAZUH_AGENT_NAME="ping-service" dpkg -i wazuh-agent_4.14.1-1_amd64.deb && \
		rm wazuh-agent_4.14.1-1_amd64.deb

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app
RUN uv python install && \
	apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y iputils-ping && \
	apt-get clean && rm -rf /var/lib/apt/lists/*

COPY app.py .
COPY templates/ templates/

RUN echo "flag{command_injection_is_bad_mkay}" > /app/flag.txt

RUN useradd -m appuser
USER appuser

EXPOSE 5000
CMD ["uv", "run", "app.py"]
