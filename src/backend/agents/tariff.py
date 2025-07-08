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
    # AGENT_TEMPLATE: Final[
    #     str
    # ] = """
    #     You are the Tariff Agent, responsible for managing tariff-related tasks.
    #     Your objective is to handle tariff inquiries and provide accurate information.
    #     Do not provide any personal or sensitive information.
    #     Provide tariff information is a tabular format.
    #     When comparing tariffs, ensure you provide the most relevant and up-to-date information in a table format.
    #     If the tariff data is not available, inform the user that you cannot access it.
    #     Ensure that you follow the provided instructions carefully.
    # """
    AGENT_TEMPLATE: Final[
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

        🧠 Chain-of-Thought Approach (Mandatory):
        You MUST respond using this step-by-step format:

        🔎 Step 1: Analyze the user query.
        → Break it into components and identify whether it’s a general FAQ.

        🧩 Step 2: Decide what information is required.
        → Identify conceptual, procedural, or policy-level data needed to respond.

        🧪 Step 3: Determine whether tool access is required.
        → If YES → Exit cleanly. Tool use is NOT permitted.
        → If NO → Proceed with static explanation.

        📨 Step 4: Respond clearly and accurately.
        → Use domain knowledge only.
        → Do NOT guess or interpolate data.
        → Do NOT reference tools, help pages, or customer support.

        🎯 Final Answer:
        → Present response in a concise, well-structured format, using stepwise explanation when helpful.
        → All tariff information should be presented in a table format and MUST be preceeded by briefly describing what the table contains, with clear headings for each column.

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

        async for _response in self.invoke(messages=message, thread=thread):
            _result = AgentLLMResponse.model_validate(
                json.loads(_response.message.content),
            )
            on_intermediate_response(
                message_id=message_id,
                status=MessageStatus.IN_PROGRESS,
                result="\n".join(_result.steps),
                agent_name=self.name,
            )

        _result = AgentLLMResponse.model_validate(
                json.loads(_response.message.content),
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
