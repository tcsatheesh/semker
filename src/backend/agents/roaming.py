"""
Roaming Agent module for handling roaming-related tasks and inquiries.

This module provides the RoamingAgent class that specializes in processing
roaming-related user requests through the Model Context Protocol (MCP)
and Semantic Kernel framework.
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
    """Roaming agent-specific configuration settings."""

    # Agent identity
    AGENT_NAME: Final[str] = "Roaming"
    PLUGIN_NAME: Final[str] = "RoamingPlugin"
    PLUGIN_DESCRIPTION: Final[str] = "A plugin for handling roaming."

    # Service endpoint
    @classmethod
    def get_mcp_endpoint(cls) -> str:
        """Get the MCP endpoint for roaming service."""
        
        return Services.ROAMING_MCP_SERVER_URL

    # Agent template
    AGENT_TEMPLATE: Final[
        str
    ] = """
        You are the Roaming Agent, responsible for managing roaming-related tasks.
        Your objective is to handle roaming inquiries and provide accurate information.
        You *MUST* only respond with information obtained from the tools you have access to.
        If the roaming data is not available, respond that you cannot answer this query.
        Do not provide any personal or sensitive information.
        Ensure that you follow the provided instructions carefully.
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
