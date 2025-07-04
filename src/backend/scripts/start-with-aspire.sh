#!/bin/bash
# Run Semker backend with .NET Aspire Dashboard integration

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Navigate to the backend directory (parent of scripts)
BACKEND_DIR="$(dirname "$SCRIPT_DIR")"

echo "🔭 Starting Semker backend with .NET Aspire Dashboard integration"

# Set environment variables for telemetry
export TELEMETRY_ENABLED=true
export OTLP_ENDPOINT=${OTLP_ENDPOINT:-"http://localhost:4317"}
export TELEMETRY_CONSOLE=${TELEMETRY_CONSOLE:-"false"}
export ENVIRONMENT=${ENVIRONMENT:-"development"}

# Server configuration
export HOST=${HOST:-"0.0.0.0"}
export PORT=${PORT:-"8000"}
export RELOAD=${RELOAD:-"true"}
export LOG_LEVEL=${LOG_LEVEL:-"info"}

echo "📊 Telemetry endpoint: $OTLP_ENDPOINT"
echo "🌍 Environment: $ENVIRONMENT"
echo "🚀 Starting server on $HOST:$PORT"
echo ""

# Check if .NET Aspire Dashboard is running
echo "🔍 Checking .NET Aspire Dashboard availability..."
if curl -s "http://localhost:18888" > /dev/null 2>&1; then
    echo "✅ .NET Aspire Dashboard detected at http://localhost:18888"
else
    echo "⚠️  .NET Aspire Dashboard not detected at http://localhost:18888"
    echo "💡 Starting the Aspire Dashboard first:"
    docker run --rm -it -p 18888:18888 -p 4317:18889 \
    --name aspire-dashboard \
    mcr.microsoft.com/dotnet/aspire-dashboard:9.0
fi

echo ""
echo "🔄 Starting Semker backend..."

# Change to backend directory and run the application
cd "$BACKEND_DIR"
# Check if uv is available
if command -v uv &> /dev/null; then
    echo "Using uv to run the server..."
    uv run uvicorn api:app --host 0.0.0.0 --port 8000 --reload
else
    echo "uv not found, using python directly..."
    python api.py
fi

