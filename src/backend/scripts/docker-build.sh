#!/bin/bash

# Build and run Semker API Docker container
# Usage: ./docker-build.sh

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Navigate to the backend directory (parent of scripts)
BACKEND_DIR="$(dirname "$SCRIPT_DIR")"

echo "🐳 Building Semker API Docker image..."

# Change to backend directory and build the Docker image
cd "$BACKEND_DIR"
docker build -t semker-api:latest .

echo "✅ Docker image built successfully!"
echo ""
echo "📋 Available commands:"
echo "  • Run container:     docker run -p 8000:8000 semker-api:latest"
echo "  • Run with compose:  docker-compose up"
echo "  • View image:        docker images | grep semker-api"
echo "  • Shell access:      docker run -it --entrypoint /bin/bash semker-api:latest"
echo ""
echo "🌐 Once running, access the API at:"
echo "  • API Documentation: http://localhost:8000/docs"
echo "  • Health Check:      http://localhost:8000/health"
