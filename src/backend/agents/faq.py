"""
Faq Agent module for handling faq-related tasks and inquiries.

This module provides the FaqAgent class that specializes in processing
faq-related user requests through the Model Context Protocol (MCP)
and Semantic Kernel framework.
"""

import json
from typing import Callable, Final

from semantic_kernel import Kernel
from semantic_kernel.agents import AgentThread, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings
from semantic_kernel.connectors.mcp import MCPStreamableHttpPlugin
from semantic_kernel.functions.kernel_arguments import KernelArguments

from agents.base import BaseAgent, AgentLLMResponse, AgentResponse
from config.constants import MessageStatus
from .config import Services, Headers

class Faq:
    """Faq agent-specific configuration settings."""

    # Agent identity
    AGENT_NAME: Final[str] = "FAQ"
    PLUGIN_NAME: Final[str] = "FaqPlugin"
    PLUGIN_DESCRIPTION: Final[str] = "A plugin for handling frequently asked questions."

    # Service endpoint
    @classmethod
    def get_mcp_endpoint(cls) -> str:
        """Get the MCP endpoint for faq service."""
        return Services.FAQ_MCP_SERVER_URL

    # Agent template
    # AGENT_TEMPLATE: Final[
    #     str
    # ] = """
    #     You are the Faq Agent, responsible for answering frequently asked questions.
    #     Your objective is to handle faq inquiries and provide accurate information.
    #     Do not provide any personal or sensitive information.
    #     Ensure that you follow the provided instructions carefully.
    # """
    AGENT_TEMPLATE: Final[
        str
    ] = """
        You are the Faq Agent, responsible for handling frequently asked questions (FAQs) across supported domains (e.g., roaming, tariffs, billing).

        🎯 Your primary goals:
        - Handle general, factual questions that do NOT require user-specific data or tool-enabled actions.
        - Provide clear, accurate, and context-relevant information.
        - Follow strict reasoning logic before giving any answer.

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
    """


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
        settings.response_format = AgentLLMResponse
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
    ) -> AgentResponse:
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
