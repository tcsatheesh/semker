#!/bin/bash

# Run Semker API using Docker
# Usage: ./docker-run.sh [OPTIONS]
#   Options:
#     --port PORT     Set port (default: 8000)
#     --host HOST     Set host (default: 0.0.0.0)
#     --name NAME     Set container name (default: semker-api)
#     --detach        Run in background
#     --help          Show this help

set -e

# Default values
PORT="8000"
HOST="0.0.0.0"
CONTAINER_NAME="semker-api"
DETACH=""
IMAGE_NAME="semker-api:latest"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --port)
            PORT="$2"
            shift 2
            ;;
        --host)
            HOST="$2"
            shift 2
            ;;
        --name)
            CONTAINER_NAME="$2"
            shift 2
            ;;
        --detach|-d)
            DETACH="-d"
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --port PORT     Set port (default: 8000)"
            echo "  --host HOST     Set host (default: 0.0.0.0)"
            echo "  --name NAME     Set container name (default: semker-api)"
            echo "  --detach, -d    Run in background"
            echo "  --help, -h      Show this help"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Stop and remove existing container if it exists
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "🛑 Stopping and removing existing container: ${CONTAINER_NAME}"
    docker stop "${CONTAINER_NAME}" >/dev/null 2>&1 || true
    docker rm "${CONTAINER_NAME}" >/dev/null 2>&1 || true
fi

# Check if image exists, build if not
if ! docker images --format '{{.Repository}}:{{.Tag}}' | grep -q "^${IMAGE_NAME}$"; then
    echo "🔨 Image ${IMAGE_NAME} not found, building..."
    ./docker-build.sh
fi

echo "� Starting Semker API container..."
echo "   • Container: ${CONTAINER_NAME}"
echo "   • Image: ${IMAGE_NAME}"
echo "   • Host: ${HOST}"
echo "   • Port: ${PORT}"

# Run the container
docker run ${DETACH} \
    --name "${CONTAINER_NAME}" \
    -p "${PORT}:${PORT}" \
    -e HOST="${HOST}" \
    -e PORT="${PORT}" \
    -e HEALTH_CHECK_URL="http://127.0.0.1:${PORT}/health" \
    "${IMAGE_NAME}"

if [ -n "$DETACH" ]; then
    echo ""
    echo "✅ Container started in background!"
    echo "🌐 API available at:"
    echo "  • API:               http://localhost:${PORT}"
    echo "  • API Documentation: http://localhost:${PORT}/docs"
    echo "  • Health Check:      http://localhost:${PORT}/health"
    echo ""
    echo "📋 Useful commands:"
    echo "  • View logs:         docker logs -f ${CONTAINER_NAME}"
    echo "  • Stop container:    docker stop ${CONTAINER_NAME}"
    echo "  • Remove container:  docker rm ${CONTAINER_NAME}"
    echo "  • Shell access:      docker exec -it ${CONTAINER_NAME} /bin/bash"
    echo "  • Check health:      docker inspect ${CONTAINER_NAME} --format='{{.State.Health.Status}}'"
else
    echo ""
    echo "✅ Container running in foreground!"
    echo "🌐 API available at:"
    echo "  • API:               http://localhost:${PORT}"
    echo "  • API Documentation: http://localhost:${PORT}/docs"
    echo "  • Health Check:      http://localhost:${PORT}/health"
    echo ""
    echo "💡 Press Ctrl+C to stop the container"
fi
