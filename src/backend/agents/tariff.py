import json
from typing import Callable, Final

from pydantic import BaseModel
from semantic_kernel import Kernel
from semantic_kernel.agents import AgentThread, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings
from semantic_kernel.connectors.mcp import MCPStreamableHttpPlugin
from semantic_kernel.functions.kernel_arguments import KernelArguments

from agents.base import BaseAgent, AgentResponse, AgentLLMResponse
from config.constants import MessageStatus
from .config import Services, Headers

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
        return Services.TARIFF_MCP_SERVER_URL

    # Agent template
    AGENT_TEMPLATE: Final[
        str
    ] = """
        You are the Tariff Agent, responsible for managing tariff-related tasks.
        Your objective is to handle tariff inquiries and provide accurate information.
        Do not provide any personal or sensitive information.
        Provide tariff information is a tabular format.
        When comparing tariffs, ensure you provide the most relevant and up-to-date information in a table format.
        If the tariff data is not available, inform the user that you cannot access it.
        Ensure that you follow the provided instructions carefully.
    """

class TariffAgent(BaseAgent):
    def __init__(
        self,
        kernel: Kernel,
    ) -> None:
        settings = AzureChatPromptExecutionSettings()
        settings.response_format = AgentLLMResponse
        settings.temperature = 0.0

        super().__init__(
            kernel=kernel,
            name=Tariff.AGENT_NAME,
            instructions=Tariff.AGENT_TEMPLATE,
            arguments=KernelArguments(settings=settings),
        )

    async def process_message_async(
        self,
        message: str,
        message_id: str,
        thread_id: str,
        thread: ChatHistoryAgentThread,
        on_intermediate_response: Callable[..., None],
    ) -> AgentResponse:
        plugin = MCPStreamableHttpPlugin(
            name=Tariff.PLUGIN_NAME,
            description=Tariff.PLUGIN_DESCRIPTION,
            url=Tariff.get_mcp_endpoint(),
            headers=Headers.get_mcp_headers(message_id, thread_id),
        )
        await plugin.connect()
        self.kernel.add_plugin(plugin)

        _response = await self.get_response(
            messages=message,
            thread=thread,
        )

        on_intermediate_response(
            message_id=message_id,
            status=MessageStatus.IN_PROGRESS,
            result="Tariff agent response received.",
            agent_name=self.name,
        )

        _llm_result: AgentLLMResponse = AgentLLMResponse.model_validate(
            json.loads(_response.message.content),
        )
        _result = AgentResponse()
        _result.reply = _llm_result.reply
        _result.human_input_required = _llm_result.human_input_required
        _result.able_to_serve = _llm_result.able_to_serve
        _result.thread = _response.thread
        _result.agent_name = self.name

        await plugin.close()

        return _result
