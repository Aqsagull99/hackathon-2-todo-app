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
