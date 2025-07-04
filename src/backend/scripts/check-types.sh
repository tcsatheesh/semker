#!/bin/bash
# Type checking script for Semker backend

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Navigate to the backend directory (parent of scripts)
BACKEND_DIR="$(dirname "$SCRIPT_DIR")"

echo "Running strict type checking on Semker backend..."

# Change to backend directory and run type checking
cd "$BACKEND_DIR"
uv run mypy --explicit-package-bases api.py models/ config/ process/ __init__.py

echo "✅ All type checks passed!"
echo "🔒 Backend code has strict type safety enabled"
