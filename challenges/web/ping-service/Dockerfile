FROM ubuntu:24.04

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

COPY app.py .
COPY templates/ templates/

RUN echo "flag{command_injection_is_bad_mkay}" > /app/flag.txt
RUN uv python install

RUN wget https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-agent/wazuh-agent_4.14.1-1_amd64.deb && \
		dpkg -i wazuh-agent_4.14.1-1_amd64.deb && \
		rm wazuh-agent_4.14.1-1_amd64.deb

EXPOSE 5000
CMD ["uv", "run", "app.py"]
