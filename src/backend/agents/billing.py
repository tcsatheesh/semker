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


class BillingAgentResponse(BaseModel):
    reply: str
    human_input_required: bool


class BillingAgent(BaseAgent):
    """Billing Agent for handling billing-related tasks."""

    def __init__(
        self,
        kernel: Kernel,
    ) -> None:

        settings = AzureChatPromptExecutionSettings()
        settings.response_format = BillingAgentResponse
        settings.temperature = 0.0

        super().__init__( # type: ignore
            kernel=kernel,
            name="Billing",
            instructions=BillingAgent._get_template(),
            arguments=KernelArguments(settings=settings),
        )

    @staticmethod
    def _get_template():
        """Generate the instruction template for the LLM."""
        return """
            You are the Billing Agent, responsible for managing billing-related tasks.
            Your objective is to handle billing inquiries and provide accurate information.
            Do not provide any personal or sensitive information.
            If the billing data is not available, inform the user that you cannot access it.
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
            name="BillingPlugin",
            description="A plugin for handling billing.",
            url="http://localhost:8002/bill/mcp",
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
            result="Billing Agent response received.",
            agent_name=self.name,
        )

        _result: BillingAgentResponse = BillingAgentResponse.model_validate(
            json.loads(_response.message.content),
        )

        await plugin.close()

        return _result.reply, _response.thread, self.name
