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
    ROAMING_SERVICE_BASE_URL: Final[str] = os.getenv("ROAMING_SERVICE_URL", "http://localhost:8002")
    BILLING_SERVICE_BASE_URL: Final[str] = os.getenv("BILLING_SERVICE_URL", "http://localhost:8002")
    
    # Service endpoints
    ROAMING_MCP_ENDPOINT: Final[str] = f"{ROAMING_SERVICE_BASE_URL}/roam/mcp"
    BILLING_MCP_ENDPOINT: Final[str] = f"{BILLING_SERVICE_BASE_URL}/bill/mcp"
    
    # Azure OpenAI configuration
    AZURE_OPENAI_API_VERSION: Final[str] = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
    AZURE_COGNITIVE_SERVICES_SCOPE: Final[str] = "https://cognitiveservices.azure.com/.default"


class Roaming:
    """Roaming agent-specific configuration settings."""
    
    # Agent identity
    AGENT_NAME: Final[str] = "Roaming"
    PLUGIN_NAME: Final[str] = "RoamingPlugin"
    PLUGIN_DESCRIPTION: Final[str] = "A plugin for handling roaming."
    
    # Service endpoint
    @classmethod
    def get_mcp_endpoint(cls) -> str:
        """Get the MCP endpoint for roaming service."""
        return f"{Services.ROAMING_SERVICE_BASE_URL}/roam/mcp"
    
    # Agent template
    AGENT_TEMPLATE: Final[str] = """
        You are the Roaming Agent, responsible for managing roaming-related tasks.
        Your objective is to handle roaming inquiries and provide accurate information.
        Do not provide any personal or sensitive information.
        Ensure that you follow the provided instructions carefully.
    """


class Billing:
    """Billing agent-specific configuration settings."""
    
    # Agent identity
    AGENT_NAME: Final[str] = "Billing"
    PLUGIN_NAME: Final[str] = "BillingPlugin"
    PLUGIN_DESCRIPTION: Final[str] = "A plugin for handling billing."
    
    # Service endpoint
    @classmethod
    def get_mcp_endpoint(cls) -> str:
        """Get the MCP endpoint for billing service."""
        return f"{Services.BILLING_SERVICE_BASE_URL}/bill/mcp"
    
    # Agent template
    AGENT_TEMPLATE: Final[str] = """
        You are the Billing Agent, responsible for managing billing-related tasks.
        Your objective is to handle billing inquiries and provide accurate information.
        Do not provide any personal or sensitive information.
        If the billing data is not available, inform the user that you cannot access it.
        Ensure that you follow the provided instructions carefully.
    """


class Tariff:
    """Tariff agent-specific configuration settings."""
    
    # Agent identity
    AGENT_NAME: Final[str] = "Tariff"
    PLUGIN_NAME: Final[str] = "TariffPlugin"
    PLUGIN_DESCRIPTION: Final[str] = "A plugin for handling tariffs."
    
    # Service endpoint
    @classmethod
    def get_mcp_endpoint(cls) -> str:
        """Get the MCP endpoint for tariffs service."""
        return f"{Services.BILLING_SERVICE_BASE_URL}/tariff/mcp"
    
    # Agent template
    AGENT_TEMPLATE: Final[str] = """
        You are the Tariff Agent, responsible for managing tariff-related tasks.
        Your objective is to handle tariff inquiries and provide accurate information.
        Do not provide any personal or sensitive information.
        Provide tariff information is a tabular format.
        When comparing tariffs, ensure you provide the most relevant and up-to-date information in a table format.
        If the tariff data is not available, inform the user that you cannot access it.
        Ensure that you follow the provided instructions carefully.
    """


class Planner:
    """Planner agent-specific configuration settings."""
    
    # Agent identity
    AGENT_NAME: Final[str] = "Planner"
    
    # Available agents for routing
    AVAILABLE_AGENTS: Final[List[str]] = [
        "Billing: Handles billing-related tasks.",
        "Roaming: Manages roaming-related inquiries.",
        "Tariff: Handles tariff-related inquiries.",
        "Broadband: Manages broadband-support-related inquiries.",
        "Ticketing: Handles raising tickets tasks."
    ]
    
    # Agent template (raw template with placeholder)
    _AGENT_TEMPLATE: Final[str] = """
        You are the Planner Agent, responsible for planning tasks.
        You have access to the following agents:
        {available_agents}
        Select one of the agents based on the user message.
        If you are unable to determine the appropriate agent, respond with a message indicating that you cannot assist.
        Your objective is to provide a clear and concise response to the user.
        Do not provide any personal or sensitive information.
        Ensure that you follow the provided instructions carefully.
    """
    
    @classmethod
    def get_agent_template(cls) -> str:
        """Get the formatted planner agent template with available agents.
        
        Returns:
            Formatted template string with available agents list
        """
        agents_list = "\n        ".join(f"- {agent}" for agent in cls.AVAILABLE_AGENTS)
        return cls._AGENT_TEMPLATE.format(available_agents=agents_list)

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
