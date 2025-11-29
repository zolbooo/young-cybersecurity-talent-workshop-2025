FROM ubuntu:24.04

RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y python3 adduser && \
	apt-get clean && rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

COPY app.py ./
COPY templates/ templates/
COPY static/ static/

RUN useradd -m appuser && mkdir /app/db && \
		chown -R appuser:appuser /app/db
USER appuser
COPY --chown=appuser --chmod=600 database.db ./db/

EXPOSE 5000
CMD ["uv", "run", "app.py"]
