#!/bin/bash

# Startup script for Semker FastAPI server

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Navigate to the backend directory (parent of scripts)
BACKEND_DIR="$(dirname "$SCRIPT_DIR")"

echo "Starting Semker FastAPI server..."

# Change to backend directory
cd "$BACKEND_DIR"

# Check if uv is available
if command -v uv &> /dev/null; then
    echo "Using uv to run the server..."
    uv run uvicorn api:app --host 0.0.0.0 --port 8000 --reload
else
    echo "uv not found, using python directly..."
    python main.py
fi
