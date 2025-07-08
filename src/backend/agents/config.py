"""
Configuration settings and constants for AI agents.

This module contains all configuration settings, constants, and helper utilities
used by the agent system. It provides a centralized location for managing
agent configurations, service endpoints, HTTP client settings, and header
generation utilities.

Classes:
    HttpClient: HTTP client configuration for Semantic Kernel integration
    Services: External service endpoints and Azure OpenAI configuration
    Headers: Helper utilities for generating request headers

Features:
    - Environment variable-based configuration
    - Centralized service endpoint management
    - HTTP client timeout and connection settings
    - MCP server URL configuration
    - Azure OpenAI service integration
    - Request header generation utilities

Example:
    ```python
    from agents.config import Services, Headers
    
    # Get service endpoint
    billing_url = Services.BILLING_MCP_SERVER_URL
    
    # Generate headers
    headers = Headers.get_mcp_headers("msg-123", "thread-456")
    ```
"""

import os
from typing import Final, Dict, List


class HttpClient:
    """
    HTTP client configuration settings for Semantic Kernel integration.

    This class contains all HTTP client-related configuration settings used
    by agents when making requests to external services. It defines timeout
    values, connection limits, and header names for request correlation.

    Configuration Categories:
        - Timeout Settings: Request and connection timeout values
        - Connection Limits: Maximum connections and keepalive settings
        - Header Names: Standard header names for request correlation

    Usage:
        These settings are used by the KernelUtils class when creating
        custom HTTP clients for Semantic Kernel integration.

    Example:
        ```python
        timeout = HttpClient.TIMEOUT_SECONDS  # 60.0
        max_conn = HttpClient.MAX_CONNECTIONS  # 100
        ```
    """

    # Timeout settings
    TIMEOUT_SECONDS: Final[float] = 60.0
    CONNECT_TIMEOUT_SECONDS: Final[float] = 5.0

    # Connection limits
    MAX_CONNECTIONS: Final[int] = 100
    MAX_KEEPALIVE_CONNECTIONS: Final[int] = 20

    # Header names
    MESSAGE_ID_HEADER: Final[str] = "x-ms-message-id"
    CONVERSATION_ID_HEADER: Final[str] = "x-ms-conversation-id"


class Services:
    """
    External service configuration settings and endpoints.

    This class contains all configuration related to external services
    used by the agent system, including MCP server endpoints and Azure
    OpenAI configuration. All URLs are configurable via environment variables.

    Service Categories:
        - MCP Server Endpoints: URLs for Model Context Protocol servers
        - Azure OpenAI: API version and authentication scope configuration

    Environment Variables:
        - ROAMING_MCP_SERVER_URL: Roaming service MCP endpoint
        - BILLING_MCP_SERVER_URL: Billing service MCP endpoint
        - TARIFF_MCP_SERVER_URL: Tariff service MCP endpoint
        - FAQ_MCP_SERVER_URL: FAQ service MCP endpoint
        - AZURE_OPENAI_API_VERSION: Azure OpenAI API version

    Example:
        ```python
        billing_url = Services.BILLING_MCP_SERVER_URL
        api_version = Services.AZURE_OPENAI_API_VERSION
        ```
    """

    # Base URLs for external services
    ROAMING_MCP_SERVER_URL: Final[str] = os.getenv(
        "ROAMING_MCP_SERVER_URL", "http://localhost:8002/roam/mcp"
    )
    BILLING_MCP_SERVER_URL: Final[str] = os.getenv(
        "BILLING_MCP_SERVER_URL", "http://localhost:8002/bill/mcp"
    )
    TARIFF_MCP_SERVER_URL: Final[str] = os.getenv(
        "TARIFF_MCP_SERVER_URL", "http://localhost:8002/tariff/mcp"
    )
    FAQ_MCP_SERVER_URL: Final[str] = os.getenv(
        "FAQ_MCP_SERVER_URL", "http://localhost:8002/faq/mcp"
    )

    # Azure OpenAI configuration
    AZURE_OPENAI_API_VERSION: Final[str] = os.getenv(
        "AZURE_OPENAI_API_VERSION", "2024-02-01"
    )
    AZURE_COGNITIVE_SERVICES_SCOPE: Final[str] = (
        "https://cognitiveservices.azure.com/.default"
    )

class Headers:
    """
    Helper class for generating request headers for agent operations.

    This class provides utility methods for generating standardized HTTP headers
    used in agent requests, particularly for MCP plugin connections and service
    correlation.

    Features:
        - Standardized header generation for MCP plugins
        - Request correlation with message and thread IDs
        - Consistent header naming across all agents

    Methods:
        get_mcp_headers: Generate headers for MCP plugin connections
    """

    @staticmethod
    def get_mcp_headers(message_id: str, thread_id: str) -> Dict[str, str]:
        """
        Generate standardized headers for MCP plugin connections.

        This method creates a dictionary of HTTP headers required for MCP
        plugin connections, including message and thread correlation IDs
        for request tracking and conversation context management.

        Args:
            message_id: Unique identifier for the current message being processed.
                       Used for request correlation and tracing across services.
            thread_id: Unique identifier for the conversation thread.
                      Used for maintaining conversation context and history.

        Returns:
            Dict[str, str]: Dictionary containing standardized headers:
                          - x-ms-message-id: Message correlation ID
                          - x-ms-conversation-id: Thread correlation ID

        Example:
            ```python
            headers = Headers.get_mcp_headers("msg-123", "thread-456")
            # Returns: {
            #     "x-ms-message-id": "msg-123",
            #     "x-ms-conversation-id": "thread-456"
            # }
            ```
        """
        return {
            HttpClient.MESSAGE_ID_HEADER: message_id,
            HttpClient.CONVERSATION_ID_HEADER: thread_id,
        }
