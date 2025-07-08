"""
Billing Agent module for handling billing-related tasks and inquiries.

This module provides the BillingAgent class that specializes in processing
billing-related user requests through the Model Context Protocol (MCP)
and Semantic Kernel framework.
"""

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
from agents.config import Services, Headers



class Billing:
    """Billing agent-specific configuration settings."""

    # Agent identity
    AGENT_NAME: Final[str] = "Billing"
    PLUGIN_NAME: Final[str] = "BillingPlugin"
    PLUGIN_DESCRIPTION: Final[str] = "A plugin for handling billing."

    # Service endpoint
    @classmethod
    def get_mcp_endpoint(cls) -> str:
        """Get the MCP endpoint for billing service."""
        return Services.BILLING_MCP_SERVER_URL

    # Agent template
    AGENT_TEMPLATE: Final[
        str
    ] = """
        You are the Billing Agent, responsible for managing billing-related tasks.
        Your objective is to handle billing inquiries and provide accurate information.
        Do not provide any personal or sensitive information.
        If the billing data is not available, inform the user that you cannot access it.
        Use a tabular format to present billing information clearly.
        Ensure that you follow the provided instructions carefully.
    """

class BillingAgent(BaseAgent):
    """
    Billing Agent for handling billing-related tasks and inquiries.
    
    This agent specializes in processing billing-related requests by connecting
    to a billing service through MCP (Model Context Protocol) and providing
    accurate billing information while maintaining security and privacy.
    
    The agent is configured with specific instructions to:
    - Handle billing inquiries professionally
    - Protect sensitive information
    - Provide clear responses when data is unavailable
    """

    def __init__(
        self,
        kernel: Kernel,
    ) -> None:
        """
        Initialize the Billing Agent.
        
        Args:
            kernel: The Semantic Kernel instance for AI operations
        """
        settings = AzureChatPromptExecutionSettings()
        settings.response_format = AgentLLMResponse
        settings.temperature = 0.0

        super().__init__(  # type: ignore
            kernel=kernel,
            name=Billing.AGENT_NAME,
            instructions=Billing.AGENT_TEMPLATE,
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
        Process a billing-related message asynchronously.
        
        This method handles billing inquiries by:
        1. Connecting to the billing service via MCP plugin
        2. Processing the user's message through the AI model
        3. Providing intermediate status updates
        4. Returning the final billing response
        
        Args:
            message: The user's billing-related message
            message_id: Unique identifier for the message
            thread_id: Unique identifier for the conversation thread
            thread: Chat history thread for context
            on_intermediate_response: Callback for intermediate status updates
        
        Returns:
            A tuple containing:
                - The agent's final response message
                - The updated thread after processing
                - The agent name ("Billing")
        
        Raises:
            Exception: If there are issues connecting to the billing service
                      or processing the request
        """
        plugin = MCPStreamableHttpPlugin(
            name=Billing.PLUGIN_NAME,
            description=Billing.PLUGIN_DESCRIPTION,
            url=Billing.get_mcp_endpoint(),
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
