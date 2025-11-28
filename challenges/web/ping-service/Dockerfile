FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

COPY app.py .
COPY templates/ templates/

RUN echo "flag{command_injection_is_bad_mkay}" > /app/flag.txt

EXPOSE 5000
CMD ["uv", "run", "app.py"]
