"""
Planner Agent module for routing user requests to appropriate specialized agents.

This module provides the PlannerAgent class that acts as a router/orchestrator,
analyzing user messages and delegating them to the most appropriate specialized
agent (Billing, Roaming, Broadband, Ticketing, etc.) based on the content.
"""

import json
from typing import Callable, Optional, cast

from pydantic import BaseModel
from semantic_kernel import Kernel
from semantic_kernel.agents import AgentThread, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings
from semantic_kernel.functions.kernel_arguments import KernelArguments

from agents.base import BaseAgent
from config.constants import MessageStatus
from .config import Planner


class PlannerAgentResponse(BaseModel):
    """
    Response model for planner agent operations.
    
    Attributes:
        reply: The planner's response message to the user
        agent_name: The name of the specialized agent to handle the request
    """
    reply: str
    agent_name: str


class PlannerAgent(BaseAgent):
    """
    Planner Agent for routing user requests to appropriate specialized agents.
    
    This agent acts as an intelligent router that analyzes incoming user messages
    and determines which specialized agent (Billing, Roaming, Broadband, Ticketing)
    is best suited to handle the specific request. It provides a centralized
    entry point for multi-agent orchestration.
    
    The planner agent:
    - Analyzes user intent and message content
    - Routes requests to appropriate specialized agents
    - Handles cases where no suitable agent is available
    - Maintains conversation context through agent handoffs
    """

    def __init__(
        self,
        kernel: Kernel,
    ) -> None:
        """
        Initialize the Planner Agent.
        
        Args:
            kernel: The Semantic Kernel instance for AI operations
        """
        settings = AzureChatPromptExecutionSettings()
        settings.response_format = PlannerAgentResponse
        settings.temperature = 0.0

        super().__init__(
            kernel=kernel,
            name=Planner.AGENT_NAME,
            instructions=Planner.get_agent_template(),
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
        Process a message asynchronously by routing it to the appropriate agent.
        
        This method analyzes the user's message to determine the most suitable
        specialized agent, then either:
        1. Routes the message to the identified agent for processing
        2. Responds directly if no suitable agent is found
        
        Args:
            message: The user's message to process
            message_id: Unique identifier for the message
            thread_id: Unique identifier for the conversation thread
            thread: Chat history thread for context
            on_intermediate_response: Callback for intermediate status updates
        
        Returns:
            A tuple containing:
                - The final response message (from planner or delegated agent)
                - The updated thread after processing
                - The name of the agent that provided the final response
        
        Raises:
            Exception: If there are issues with agent instantiation or processing
        """
        _response = await self.get_response(
            messages=message,
            thread=thread,
        )

        _result = PlannerAgentResponse.model_validate(
            json.loads(_response.message.content),
        )

        on_intermediate_response(
            message_id=message_id,
            status=MessageStatus.IN_PROGRESS,
            result="Planner agent response received.",
            agent_name=self.name,
        )

        _agent: Optional[BaseAgent] = None
        if _result.agent_name == "Billing":
            from agents.billing import BillingAgent

            _agent = BillingAgent(kernel=self.kernel)
        elif _result.agent_name == "Roaming":
            from agents.roaming import RoamingAgent

            _agent = RoamingAgent(kernel=self.kernel)
        elif _result.agent_name == "Tariff":
            from agents.tariff import TariffAgent

            _agent = TariffAgent(kernel=self.kernel)

        if _agent:
            _thread = cast(
                ChatHistoryAgentThread,
                _response.thread,
            )
            on_intermediate_response(
                message_id=message_id,
                status=MessageStatus.IN_PROGRESS,
                result=f"Planner agent routing to {_result.agent_name} agent.",
                agent_name=self.name,
            )
            _inner_response, _inner_thread, _agent_name = await _agent.process_message_async(
                message=message,
                message_id=message_id,
                thread_id=thread_id,
                thread=_thread,
                on_intermediate_response=on_intermediate_response,
            )
            return _inner_response, _inner_thread, _agent_name

        else:
            return _result.reply, _response.thread, self.name
