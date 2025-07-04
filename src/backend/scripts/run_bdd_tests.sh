#!/bin/bash

# BDD Test runner for Semker API
echo "🧪 Running Semker API BDD Tests"
echo "================================"

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Navigate to the backend directory (parent of scripts)
BACKEND_DIR="$(dirname "$SCRIPT_DIR")"

# Ensure we're in the backend directory
cd "$BACKEND_DIR"

# Check if behave is available
if ! command -v behave &> /dev/null; then
    echo "Installing behave..."
    uv add behave
fi

# Set Python path to include current directory
export PYTHONPATH="$(pwd):$PYTHONPATH"

# Run the tests
if [ "$1" = "smoke" ]; then
    echo "Running smoke tests only..."
    uv run behave tests/features/smoke_test.feature --format pretty --show-timings
elif [ -n "$1" ]; then
    echo "Running feature: $1"
    uv run behave tests/features/$1.feature --format pretty --show-timings
else
    echo "Running all BDD tests..."
    uv run behave tests/features --format pretty --show-timings
fi

echo ""
echo "✅ BDD tests completed!"
echo "📚 View results above or check logs for details"
