import json
from typing import Callable

from pydantic import BaseModel
from semantic_kernel import Kernel
from semantic_kernel.agents import AgentThread, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings
from semantic_kernel.connectors.mcp import MCPStreamableHttpPlugin
from semantic_kernel.functions.kernel_arguments import KernelArguments

from agents.base import BaseAgent
from config.constants import MessageStatus
from .config import Tariff, Headers


class TariffAgentResponse(BaseModel):
    reply: str
    human_input_required: bool


class TariffAgent(BaseAgent):
    def __init__(
        self,
        kernel: Kernel,
    ) -> None:
        settings = AzureChatPromptExecutionSettings()
        settings.response_format = TariffAgentResponse
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
    ) -> tuple[str, AgentThread, str]:
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

        _result: TariffAgentResponse = TariffAgentResponse.model_validate(
            json.loads(_response.message.content),
        )

        await plugin.close()

        return _result.reply, _response.thread, self.name
