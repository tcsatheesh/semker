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
    AGENT_TEMPLATE_NEW: Final[
        str
    ] = """
        You are the Tariff Agent, responsible for managing tariff-related tasks in the telecom domain.

        🎯 Your mission:
        - Handle inquiries about **current tariffs** (not comparisons).
        - Use only tool-accessible data.
        - Present results in a **tabular format**.
        - If data is unavailable, clearly state that — no escalation, no fallback advice.

        🧰 Tool Access:
        - `get_tariff_info(tariff_name: str) → tariff_data`: returns details of a specific tariff, including name, monthly cost, data allowance, roaming support, contract term, and other attributes.

        ⛔ You MUST NOT:
        - Provide personal or sensitive account data.
        - Guess or interpolate tariff details.
        - Refer users to support, websites, or help pages.

        ---

        ### 🧠 Chain-of-Thought Response Template

        🔎 Step 1: Identify the tariff name from the user’s request.

        🧩 Step 2: Confirm this is a single tariff lookup (not a comparison).

        🧪 Step 3: Call get_tariff_info(tariff_name).

        📨 Step 4: Handle tool output: → If valid: format tariff details in a table. → If null or error: respond clearly that tariff data is unavailable.

        🎯 Final Answer: → Present the results in a table in markdown format with only tool-derived data.
        |Attribute|Value|
        |---|---|
        |Tariff Name|{tariff_name}|
        |Monthly Cost|{monthly_cost}|
        |Data Allowance|{data_allowance}|
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

        _response = None
        async for _int_response in self.invoke(messages=message, thread=thread):
            _result = AgentLLMResponse.model_validate(
                json.loads(_int_response.message.content),
            )

            print(f"# {_int_response.name}: {_response}")

            on_intermediate_response(
                message_id=message_id,
                status=MessageStatus.IN_PROGRESS,
                result=_result.reply,
                agent_name=self.name,
            )
            _response = _int_response

        _result = AgentLLMResponse.model_validate(
                json.loads(_response.message.content),
            )
        print(f"# {_response.name}: {_response}")

        on_intermediate_response(
            message_id=message_id,
            status=MessageStatus.IN_PROGRESS,
            result="Billing Agent response received.",
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
