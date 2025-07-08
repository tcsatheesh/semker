"""
Base agent class for Semantic Kernel-based AI agents.

This module provides the abstract base class that all custom agents should inherit from.
It extends the ChatCompletionAgent from Semantic Kernel to provide a consistent interface
for message processing with intermediate response callbacks.
"""

from abc import abstractmethod
from typing import Any, Callable, Annotated, Optional

from pydantic import BaseModel
from semantic_kernel.agents import (
    AgentThread,
    ChatCompletionAgent,
    ChatHistoryAgentThread,
)


class AgentLLMResponse(BaseModel):
    """
    Response model for agent operations.

    Attributes:
        reply: The agent's response message to the user
        human_input_required: Whether additional human input is needed
        able_to_serve: Indicates if the agent can serve the request
    """

    reply: Annotated[str, "The agent's response message to the user"]
    human_input_required: Annotated[
        bool, "Does the agent require human input to proceed?"
    ]
    able_to_serve: Annotated[bool, "Was the agent able to serve the request?"]


class AgentResponse:
    """
    Extended response model for agent operations with thread details.

    This class adds a thread field and agent_name field to the base AgentResponse.

    Attributes:
        reply: The agent's response message to the user
        human_input_required: Whether additional human input is needed
        able_to_serve: Indicates if the agent can serve the request
        thread: The chat history thread for context
        agent_name: The name of the agent that processed the message
    """

    reply: Annotated[str, "The agent's response message to the user"]
    human_input_required: Annotated[
        bool, "Does the agent require human input to proceed?"
    ]
    able_to_serve: Annotated[bool, "Was the agent able to serve the request?"]
    thread: Annotated[AgentThread, "Chat history"]
    agent_name: Annotated[str, "Name of the agent that processed the message"]


class BaseAgent(ChatCompletionAgent):
    """
    Abstract base class for all custom agents in the system.

    This class extends Semantic Kernel's ChatCompletionAgent to provide a standardized
    interface for message processing with support for intermediate responses and
    thread management.

    All custom agents (billing, roaming, planner, etc.) should inherit from this class
    and implement the process_message_async method.
    """

    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the base agent.

        Args:
            *args: Variable length argument list passed to parent ChatCompletionAgent
            **kwargs: Arbitrary keyword arguments passed to parent ChatCompletionAgent
        """
        super().__init__(
            *args,
            **kwargs,
        )

    @abstractmethod
    async def process_message_async(
        self,
        message: str,
        message_id: str,
        thread_id: str,
        thread: ChatHistoryAgentThread,
        on_intermediate_response: Callable[..., None],
    ) -> AgentResponse:
        """
        Process a message asynchronously and return the response.

        This is an abstract method that must be implemented by all concrete agent classes.
        The method should handle the business logic specific to each agent type while
        providing intermediate updates through the callback function.

        Args:
            message: The user message to process
            message_id: Unique identifier for the message being processed
            thread_id: Unique identifier for the conversation thread
            thread: The chat history thread for maintaining conversation context
            on_intermediate_response: Callback function to send intermediate updates.
                                    Takes (message_id, status, result, agent_name) as parameters.

        Returns:
            A tuple containing:
                - str: The final response message
                - AgentThread: The updated thread after processing
                - str: The agent name that processed the message

        Raises:
            NotImplementedError: This is an abstract method and must be implemented
                               by concrete agent classes
        """
        pass  # This is an abstract method, no implementation here.
