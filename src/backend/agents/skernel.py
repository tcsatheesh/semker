import os
import httpx

from openai import AsyncAzureOpenAI

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

from models.schemas import Message

from telemetry.httpx_logger import (
    request_interceptor,
    response_interceptor,
    error_interceptor,
)


class KernelUtils:

    def __init__(
        self,
        message_id: str,
        thread_id: str,
    ):
        self.kernel = self._init_kernel(
            message_id=message_id,
            thread_id=thread_id,
        )

    def _init_kernel(
        self,
        message_id: str,
        thread_id: str,
    ):
        # 1. Create your custom httpx.AsyncClient
        _custom_httpx_client = httpx.AsyncClient(
            timeout=httpx.Timeout(
                timeout=60.0,
                connect=5.0,
            ),
            limits=httpx.Limits(
                max_connections=100,
                max_keepalive_connections=20,
            ),
            headers={
                "x-ms-message-id": message_id,
                "x-ms-conversation_id": thread_id,
            },
            event_hooks={
                "request": [request_interceptor],
                "response": [response_interceptor],
                "error": [error_interceptor],
            },
        )
        _azure_openai_async_client = AsyncAzureOpenAI(
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
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
    ):
        _kernel = self.kernel

        from agents.planner import PlannerAgent

        _planner_agent = PlannerAgent(
            kernel=_kernel,
        )

        return _planner_agent
