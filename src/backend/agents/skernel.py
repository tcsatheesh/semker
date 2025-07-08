"""Semantic Kernel utilities for Azure OpenAI integration.

This module prov            limits=httpx.Limits(
                timeout=HttpClient.TIMEOUT_SECONDS,
                connect=HttpClient.CONNECT_TIMEOUT_SECONDS,
            ),
            limits=httpx.Limits(
                max_connections=HttpClient.MAX_CONNECTIONS,
                max_keepalive_connections=HttpClient.MAX_KEEPALIVE_CONNECTIONS,
            ),
            headers={
                HttpClient.MESSAGE_ID_HEADER: message_id,
                HttpClient.CONVERSATION_ID_HEADER: thread_id,ies for initializing and configuring Semantic Kernel
instances with Azure OpenAI services, including custom HTTP clients with telemetry
and logging capabilities.

Classes:
    KernelUtils: Utility class for creating and managing Semantic Kernel instances.
"""

import os
import httpx
from typing import TYPE_CHECKING

from openai import AsyncAzureOpenAI

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

from telemetry.httpx_logger import (
    request_interceptor,
    response_interceptor,
    error_interceptor,
)
from .config import HttpClient, Services

if TYPE_CHECKING:
    from agents.planner import PlannerAgent


class KernelUtils:
    """
    Utility class for creating and managing Semantic Kernel instances.
    
    This class provides comprehensive functionality to initialize Semantic Kernel
    instances with Azure OpenAI services, including custom HTTP clients with
    telemetry, logging capabilities, and conversation context management.
    
    The KernelUtils class handles:
    - Semantic Kernel initialization with Azure OpenAI
    - Custom HTTP client configuration with telemetry hooks
    - Authentication management (API key or Azure AD)
    - Connection pooling and timeout configuration
    - Request/response interceptors for logging and monitoring
    - Agent instantiation and lifecycle management
    
    Attributes:
        kernel (Kernel): The initialized Semantic Kernel instance with
                        configured Azure OpenAI services and custom HTTP client.
    
    Example:
        ```python
        kernel_utils = KernelUtils(
            message_id="msg-123",
            thread_id="thread-456"
        )
        agent = kernel_utils.get_agent()
        response = await agent.process_message_async(...)
        ```
    """

    def __init__(
        self,
        message_id: str,
        thread_id: str,
    ) -> None:
        """
        Initialize KernelUtils with message and thread identifiers.
        
        Creates a Semantic Kernel instance configured with Azure OpenAI services,
        custom HTTP client with telemetry hooks, and conversation context headers.
        
        Args:
            message_id: Unique identifier for the current message being processed.
                       Used for request tracing and correlation across services.
            thread_id: Unique identifier for the conversation thread.
                      Used for maintaining conversation context and history.
        
        Side Effects:
            - Initializes the kernel attribute with a configured Semantic Kernel
            - Sets up HTTP client with telemetry interceptors
            - Configures Azure OpenAI authentication (API key or Azure AD)
            - Establishes connection pooling and timeout settings
        """
        self.kernel = self._init_kernel(
            message_id=message_id,
            thread_id=thread_id,
        )

    def _init_kernel(
        self,
        message_id: str,
        thread_id: str,
    ) -> Kernel:
        """
        Initialize a Semantic Kernel instance with Azure OpenAI integration.
        
        Creates a custom HTTP client with telemetry hooks and configures
        the kernel with Azure OpenAI chat completion services. This method
        handles both API key and Azure AD authentication methods.
        
        Args:
            message_id: Unique identifier for the message, added to HTTP headers
                       for request tracing and correlation.
            thread_id: Unique identifier for the conversation thread, added to
                      HTTP headers for conversation context management.
            
        Returns:
            Kernel: Configured Semantic Kernel instance with:
                   - Azure OpenAI chat completion service
                   - Custom HTTP client with telemetry hooks
                   - Request/response interceptors for logging
                   - Connection pooling and timeout configuration
                   - Authentication (API key or Azure AD token provider)
        
        Configuration:
            - Timeout settings from HttpClient configuration
            - Connection limits and keepalive settings
            - Request/response/error interceptors for telemetry
            - Authentication method determined by AZURE_OPENAI_API_KEY presence
        
        Example:
            The method creates an HTTP client with these features:
            - Request timeout: 30 seconds (configurable)
            - Connection timeout: 10 seconds (configurable)
            - Max connections: 100 (configurable)
            - Telemetry hooks for all request/response cycles
        """
            
        Returns:
            Kernel: Configured Semantic Kernel instance.
        """
        # 1. Create your custom httpx.AsyncClient
        _custom_httpx_client = httpx.AsyncClient(
            timeout=httpx.Timeout(
                timeout=HttpClient.TIMEOUT_SECONDS,
                connect=HttpClient.CONNECT_TIMEOUT_SECONDS,
            ),
            limits=httpx.Limits(
                max_connections=HttpClient.MAX_CONNECTIONS,
                max_keepalive_connections=HttpClient.MAX_KEEPALIVE_CONNECTIONS,
            ),
            headers={
                HttpClient.MESSAGE_ID_HEADER: message_id,
                HttpClient.CONVERSATION_ID_HEADER: thread_id,
            },
            event_hooks={
                "request": [request_interceptor],
                "response": [response_interceptor],
                "error": [error_interceptor],
            },
        )

        _azure_openai_async_client = None
        if os.getenv("AZURE_OPENAI_API_KEY", None):
            _azure_openai_async_client = AsyncAzureOpenAI(
                api_version=Services.AZURE_OPENAI_API_VERSION,
                http_client=_custom_httpx_client,
            )
        else:
            from azure.identity import DefaultAzureCredential, get_bearer_token_provider

            _azure_credential = DefaultAzureCredential()
            _token_provider = get_bearer_token_provider(
                _azure_credential,
                Services.AZURE_COGNITIVE_SERVICES_SCOPE,
            )
            _azure_openai_async_client = AsyncAzureOpenAI(
                api_version=Services.AZURE_OPENAI_API_VERSION,
                azure_ad_token_provider=_token_provider,
                http_client=_custom_httpx_client,
            )

        _kernel = Kernel()

        _kernel.add_service(
            AzureChatCompletion(
                async_client=_azure_openai_async_client,
            )
        )
        return _kernel

    def get_agent(
        self,
    ) -> "PlannerAgent":
        """
        Create and return a PlannerAgent instance.
        
        Initializes a PlannerAgent with the configured Semantic Kernel instance.
        The PlannerAgent serves as the main entry point for message processing
        and routing to appropriate specialized agents.
        
        Returns:
            PlannerAgent: Configured planner agent instance ready for message processing.
                         The agent is initialized with the kernel containing Azure OpenAI
                         services and custom HTTP client configuration.
        
        Example:
            ```python
            kernel_utils = KernelUtils("msg-123", "thread-456")
            planner_agent = kernel_utils.get_agent()
            
            response = await planner_agent.process_message_async(
                message="What is my bill?",
                message_id="msg-123",
                thread_id="thread-456",
                thread=chat_thread,
                on_intermediate_response=callback
            )
            ```
        """
        _kernel = self.kernel

        from agents.planner import PlannerAgent

        _planner_agent = PlannerAgent(
            kernel=_kernel,
        )

        return _planner_agent
