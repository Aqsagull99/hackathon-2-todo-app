# Docker Optimization Techniques for Python/FastAPI Applications

This document covers optimization techniques to improve performance, reduce image size, and enhance efficiency of Docker containers for Python/FastAPI applications.

## Image Size Optimization

### 1. Multi-Stage Builds

Use multi-stage builds to separate build dependencies from runtime dependencies:

```dockerfile
# Build stage with all dependencies
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage with only necessary files
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appuser . .
USER appuser
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Minimal Base Images

Choose minimal base images to reduce image size:

```dockerfile
# Use slim images instead of full Python images
FROM python:3.11-slim
# Or use Alpine for even smaller images
FROM python:3.11-alpine
# Or use Docker Hardened Images for security + size benefits
FROM dhi.io/python:3.11-alpine3.18
```

### 3. Layer Caching Optimization

Order Dockerfile instructions to maximize layer caching:

```dockerfile
# Copy requirements first (changes less frequently)
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy application code last (changes more frequently)
COPY . .
```

### 4. Clean Up Package Managers

Clean up package manager caches to reduce image size:

```dockerfile
# For Alpine
RUN apk add --no-cache gcc musl-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del gcc musl-dev

# For Debian/Ubuntu
RUN apt-get update && apt-get install -y gcc && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y gcc && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

## Performance Optimization

### 1. FastAPI with Uvicorn Configuration

Optimize Uvicorn for production performance:

```dockerfile
CMD ["python", "-m", "uvicorn", "main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--timeout-keep-alive", "30", \
     "--max-keepalive-requests", "1000"]
```

### 2. Environment Variables for Performance

Set performance-related environment variables:

```dockerfile
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV UVICORN_WORKERS=4
ENV MAX_WORKERS=4
ENV PYTHONPATH=/app
```

### 3. Python Optimization Flags

Use Python optimization flags for better performance:

```dockerfile
ENV PYTHONOPTIMIZE=1  # Enable Python optimization
ENV PYTHONHASHSEED=0  # For reproducible builds
```

## Build Time Optimization

### 1. Efficient COPY Operations

Use efficient COPY operations to reduce build time:

```dockerfile
# Copy only necessary files first for better caching
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy application files separately
COPY . .
```

### 2. .dockerignore File

Use a .dockerignore file to exclude unnecessary files:

```
.git
.gitignore
README.md
Dockerfile
.dockerignore
node_modules
*.log
__pycache__
*.pyc
.env
.pytest_cache
.coverage
.vscode
.idea
*.swp
*.swo
.DS_Store
```

### 3. Build Args for Flexibility

Use build arguments for flexible builds:

```dockerfile
ARG PYTHON_VERSION=3.11-slim
FROM python:${PYTHON_VERSION}

ARG WORKERS=4
ENV UVICORN_WORKERS=${WORKERS}
```

Build with: `docker build --build-arg WORKERS=8 -t my-app .`

## Memory Optimization

### 1. Python Memory Settings

Configure Python memory settings:

```dockerfile
ENV PYTHONPATH=/app
ENV PYTHONSTARTUP=/app/.pythonrc
ENV PYTHONIOENCODING=utf-8
ENV PYTHONHASHSEED=random
```

### 2. Uvicorn Memory Configuration

Configure Uvicorn for memory efficiency:

```dockerfile
CMD ["python", "-m", "uvicorn", "main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "2", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--worker-connections", "1000", \
     "--max-requests", "1000", \
     "--max-requests-jitter", "100"]
```

## Production-Ready Optimized Dockerfile

```dockerfile
# syntax=docker/dockerfile:1

# === Build stage: Install dependencies and optimize ===
FROM python:3.11-slim AS builder

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies efficiently
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies with optimization
COPY requirements.txt .
RUN pip install --user --no-cache-dir --upgrade pip && \
    pip install --user --no-cache-dir -r requirements.txt

# === Final stage: Create optimized runtime image ===
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser

# Copy optimized dependencies from builder
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Make sure scripts in .local are usable
ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Optimized production command
CMD ["python", "-m", "uvicorn", "main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "4", \
     "--timeout-keep-alive", "30", \
     "--max-keepalive-requests", "1000"]
```

## Docker Compose Optimization

### Optimized Production Docker Compose

```yaml
version: "3.8"

services:
  web:
    build:
      context: .
      target: final
      args:
        - WORKERS=4
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/myapp
      - UVICORN_WORKERS=4
      - PYTHONPATH=/app
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped
    # Resource optimization
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
    # Health check
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  db:
    image: postgres:15
    restart: unless-stopped
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    # Resource optimization
    deploy:
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d myapp"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

## Build Cache Optimization

### Using BuildKit for Better Caching

Enable BuildKit for improved caching:

```bash
export DOCKER_BUILDKIT=1
docker build -t my-python-fastapi-app .
```

### Using External Cache for CI/CD

```dockerfile
# Use external cache for CI/CD
FROM python:3.11-slim AS builder
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --user --no-cache-dir -r requirements.txt
```

Build with: `docker build --build-arg BUILDKIT_INLINE_CACHE=1 --cache-from my-python-fastapi-app .`

## Resource Configuration for AI Services and Heavy Workloads

When deploying AI services or resource-intensive applications, proper resource allocation is critical for performance and stability.

### Memory and CPU Constraints

Configure appropriate resource limits to prevent container resource exhaustion:

```yaml
# In docker-compose.yml
services:
  ai-service:
    build: .
    deploy:
      resources:
        limits:
          # Memory limits (hard limits that cannot be exceeded)
          memory: 8G          # Maximum memory usage
          # CPU limits (hard limits on CPU usage)
          cpus: '4.0'         # Maximum 4 CPU cores
          pids: 200           # Maximum 200 processes/threads
        reservations:
          # Minimum guaranteed resources
          memory: 2G          # Guaranteed minimum memory
          cpus: '1.0'         # Guaranteed minimum CPU
```

### AI Service Specific Configuration

For AI and machine learning workloads:

```yaml
# Docker Compose with GPU support
services:
  ml-service:
    image: my-ml-service:latest
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia      # NVIDIA GPU support
              count: all          # Use all available GPUs
              capabilities: [gpu, compute, utility]
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - NVIDIA_DRIVER_CAPABILITIES=compute,utility
```

### Performance Tuning for AI Workloads

```dockerfile
# Optimized Dockerfile for AI services
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-devel

# Set environment variables for AI performance
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV TORCH_CUDNN_V8_API_ENABLED=1
ENV CUDA_HOME=/usr/local/cuda

# Set ulimits for AI workloads
RUN echo "* soft nofile 1048576" >> /etc/security/limits.conf && \
    echo "* hard nofile 1048576" >> /etc/security/limits.conf

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Runtime Resource Management

```bash
# Check container resource usage
docker stats

# Update resource limits for running container
docker update --memory 8g --cpus 4.0 container_name

# Run with specific resource constraints
docker run -m 8g --cpus=4.0 --pids-limit 300 my-ai-service
```

These optimization techniques will help you create efficient, performant Docker containers for your Python/FastAPI applications.