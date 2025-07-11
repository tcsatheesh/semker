"""
Roaming Agent module for handling roaming-related tasks and inquiries.

This module provides the RoamingAgent class that specializes in processing
roaming-related user requests through the Model Context Protocol (MCP)
and Semantic Kernel framework. The agent focuses on providing accurate
roaming rate information and coverage details for international travel.

Classes:
    Roaming: Configuration class containing agent settings and templates
    RoamingAgent: Main agent class for processing roaming inquiries

Features:
    - MCP integration with roaming rate services
    - Country-specific roaming rate retrieval
    - Chain-of-thought reasoning for transparency
    - Real-time intermediate response updates
    - Secure data handling and validation
    - Professional roaming information presentation

Example:
    ```python
    agent = RoamingAgent(kernel)
    response = await agent.process_message_async(
        message="What are the roaming rates for Spain?",
        message_id="msg-123",
        thread_id="thread-456",
        thread=thread,
        on_intermediate_response=callback
    )
    ```
"""

import json
from typing import Callable, Final

from semantic_kernel import Kernel
from semantic_kernel.agents import AgentThread, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings
from semantic_kernel.connectors.mcp import MCPStreamableHttpPlugin
from semantic_kernel.functions.kernel_arguments import KernelArguments

from agents.base import BaseAgent, AgentResponse, AgentLLMResponse
from config.constants import MessageStatus
from .config import Services, Headers


class Roaming:
    """
    Configuration class for the Roaming Agent.

    This class contains all configuration settings, constants, and templates
    needed for the Roaming Agent to function properly. It provides centralized
    configuration for roaming rate queries, MCP endpoint management, and
    agent behavior instructions.

    Class Attributes:
        AGENT_NAME: The identifier name for this agent
        PLUGIN_NAME: The name of the MCP plugin for roaming services
        PLUGIN_DESCRIPTION: Description of the plugin functionality
        AGENT_TEMPLATE: Comprehensive instructions for roaming-specific behavior

    Methods:
        get_mcp_endpoint: Returns the MCP server endpoint for roaming services

    Features:
        - Country-specific roaming rate retrieval
        - Month-based rate queries for billing cycles
        - Chain-of-thought reasoning for transparency
        - Tool-based data validation to prevent errors
        - Professional presentation of roaming information
    """

    # Agent identity
    AGENT_NAME: Final[str] = "Roaming"
    PLUGIN_NAME: Final[str] = "RoamingPlugin"
    PLUGIN_DESCRIPTION: Final[str] = "A plugin for handling roaming."

    # Service endpoint
    @classmethod
    def get_mcp_endpoint(cls) -> str:
        """
        Get the MCP endpoint URL for the roaming service.

        Returns:
            str: The complete URL endpoint for the roaming MCP server

        Note:
            This method retrieves the endpoint from the Services configuration
            which can be customized via environment variables for different
            deployment environments.
        """
        
        return Services.ROAMING_MCP_SERVER_URL

    # Agent template
    # AGENT_TEMPLATE: Final[
    #     str
    # ] = """
    #     You are the Roaming Agent, responsible for managing roaming-related tasks.
    #     Your objective is to handle roaming inquiries and provide accurate information.
    #     You *MUST* only respond with information obtained from the tools you have access to.
    #     If the roaming data is not available, respond that you cannot answer this query.
    #     Do not provide any personal or sensitive information.
    #     Ensure that you follow the provided instructions carefully.
    # """
    AGENT_TEMPLATE: Final[
        str
    ] = """
        You are a Roaming Agent specializing in telecom billing and coverage abroad. Your responsibility is to handle user queries specifically about **standard roaming rates per country and month**, using factual tool-based responses only.

        You are equipped with one tool:

        🧰 Tool Access:
        - `get_roaming_rate(country: str, month: str) → rate_info`: Returns the standard roaming rate (voice, SMS, data) for the specified country and billing month. If data is unavailable, this tool returns a null or error response.

        🔗 Your Behavioral Protocol:
        You must follow a **chain-of-thought response structure** — reasoning out loud in stepwise format — and produce intermediate updates before issuing your final answer.

        ⛔ If the tool cannot provide data (e.g., unsupported country or missing rates), you must:
        - Clearly state that the data isn’t available.
        - Do NOT suggest escalation to support or link out.
        - Do NOT guess or interpolate static pricing.
        - Do NOT offer fallback roaming advice.

        ---

        ### 🧠 Response Template for Roaming Rate Requests
        🔎 Step 1: Interpret the user’s question. → Identify the target country and month.

        🧩 Step 2: Confirm that the query is about standard rates (not account-specific usage).

        🧪 Step 3: Call the get_roaming_rate tool with provided country and month.

        📨 Step 4: Handle the tool output: → If valid: summarize voice/SMS/data rate info. → If null or error: state that rate info is unavailable for the requested input.

        🎯 Final Answer: → Present only the verified data returned from the tool. No assumptions. No generic advice.
        → Present response in a concise, well-structured format, using stepwise explanation when helpful.
        → All roaming information should be presented in a table format and MUST be preceeded by briefly describing what the table contains, with clear headings for each column.
    """

class RoamingAgent(BaseAgent):
    """
    Roaming Agent for handling roaming-related tasks and inquiries.
    
    This agent specializes in processing roaming-related requests by connecting
    to a roaming service through MCP (Model Context Protocol) and providing
    accurate roaming information while maintaining security and privacy.
    
    The agent is configured with specific instructions to:
    - Handle roaming inquiries professionally
    - Protect sensitive information
    - Provide clear responses when data is unavailable
    """

    def __init__(
        self,
        kernel: Kernel,
    ) -> None:
        """
        Initialize the Roaming Agent.
        
        Args:
            kernel: The Semantic Kernel instance for AI operations
        """
        settings = AzureChatPromptExecutionSettings()
        settings.response_format = AgentLLMResponse
        settings.temperature = 0.0

        super().__init__(
            kernel=kernel,
            name=Roaming.AGENT_NAME,
            instructions=Roaming.AGENT_TEMPLATE,
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
        """
        Process a roaming-related message asynchronously.
        
        This method handles roaming inquiries by:
        1. Connecting to the roaming service via MCP plugin
        2. Processing the user's message through the AI model
        3. Providing intermediate status updates
        4. Returning the final roaming response
        
        Args:
            message: The user's roaming-related message
            message_id: Unique identifier for the message
            thread_id: Unique identifier for the conversation thread
            thread: Chat history thread for context
            on_intermediate_response: Callback for intermediate status updates
        
        Returns:
            A tuple containing:
                - The agent's final response message
                - The updated thread after processing
                - The agent name ("Roaming")
        
        Raises:
            Exception: If there are issues connecting to the roaming service
                      or processing the request
        """
        plugin = MCPStreamableHttpPlugin(
            name=Roaming.PLUGIN_NAME,
            description=Roaming.PLUGIN_DESCRIPTION,
            url=Roaming.get_mcp_endpoint(),
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
