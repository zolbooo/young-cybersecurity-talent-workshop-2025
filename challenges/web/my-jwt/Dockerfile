# syntax=docker/dockerfile:1.7

# Use a slim Python base image
FROM python:3.11-slim

# Prevent Python from writing .pyc and enable unbuffered stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies (if needed) and create non-root user
RUN apt-get update -y && apt-get install -y --no-install-recommends \
      curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m appuser

WORKDIR /app

# Copy dependency manifest first for better layer caching
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY app /app/app

# Switch to non-root user
USER appuser

# Expose the port uvicorn will listen on
EXPOSE 8000

# Default start command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
