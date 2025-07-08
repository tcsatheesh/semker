"""Configuration settings for AI agents.

This module contains all configuration settings and constants used by the
agent system, organized by namespace for better separation of concerns.

Namespaces:
    HttpClient: HTTP client configuration settings
    Services: External service configuration settings
    Roaming: Roaming agent-specific configuration
    Billing: Billing agent-specific configuration
    Planner: Planner agent-specific configuration
    Templates: Template strings for agent instructions
    Headers: Helper utilities for generating headers
"""

import os
from typing import Final, Dict, List


class HttpClient:
    """HTTP client configuration settings for Semantic Kernel integration."""

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
    """External service configuration settings."""

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
    """Helper class for generating agent headers."""

    @staticmethod
    def get_mcp_headers(message_id: str, thread_id: str) -> Dict[str, str]:
        """Generate headers for MCP plugin connections.

        Args:
            message_id: Unique identifier for the message
            thread_id: Unique identifier for the conversation thread

        Returns:
            Dictionary containing required headers for MCP plugins
        """
        return {
            HttpClient.MESSAGE_ID_HEADER: message_id,
            HttpClient.CONVERSATION_ID_HEADER: thread_id,
        }
