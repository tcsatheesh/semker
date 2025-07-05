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
    """Utility class for creating and managing Semantic Kernel instances.
    
    This class provides functionality to initialize Semantic Kernel instances
    with Azure OpenAI services, including custom HTTP clients with telemetry
    and logging capabilities.
    
    Attributes:
        kernel (Kernel): The initialized Semantic Kernel instance.
    """

    def __init__(
        self,
        message_id: str,
        thread_id: str,
    ) -> None:
        """Initialize KernelUtils with message and thread identifiers.
        
        Args:
            message_id: Unique identifier for the message.
            thread_id: Unique identifier for the conversation thread.
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
        """Initialize a Semantic Kernel instance with Azure OpenAI integration.
        
        Creates a custom HTTP client with telemetry hooks and configures
        the kernel with Azure OpenAI chat completion services.
        
        Args:
            message_id: Unique identifier for the message.
            thread_id: Unique identifier for the conversation thread.
            
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
        """Create and return a PlannerAgent instance.
        
        Initializes a PlannerAgent with the configured Semantic Kernel instance.
        
        Returns:
            PlannerAgent: Configured planner agent instance.
        """
        _kernel = self.kernel

        from agents.planner import PlannerAgent

        _planner_agent = PlannerAgent(
            kernel=_kernel,
        )

        return _planner_agent
