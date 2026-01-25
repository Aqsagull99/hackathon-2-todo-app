#!/usr/bin/env python3
"""
Dockerfile generator for Python/FastAPI applications
"""

import argparse
import os
from pathlib import Path

def generate_dockerfile(config_type="production"):
    """Generate Dockerfile based on configuration type"""

    if config_type == "development":
        return generate_dev_dockerfile()
    elif config_type == "production":
        return generate_prod_dockerfile()
    elif config_type == "dhi":
        return generate_dhi_dockerfile()
    else:
        raise ValueError(f"Unsupported config type: {config_type}")

def generate_dev_dockerfile():
    """Generate development Dockerfile"""
    return """# syntax=docker/dockerfile:1

# === Build stage: Install dependencies and create virtual environment ===
FROM python:3.11-slim AS builder

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# === Final stage: Create minimal runtime image ===
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser

# Copy Python dependencies from builder stage
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Make sure scripts in .local are usable
ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
"""

def generate_prod_dockerfile():
    """Generate production Dockerfile"""
    return """# syntax=docker/dockerfile:1

# === Build stage: Install dependencies and create virtual environment ===
FROM python:3.11-slim AS builder

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# === Final stage: Create minimal runtime image ===
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser

# Copy Python dependencies from builder stage
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Make sure scripts in .local are usable
ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

def generate_dhi_dockerfile():
    """Generate Dockerfile with Docker Hardened Images (DHI)"""
    return """# syntax=docker/dockerfile:1

# === Build stage: Install dependencies and create virtual environment ===
FROM dhi.io/python:3.11-alpine3.18-dev AS builder

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app

RUN python -m venv /app/venv
COPY requirements.txt .

# Install any additional packages if needed using apk
RUN apk add --no-cache gcc musl-dev && \\
    pip install --no-cache-dir -r requirements.txt

# === Final stage: Create minimal runtime image ===
FROM dhi.io/python:3.11-alpine3.18

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

# Create non-root user for security
RUN addgroup -g 1001 -S appgroup && \\
    adduser -S appuser -u 1001 -G appgroup

COPY app.py ./
COPY --from=builder /app/venv /app/venv

# Switch to non-root user
USER appuser

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
"""

def main():
    parser = argparse.ArgumentParser(description='Generate Dockerfile for Python/FastAPI applications')
    parser.add_argument('--type', choices=['development', 'production', 'dhi'],
                       default='production', help='Dockerfile type to generate')
    parser.add_argument('--output', default='Dockerfile', help='Output filename')

    args = parser.parse_args()

    dockerfile_content = generate_dockerfile(args.type)

    with open(args.output, 'w') as f:
        f.write(dockerfile_content)

    print(f"Dockerfile generated successfully: {args.output}")
    print(f"Type: {args.type}")

if __name__ == "__main__":
    main()
