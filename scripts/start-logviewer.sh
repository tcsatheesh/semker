#!/bin/bash

# Startup script for Semker Log Viewer

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Navigate to the logviewer directory (parent of scripts)
LOGVIEWER_DIR="$(dirname "$SCRIPT_DIR")/src/logviewer"

echo "Starting Semker Log Viewer..."

# Change to logviewer directory
cd "$LOGVIEWER_DIR"

# Check if uv is available
if command -v uv &> /dev/null; then
    echo "Using uv to run the server..."
    uv run python app.py
else
    echo "uv not found, using python directly..."
    python app.py
fi
