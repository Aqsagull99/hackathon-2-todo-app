# Docker Security Best Practices for Python/FastAPI Applications

This document outlines security best practices for Docker containers in Python/FastAPI applications, particularly for production deployments.

## Security Hardening Techniques

### 1. Use Non-Root Users

Always run containers as non-root users to minimize potential damage from security vulnerabilities:

```dockerfile
# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser

# Copy application with proper ownership
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser
```

### 2. Multi-Stage Builds

Separate build and runtime environments to reduce attack surface:

```dockerfile
# Build stage
FROM python:3.11-slim AS builder
# Install dependencies, build application
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim
# Copy only necessary artifacts from builder stage
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local
```

### 3. Minimal Base Images

Use minimal base images like Alpine or Docker Hardened Images (DHI):

```dockerfile
# Use hardened images
FROM dhi.io/python:3.11-alpine3.18
# Or use minimal alpine images
FROM python:3.11-alpine
```

### 4. Read-Only Root Filesystem

Mount the root filesystem as read-only where possible:

```yaml
# In docker-compose.yml
services:
  web:
    # ... other config
    read_only: true
    tmpfs:
      - /tmp
      - /run
```

### 5. Drop Capabilities

Drop unnecessary Linux capabilities:

```yaml
# In docker-compose.yml
services:
  web:
    # ... other config
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE  # Only add what's absolutely necessary
```

### 6. Secrets Management

Never store secrets in Docker images or environment variables. Use Docker secrets:

```dockerfile
# In Dockerfile - don't include secrets
# Instead, use environment variables that will be populated at runtime
ENV DATABASE_URL=postgresql://user:password@db:5432/myapp
```

```yaml
# In docker-compose.yml
services:
  web:
    # ... other config
    secrets:
      - db_password
    environment:
      - POSTGRES_PASSWORD_FILE=/run/secrets/db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

## Production Security Configuration

### Complete Production Dockerfile with Security

```dockerfile
# syntax=docker/dockerfile:1

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
RUN apk add --no-cache gcc musl-dev && \
    pip install --no-cache-dir -r requirements.txt

# === Final stage: Create minimal runtime image ===
FROM dhi.io/python:3.11-alpine3.18

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

# Create non-root user and group for security
RUN addgroup -g 1001 -S appgroup && \
    adduser -S appuser -u 1001 -G appgroup

COPY app.py ./
COPY --from=builder /app/venv /app/venv

# Switch to non-root user
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Complete Production Docker Compose with Security

```yaml
version: "3.8"

services:
  web:
    build:
      context: .
      target: final
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/myapp
    env_file:
      - .env
    secrets:
      - db_password
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped
    # Security enhancements
    read_only: true
    tmpfs:
      - /tmp
      - /run
      - /var/run
    cap_drop:
      - ALL
    cap_add:
      - CHOWN
      - SETUID
      - SETGID
      - DAC_OVERRIDE
    security_opt:
      - no-new-privileges:true

  db:
    image: postgres:15
    restart: unless-stopped
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD_FILE=/run/secrets/db_password
    secrets:
      - db_password
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d myapp"]
      interval: 10s
      timeout: 5s
      retries: 5
    cap_drop:
      - ALL
    read_only: true
    tmpfs:
      - /tmp

secrets:
  db_password:
    file: ./secrets/db_password.txt

volumes:
  postgres_data:
```

## Security Scanning

### Docker Bench for Security

Consider running Docker Bench for Security to scan for common security issues:

```bash
# Install and run Docker Bench for Security
docker run --rm -it --net host --pid host --userns host --cap-add audit_control \
    -e DOCKER_CONTENT_TRUST=$DOCKER_CONTENT_TRUST \
    -v /var/lib:/var/lib \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /usr/lib/systemd:/usr/lib/systemd \
    -v /etc:/etc \
    docker/docker-bench-security
```

### Trivy for Vulnerability Scanning

Scan images for vulnerabilities:

```bash
# Install Trivy
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy:latest image my-python-fastapi-app
```

## Additional Security Measures

### 1. Resource Limits

Prevent resource exhaustion attacks:

```yaml
services:
  web:
    # ... other config
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

### 2. Network Security

Use custom networks and restrict inter-service communication:

```yaml
services:
  web:
    networks:
      - app-network
  db:
    networks:
      - app-network
    # Restrict access if needed
    ports: []  # Don't expose DB port externally

networks:
  app-network:
    driver: bridge
```

### 3. Image Signing and Verification

Use Docker Content Trust for image signing:

```bash
export DOCKER_CONTENT_TRUST=1
docker build -t my-python-fastapi-app .
docker push my-python-fastapi-app
```

Following these security practices will significantly improve the security posture of your Python/FastAPI Docker deployments.