# Docker Prerequisites and System Validation

This document outlines the prerequisites, system requirements, and validation steps for Docker installations, particularly for AI services and production deployments.

## System Requirements

### Minimum Requirements
- **Operating System**: Linux (Ubuntu 20.04+, Debian 11+), macOS 10.15+, Windows 10/11
- **CPU**: 2+ cores (4+ recommended for AI workloads)
- **RAM**: 4GB minimum, 8GB+ recommended for AI services
- **Disk Space**: 20GB+ free space for Docker engine and images
- **Kernel**: Linux kernel 3.10+ (64-bit)

### Recommended for AI Services
- **RAM**: 16GB+ (32GB+ for large models)
- **CPU**: 4+ cores with high clock speed
- **Storage**: SSD with 50GB+ free space
- **GPU Support**: NVIDIA GPU with CUDA capability (for GPU acceleration)

## Docker Installation Validation

### Basic Installation Check
```bash
# Verify Docker daemon is running
systemctl status docker  # On Linux

# Check Docker version
docker --version

# Test Docker functionality
docker run hello-world

# Check Docker Compose
docker compose version

# View system-wide Docker information
docker info
```

### Advanced Validation
```bash
# Check available storage driver
docker info | grep -i storage

# Verify registry connectivity
docker run --rm hello-world

# Check Docker daemon configuration
docker system info

# List available images
docker image ls

# Check running containers
docker ps
```

## Docker Desktop Specific Setup

### Installation Verification
```bash
# For Docker Desktop on Windows/Mac:
# 1. Check if Docker Desktop service is running
# 2. Open Docker Desktop application
# 3. Verify status shows "Docker Desktop is running"

# Check if Docker Desktop is properly installed
docker version

# Verify Docker Compose is available
docker compose version

# Check system resources allocated to Docker Desktop
docker system df
```

### Resource Allocation in Docker Desktop
1. Open Docker Desktop application
2. Navigate to Settings > Resources
3. Configure:
   - **Memory**: Set to 8GB+ for AI workloads (default is usually 2GB)
   - **CPUs**: Set to 4+ cores for AI services (default is usually 2)
   - **Swap**: Set to 1GB+ if needed for large workloads
   - **Disk image size**: Set to 32GB+ for multiple large images

## GPU Support Setup (For AI Services)

### NVIDIA GPU Setup
```bash
# Install NVIDIA Container Toolkit (Linux)
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker

# Verify GPU support
nvidia-smi
docker run --rm --gpus all nvidia/cuda:11.0-base-ubuntu20.04 nvidia-smi
```

### GPU Validation
```bash
# Test GPU access in Docker
docker run --rm --gpus all nvidia/cuda:11.0-base-ubuntu20.04 nvidia-smi

# For CUDA samples
docker run --rm -it --gpus all nvidia/cuda:11.0-base-ubuntu20.04 nvidia-smi

# Test with PyTorch
docker run --rm --gpus all pytorch/pytorch:1.9.0-cuda11.1-cudnn8-runtime python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.device_count())"
```

## Docker Compose Validation

### Installation Check
```bash
# Verify Docker Compose is installed
docker compose version

# Test Docker Compose functionality
echo 'version: "3.8"
services:
  test:
    image: hello-world
    command: echo "Docker Compose is working!"
' > docker-compose-test.yml

docker compose -f docker-compose-test.yml up
docker compose -f docker-compose-test.yml down
```

## System Readiness for AI Services

### Pre-deployment Checks
```bash
# Check available memory
docker run --rm --memory=2g alpine free -m

# Test CPU allocation
docker run --rm --cpus=2.0 alpine lscpu

# Verify disk space in container
docker run --rm -v /tmp:/tmp alpine df -h /tmp

# Test network connectivity
docker run --rm alpine ping -c 3 google.com
```

### Performance Validation
```bash
# Memory stress test
docker run --rm --memory=1g --memory-swap=1g progrium/stress --vm 1 --vm-bytes 512M --vm-keep

# CPU stress test
docker run --rm --cpus=1.0 progrium/stress --cpu 1

# IO stress test
docker run --rm -v /tmp:/tmp progrium/stress --io 4
```

## Troubleshooting Common Issues

### Permission Issues
```bash
# Add user to docker group (Linux)
sudo groupadd docker  # if group doesn't exist
sudo usermod -aG docker $USER
newgrp docker  # or log out and back in
```

### Docker Daemon Issues
```bash
# Restart Docker daemon
sudo systemctl restart docker

# Check Docker daemon logs
sudo journalctl -u docker.service

# Reset Docker to factory defaults (Docker Desktop)
# Settings > Reset > Reset to factory defaults
```

### Resource Limit Issues
```bash
# Check current resource usage
docker stats --no-stream

# Check system limits
ulimit -a

# Increase file descriptor limits
echo "* soft nofile 1048576" | sudo tee -a /etc/security/limits.conf
echo "* hard nofile 1048576" | sudo tee -a /etc/security/limits.conf
```

## Validation Script Template

Create a validation script to check system readiness:

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

Run with: `chmod +x docker-validation.sh && ./docker-validation.sh`

This validation ensures your system is properly prepared for Docker deployments, especially for AI services and production workloads.