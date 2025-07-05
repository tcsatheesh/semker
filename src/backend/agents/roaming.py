import json
from typing import Callable
from pydantic import BaseModel

from semantic_kernel import Kernel
from semantic_kernel.agents import AgentThread, ChatHistoryAgentThread
from semantic_kernel.connectors.mcp import MCPStreamableHttpPlugin
from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings
from semantic_kernel.functions.kernel_arguments import KernelArguments

from agents.base import BaseAgent
from config.constants import MessageStatus

class RoamingAgentResponse(BaseModel):
    reply: str
    human_input_required: bool


class RoamingAgent(BaseAgent):
    """Roaming Agent for handling roaming-related tasks."""

    def __init__(
        self,
        kernel: Kernel,
    ):
        settings = AzureChatPromptExecutionSettings()
        settings.response_format = RoamingAgentResponse
        settings.temperature = 0.0

        super().__init__(
            kernel=kernel,
            name="Roaming",
            instructions=RoamingAgent._get_template(),
            arguments=KernelArguments(settings=settings),
        )

    @staticmethod
    def _get_template():
        """Generate the instruction template for the LLM."""
        return """
            You are the Roaming Agent, responsible for managing roaming-related tasks.
            Your objective is to handle roaming inquiries and provide accurate information.
            Do not provide any personal or sensitive information.
            Ensure that you follow the provided instructions carefully.
        """

    async def process_message_async(
        self,
        message: str,
        message_id: str,
        thread_id: str,
        thread: ChatHistoryAgentThread,
        on_intermediate_response: Callable[..., None],
    ) -> tuple[str, AgentThread, str]:
        plugin = MCPStreamableHttpPlugin(
            name="RoamingPlugin",
            description="A plugin for handling roaming.",
            url="http://localhost:8002/roam/mcp",
            headers={
                "x-ms-message-id": message_id,
                "x-ms-conversation_id": thread_id,
            },
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
            result="Roaming agent response received.",
            agent_name=self.name,
        )

        _result = RoamingAgentResponse.model_validate(
            json.loads(_response.message.content),
        )

        await plugin.close()

        return _result.reply, _response.thread, self.name
