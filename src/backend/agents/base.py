"""
Base agent class for Semantic Kernel-based AI agents.

This module provides the abstract base class that all custom agents should inherit from.
It extends the ChatCompletionAgent from Semantic Kernel to provide a consistent interface
for message processing with intermediate response callbacks.
"""

from abc import abstractmethod
from typing import Any, Callable

from semantic_kernel.agents import AgentThread, ChatCompletionAgent, ChatHistoryAgentThread


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
    ) -> tuple[str, AgentThread, str]:
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
