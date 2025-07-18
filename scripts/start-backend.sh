#!/bin/bash

# Startup script for Semker FastAPI server

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Navigate to the backend directory (parent of scripts)
BACKEND_DIR="$(dirname "$SCRIPT_DIR")/src/backend"

echo "Starting Semker FastAPI server..."

# Change to backend directory
cd "$BACKEND_DIR"

# Load environment variables from .env file
if [ -f .env ]; then
    echo "Loading environment variables from .env file..."
    export $(grep -v '^#' .env | xargs)
else
    echo ".env file not found, exiting..."
    exit 1
fi

# Check if uv is available
if command -v uv &> /dev/null; then
    echo "Using uv to run the server..."
    uv run uvicorn api:app --host 0.0.0.0 --port 8000 --reload
else
    echo "uv not found, using python directly..."
    python api.py
fi
