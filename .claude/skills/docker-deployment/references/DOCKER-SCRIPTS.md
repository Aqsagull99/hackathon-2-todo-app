# Docker Scripts for Python/FastAPI Applications

This document contains scripts for automated Dockerfile and Docker Compose generation for Python/FastAPI applications.

## Automated Dockerfile Generator Script

```python
#!/usr/bin/env python3
"""
Automated Dockerfile generator for Python/FastAPI applications
Supports multiple configurations: development, production, with/without DHI
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
```

## Docker Compose Generator Script

```python
#!/usr/bin/env python3
"""
Automated Docker Compose generator for multi-service Python/FastAPI applications
"""

import argparse
import yaml
from pathlib import Path

def generate_compose_file(services_config):
    """Generate Docker Compose file based on services configuration"""

    compose_data = {
        'version': '3.8',
        'services': {},
        'volumes': {}
    }

    # Add web service
    compose_data['services']['web'] = {
        'build': {
            'context': '.',
            'target': 'final'
        },
        'ports': ['8000:8000'],
        'environment': [
            'DATABASE_URL=postgresql://user:password@db:5432/myapp',
            'REDIS_URL=redis://redis:6379'
        ],
        'env_file': ['.env'],
        'restart': 'unless-stopped'
    }

    depends_conditions = []

    # Add database service if requested
    if 'postgres' in services_config:
        compose_data['services']['db'] = {
            'image': 'postgres:15',
            'restart': 'unless-stopped',
            'volumes': ['postgres_data:/var/lib/postgresql/data/'],
            'environment': [
                'POSTGRES_DB=myapp',
                'POSTGRES_USER=user',
                'POSTGRES_PASSWORD=password'
            ],
            'healthcheck': {
                'test': ['CMD-SHELL', 'pg_isready -U user -d myapp'],
                'interval': '10s',
                'timeout': '5s',
                'retries': 5
            }
        }
        compose_data['volumes']['postgres_data'] = None
        depends_conditions.append({'db': {'condition': 'service_healthy'}})

    # Add Redis service if requested
    if 'redis' in services_config:
        compose_data['services']['redis'] = {
            'image': 'redis:7-alpine',
            'restart': 'unless-stopped',
            'healthcheck': {
                'test': ['CMD', 'redis-cli', 'ping'],
                'interval': '10s',
                'timeout': '5s',
                'retries': 5
            }
        }
        depends_conditions.append({'redis': {'condition': 'service_healthy'}})

    # Add dependency conditions to web service
    if depends_conditions:
        compose_data['services']['web']['depends_on'] = {}
        for dep in depends_conditions:
            compose_data['services']['web']['depends_on'].update(dep)

    return yaml.dump(compose_data, default_flow_style=False, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Generate Docker Compose file for Python/FastAPI applications')
    parser.add_argument('--services', nargs='+', choices=['postgres', 'redis'],
                       default=['postgres'], help='Services to include in compose')
    parser.add_argument('--output', default='docker-compose.yml', help='Output filename')

    args = parser.parse_args()

    compose_content = generate_compose_file(args.services)

    with open(args.output, 'w') as f:
        f.write(compose_content)

    print(f"Docker Compose file generated successfully: {args.output}")
    print(f"Included services: {', '.join(args.services)}")

if __name__ == "__main__":
    main()
```

## Docker Prerequisites Validation Script

```bash
#!/bin/bash
# docker-validation.sh

echo "=== Docker Installation Validation ==="

# Check Docker installation
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    exit 1
else
    echo "✅ Docker is installed: $(docker --version)"
fi

# Check Docker daemon
if docker info &> /dev/null; then
    echo "✅ Docker daemon is running"
else
    echo "❌ Docker daemon is not running"
    exit 1
fi

# Check Docker Compose
if command -v docker compose &> /dev/null; then
    echo "✅ Docker Compose is installed: $(docker compose version)"
else
    echo "❌ Docker Compose is not installed"
    exit 1
fi

# Test basic functionality
if docker run --rm hello-world &> /dev/null; then
    echo "✅ Docker is functioning correctly"
else
    echo "❌ Docker test failed"
    exit 1
fi

# Check available memory
MEMORY_AVAILABLE=$(free -g | awk 'NR==2{print $7}')
if [ "$MEMORY_AVAILABLE" -ge 4 ]; then
    echo "✅ Sufficient memory available: ${MEMORY_AVAILABLE}GB free"
else
    echo "⚠️  Limited memory available: ${MEMORY_AVAILABLE}GB free (recommended: 4GB+)"
fi

# Check CPU cores
CPU_CORES=$(nproc)
if [ "$CPU_CORES" -ge 2 ]; then
    echo "✅ Sufficient CPU cores: ${CPU_CORES} cores detected"
else
    echo "⚠️  Limited CPU cores: ${CPU_CORES} cores detected (recommended: 2+)"
fi

echo "=== Validation Complete ==="
```

## AI Service Resource Configuration Script

```python
#!/usr/bin/env python3
"""
Script to generate Docker Compose configuration with resource constraints for AI services
"""

import argparse
import yaml

def generate_ai_compose_config(service_name, memory_limit="8G", cpu_limit="4.0", gpu_enabled=False):
    """Generate Docker Compose configuration with AI service resource constraints"""

    compose_config = {
        'version': '3.8',
        'services': {
            service_name: {
                'build': '.',
                'deploy': {
                    'resources': {
                        'limits': {
                            'cpus': cpu_limit,
                            'memory': memory_limit,
                            'pids': 300
                        },
                        'reservations': {
                            'cpus': str(float(cpu_limit) / 2),
                            'memory': str(int(memory_limit.replace('G', '')) // 2) + 'G'
                        }
                    }
                }
            }
        }
    }

    # Add GPU configuration if enabled
    if gpu_enabled:
        compose_config['services'][service_name]['deploy']['resources']['reservations']['devices'] = [{
            'driver': 'nvidia',
            'count': 'all',
            'capabilities': ['gpu', 'compute', 'utility']
        }]
        compose_config['services'][service_name]['environment'] = [
            'NVIDIA_VISIBLE_DEVICES=all',
            'NVIDIA_DRIVER_CAPABILITIES=compute,utility'
        ]

    return yaml.dump(compose_config, default_flow_style=False, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Generate Docker Compose config for AI services with resource constraints')
    parser.add_argument('--service-name', default='ai-service', help='Name of the service')
    parser.add_argument('--memory-limit', default='8G', help='Memory limit (e.g., 4G, 8G)')
    parser.add_argument('--cpu-limit', default='4.0', help='CPU limit (e.g., 2.0, 4.0)')
    parser.add_argument('--enable-gpu', action='store_true', help='Enable GPU support')
    parser.add_argument('--output', default='docker-compose-ai.yml', help='Output filename')

    args = parser.parse_args()

    compose_content = generate_ai_compose_config(
        args.service_name,
        args.memory_limit,
        args.cpu_limit,
        args.enable_gpu
    )

    with open(args.output, 'w') as f:
        f.write(compose_content)

    print(f"Docker Compose AI config generated successfully: {args.output}")
    print(f"Service: {args.service_name}, Memory: {args.memory_limit}, CPU: {args.cpu_limit}")
    if args.enable_gpu:
        print("GPU support enabled")

if __name__ == "__main__":
    main()
```