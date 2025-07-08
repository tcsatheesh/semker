"""
Faq Agent module for handling faq-related tasks and inquiries.

This module provides the FaqAgent class that specializes in processing
faq-related user requests through the Model Context Protocol (MCP)
and Semantic Kernel framework.
"""

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
from .config import Faq, Headers


class FaqAgentResponse(BaseModel):
    """
    Response model for faq agent operations.
    
    Attributes:
        reply: The agent's response message to the user
        human_input_required: Whether additional human input is needed
    """
    reply: str
    human_input_required: bool


class FaqAgent(BaseAgent):
    """
    Faq Agent for handling faq-related tasks and inquiries.
    
    This agent specializes in processing faq-related requests by connecting
    to a faq service through MCP (Model Context Protocol) and providing
    accurate faq information while maintaining security and privacy.
    
    The agent is configured with specific instructions to:
    - Handle faq inquiries professionally
    - Protect sensitive information
    - Provide clear responses when data is unavailable
    """

    def __init__(
        self,
        kernel: Kernel,
    ) -> None:
        """
        Initialize the Faq Agent.
        
        Args:
            kernel: The Semantic Kernel instance for AI operations
        """
        settings = AzureChatPromptExecutionSettings()
        settings.response_format = FaqAgentResponse
        settings.temperature = 0.0

        super().__init__(
            kernel=kernel,
            name=Faq.AGENT_NAME,
            instructions=Faq.AGENT_TEMPLATE,
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
        """
        Process a faq-related message asynchronously.
        
        This method handles faq inquiries by:
        1. Connecting to the faq service via MCP plugin
        2. Processing the user's message through the AI model
        3. Providing intermediate status updates
        4. Returning the final faq response
        
        Args:
            message: The user's faq-related message
            message_id: Unique identifier for the message
            thread_id: Unique identifier for the conversation thread
            thread: Chat history thread for context
            on_intermediate_response: Callback for intermediate status updates
        
        Returns:
            A tuple containing:
                - The agent's final response message
                - The updated thread after processing
                - The agent name ("Faq")
        
        Raises:
            Exception: If there are issues connecting to the faq service
                      or processing the request
        """
        plugin = MCPStreamableHttpPlugin(
            name=Faq.PLUGIN_NAME,
            description=Faq.PLUGIN_DESCRIPTION,
            url=Faq.get_mcp_endpoint(),
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
            result="Faq agent response received.",
            agent_name=self.name,
        )

        _result: FaqAgentResponse = FaqAgentResponse.model_validate(
            json.loads(_response.message.content),
        )

        await plugin.close()

        return _result.reply, _response.thread, self.name
