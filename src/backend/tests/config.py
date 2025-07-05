"""
Test configuration settings

This module contains configuration settings specifically for testing environments,
including server setup, timeouts, and test execution parameters.
"""

from dataclasses import dataclass


@dataclass
class TestConfig:
    """Configuration for testing environment"""
    
    # Server configuration
    TEST_BASE_URL: str = "http://localhost:8000"
    TEST_HOST: str = "0.0.0.0"
    TEST_PORT: str = "8000"
    
    # Health check configuration
    HEALTH_ENDPOINT: str = "/health"
    HEALTH_CHECK_TIMEOUT: int = 2
    SERVER_START_TIMEOUT: int = 1
    MAX_START_ATTEMPTS: int = 30
    
    # Server commands
    UV_COMMAND: str = "uv"
    RUN_COMMAND: str = "run"
    UVICORN_COMMAND: str = "uvicorn"
    APP_MODULE: str = "api:app"


# Instantiate configuration object
test_config = TestConfig()
