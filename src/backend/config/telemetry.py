"""
Telemetry configuration settings

This module contains configuration settings for telemetry, logging, and monitoring
systems to avoid circular imports with the main agents config.
"""

from dataclasses import dataclass


@dataclass
class TelemetryConfig:
    """Configuration for telemetry and logging"""
    
    # Service names and identifiers
    SERVICE_NAME: str = "semker-backend"
    SERVICE_VERSION: str = "0.1.0"
    SERVICE_NAMESPACE: str = "semker"
    
    # Middleware configuration
    MIDDLEWARE_TRACER_NAME: str = "semker.middleware"
    MIDDLEWARE_LOGGER_NAME: str = "semker.middleware"
    MIDDLEWARE_SERVICE_NAME: str = "backend"
    
    # HTTPX logger configuration
    HTTPX_LOGGER_NAME: str = "openai.httpx"
    HTTPX_LOG_FOLDER: str = "logs"
    HTTPX_LOG_FILE: str = "httpx.jsonl"
    
    # Request tracking headers
    REQUEST_ID_HEADER: str = "x-ms-request-id"
    USER_AGENT_HEADER: str = "user-agent"
    
    # Default values
    UNKNOWN_ROUTE: str = "unknown"
    UNKNOWN_ENDPOINT: str = "unknown"
    DEFAULT_USER_AGENT: str = ""
    DEFAULT_TIMEOUT: int = 2
    
    # OTLP Configuration
    DEFAULT_OTLP_ENDPOINT: str = "http://localhost:4317"


# Instantiate configuration object
telemetry_config = TelemetryConfig()
