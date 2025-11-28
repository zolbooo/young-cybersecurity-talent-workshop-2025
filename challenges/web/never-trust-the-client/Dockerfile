FROM ubuntu:24.04

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app
RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y python3 && \
	apt-get clean && rm -rf /var/lib/apt/lists/*

COPY app.py .
COPY templates/ templates/
COPY static/ static/

RUN useradd -m appuser
USER appuser

EXPOSE 5000
CMD ["uv", "run", "app.py"]
