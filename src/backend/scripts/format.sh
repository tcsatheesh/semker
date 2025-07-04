#!/bin/bash

# Format script for Python code
# This script formats the codebase using black and isort

set -e

# Change to the backend directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(dirname "$SCRIPT_DIR")"

echo "🔧 Formatting Python code in $BACKEND_DIR..."

# Change to the backend directory
cd "$BACKEND_DIR"

# Check if we're in a virtual environment or use uv
if [[ -n "$VIRTUAL_ENV" ]] || command -v uv &> /dev/null; then
    echo "📦 Using available Python environment..."
    
    # Format imports with isort
    echo "🔀 Sorting imports with isort..."
    if command -v uv &> /dev/null; then
        uv run isort . --check-only --diff || uv run isort .
    elif python -m isort --version &> /dev/null; then
        python -m isort . --check-only --diff || python -m isort .
    else
        echo "⚠️  isort not available, skipping import sorting"
    fi
    
    # Format code with black
    echo "⚫ Formatting code with black..."
    if command -v uv &> /dev/null; then
        uv run black . --check --diff || uv run black .
    elif python -m black --version &> /dev/null; then
        python -m black . --check --diff || python -m black .
    else
        echo "⚠️  black not available, skipping code formatting"
    fi
    
    echo "✅ Code formatting completed!"
else
    echo "❌ No Python environment found. Please activate a virtual environment or install uv."
    exit 1
fi
