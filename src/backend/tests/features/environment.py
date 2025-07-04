"""
Behave environment configuration for Semker API tests
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path
from typing import Any, Optional

# Add the backend directory to Python path
backend_dir: Path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

# Also add the parent directory for imports
parent_dir: Path = backend_dir.parent
sys.path.insert(0, str(parent_dir))

# Server process holder
server_process: Optional[subprocess.Popen[bytes]] = None
BASE_URL: str = "http://localhost:8000"


def before_all(context: Any) -> None:
    """Setup before all tests"""
    print("Setting up test environment...")
    
    # Check if server is already running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code == 200:
            print("API server is already running")
            context.server_started_by_tests = False
            return
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        pass
    
    # Start the server
    print("Starting API server for tests...")
    context.server_started_by_tests = True
    start_test_server(context)


def after_all(context: Any) -> None:
    """Cleanup after all tests"""
    if hasattr(context, 'server_started_by_tests') and context.server_started_by_tests:
        stop_test_server(context)


def start_test_server(context: Any) -> None:
    """Start the API server for testing"""
    global server_process
    
    try:
        # Change to backend directory first
        os.chdir(backend_dir)
        
        # Start server using uvicorn with absolute module path
        server_process = subprocess.Popen([
            "uv", "run", "uvicorn", "api:app",
            "--host", "0.0.0.0",
            "--port", "8000"
        ], cwd=backend_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        max_attempts = 30
        for attempt in range(max_attempts):
            try:
                response = requests.get(f"{BASE_URL}/health", timeout=1)
                if response.status_code == 200:
                    print(f"Server started successfully after {attempt + 1} attempts")
                    context.server_process = server_process
                    return
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                time.sleep(1)
        
        raise Exception("Server failed to start within expected time")
        
    except Exception as e:
        print(f"Failed to start server: {e}")
        if server_process:
            server_process.terminate()
        raise


def stop_test_server(context: Any) -> None:
    """Stop the test server"""
    global server_process
    
    if hasattr(context, 'server_process') and context.server_process:
        print("Stopping test server...")
        context.server_process.terminate()
        context.server_process.wait()
        print("Test server stopped")
    elif server_process:
        server_process.terminate()
        server_process.wait()


def before_scenario(context: Any, scenario: Any) -> None:
    """Setup before each scenario"""
    # Reset any scenario-specific data
    if hasattr(context, 'message_id'):
        delattr(context, 'message_id')
    if hasattr(context, 'response'):
        delattr(context, 'response')
    if hasattr(context, 'response_data'):
        delattr(context, 'response_data')


def after_scenario(context: Any, scenario: Any) -> None:
    """Cleanup after each scenario"""
    # Clean up any test data if needed
    pass
