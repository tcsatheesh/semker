#!/bin/bash

# Startup script for Semker MCP Server

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Navigate to the mcpserver directory (parent of scripts)
MCPSERVER_DIR="$(dirname "$SCRIPT_DIR")/src/mcpserver"

echo "Starting Semker MCP Server..."

# Change to mcpserver directory
cd "$MCPSERVER_DIR"

# Check if uv is available
if command -v uv &> /dev/null; then
    echo "Using uv to run the server..."
    uv run uvicorn main:app --port 8002 --reload
else
    echo "uv not found, using python directly..."
    uvicorn main:app --port 8002 --reload
fi
