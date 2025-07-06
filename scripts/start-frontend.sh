#!/bin/bash

# Startup script for Semker frontend

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Navigate to the frontend directory (parent of scripts)
FRONTEND_DIR="$(dirname "$SCRIPT_DIR")/src/frontend"

echo "Starting Semker frontend..."

# Change to frontend directory
cd "$FRONTEND_DIR"

npm start

