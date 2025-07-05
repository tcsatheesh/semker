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
from unittest.mock import patch

# Add the backend directory to Python path
backend_dir: Path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

# Also add the parent directory for imports
parent_dir: Path = backend_dir.parent
sys.path.insert(0, str(parent_dir))

# Import test config from tests directory (after path setup)
def _get_test_config():
    """Get test configuration after path setup to avoid import issues"""
    from tests.config import test_config
    return test_config

test_config = _get_test_config()

# Server process holder
server_process: Optional[subprocess.Popen[bytes]] = None

# Use test config values
BASE_URL: str = test_config.TEST_BASE_URL
TEST_HOST: str = test_config.TEST_HOST
TEST_PORT: str = test_config.TEST_PORT
HEALTH_ENDPOINT: str = test_config.HEALTH_ENDPOINT
HEALTH_CHECK_TIMEOUT: int = test_config.HEALTH_CHECK_TIMEOUT
SERVER_START_TIMEOUT: int = test_config.SERVER_START_TIMEOUT
MAX_START_ATTEMPTS: int = test_config.MAX_START_ATTEMPTS
UV_COMMAND: str = test_config.UV_COMMAND
RUN_COMMAND: str = test_config.RUN_COMMAND
UVICORN_COMMAND: str = test_config.UVICORN_COMMAND
APP_MODULE: str = test_config.APP_MODULE


async def mock_agent_process_message(
    message: str,
    message_id: str,
    thread_id: str,
    thread: Any,
    on_intermediate_response: Any = None,
) -> tuple[str, Any, str]:
    """Mock agent process message function for testing"""
    # Simulate intermediate response
    if on_intermediate_response:
        on_intermediate_response(
            message_id=message_id,
            status="in_progress",
            result="Processing your message...",
            agent_name="MockAgent",
        )
    
    # Return mock response
    return f"Mock response for: {message}", thread, "MockAgent"


def setup_mocks(context: Any) -> None:
    """Setup mocks for external dependencies"""
    print("Setting up mocks for external dependencies...")
    
    # Mock the agent processing to avoid Azure OpenAI calls
    context.agent_mock = patch('agents.base.BaseAgent.process_message_async', new=mock_agent_process_message)
    context.agent_mock.start()
    
    # Mock Azure OpenAI client to avoid actual API calls
    context.openai_mock = patch('openai.AsyncAzureOpenAI')
    context.openai_mock.start()
    
    # Mock httpx client calls to external services
    context.httpx_mock = patch('httpx.AsyncClient')
    context.httpx_mock.start()


def teardown_mocks(context: Any) -> None:
    """Teardown mocks"""
    if hasattr(context, 'agent_mock'):
        context.agent_mock.stop()
    if hasattr(context, 'openai_mock'):
        context.openai_mock.stop()
    if hasattr(context, 'httpx_mock'):
        context.httpx_mock.stop()


def before_all(context: Any) -> None:
    """Setup before all tests"""
    print("Setting up test environment...")
    
    # Setup mocking for Azure OpenAI calls
    setup_mocks(context)
    
    # Check if server is already running
    try:
        response = requests.get(f"{BASE_URL}{HEALTH_ENDPOINT}", timeout=HEALTH_CHECK_TIMEOUT)
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
    # Teardown mocks
    teardown_mocks(context)
    
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
            UV_COMMAND, RUN_COMMAND, UVICORN_COMMAND, APP_MODULE,
            "--host", TEST_HOST,
            "--port", TEST_PORT
        ], cwd=backend_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        max_attempts = MAX_START_ATTEMPTS
        for attempt in range(max_attempts):
            try:
                response = requests.get(f"{BASE_URL}{HEALTH_ENDPOINT}", timeout=SERVER_START_TIMEOUT)
                if response.status_code == 200:
                    print(f"Server started successfully after {attempt + 1} attempts")
                    context.server_process = server_process
                    return
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                time.sleep(SERVER_START_TIMEOUT)
        
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
