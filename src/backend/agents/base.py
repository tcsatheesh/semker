"""
Base agent class for Semantic Kernel-based AI agents.

This module provides the abstract base class that all custom agents should inherit from.
It extends the ChatCompletionAgent from Semantic Kernel to provide a consistent interface
for message processing with intermediate response callbacks.
"""

from abc import abstractmethod
from typing import Any, Callable, Annotated, Optional, List

from pydantic import BaseModel
from semantic_kernel.agents import (
    AgentThread,
    ChatCompletionAgent,
    ChatHistoryAgentThread,
)


class AgentLLMResponse(BaseModel):
    """
    Pydantic model for structured agent LLM responses.

    This model represents the structured response from an AI agent's language model,
    including the thought process, final reply, and metadata about the interaction.
    It's used for parsing and validating agent responses before they are returned
    to the message processor.

    Attributes:
        steps: Optional list of reasoning steps or thought process taken by the agent
        reply: The agent's final response message to the user
        human_input_required: Whether the agent needs additional human input to proceed
        able_to_serve: Whether the agent was able to successfully serve the user's request

    Example:
        ```python
        response = AgentLLMResponse(
            steps=["Analyzed user query", "Retrieved billing data", "Formatted response"],
            reply="Your current bill is £45.50",
            human_input_required=False,
            able_to_serve=True
        )
        ```
    """
    steps: Annotated[Optional[List[str]], "The chain of thoughts or steps taken to process the request"]
    reply: Annotated[str, "The agent's response message to the user"]
    human_input_required: Annotated[
        bool, "Does the agent require human input to proceed?"
    ]
    able_to_serve: Annotated[bool, "Was the agent able to serve the request?"]


class AgentResponse:
    """
    Extended response model for agent operations with thread management.

    This class represents the complete response from an agent after processing
    a message, including the response content, metadata, and conversation context.
    It extends the basic response model to include thread management for
    maintaining conversation history.

    Attributes:
        reply: The agent's final response message to the user
        human_input_required: Whether the agent needs additional human input to proceed
        able_to_serve: Whether the agent was able to successfully serve the user's request
        thread: The updated chat history thread with conversation context
        agent_name: The name/identifier of the agent that processed the message

    Usage:
        This class is typically returned by the process_message_async method
        of concrete agent implementations and contains all necessary information
        for the message processor to update the conversation state.

    Example:
        ```python
        response = AgentResponse()
        response.reply = "Your bill is £45.50"
        response.human_input_required = False
        response.able_to_serve = True
        response.thread = updated_thread
        response.agent_name = "BillingAgent"
        ```
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
    Abstract base class for all custom AI agents in the Semker system.

    This class extends Semantic Kernel's ChatCompletionAgent to provide a standardized
    interface for message processing with support for intermediate responses, thread
    management, and conversation context preservation. All specialized agents (billing,
    roaming, tariff, FAQ, planner) inherit from this class.

    The BaseAgent provides:
    - Consistent interface for message processing
    - Thread management for conversation context
    - Intermediate response callbacks for real-time updates
    - Error handling and validation patterns
    - Integration with Semantic Kernel framework

    Abstract Methods:
        process_message_async: Must be implemented by all concrete agent classes
                              to handle domain-specific message processing logic.

    Usage:
        This class should not be instantiated directly. Instead, create concrete
        implementations that inherit from BaseAgent and implement the required
        abstract methods.

    Example:
        ```python
        class CustomAgent(BaseAgent):
            async def process_message_async(self, message, message_id, thread_id, 
                                          thread, on_intermediate_response):
                # Custom implementation here
                return response
        ```
    """

    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the base agent with Semantic Kernel ChatCompletionAgent.

        This constructor forwards all arguments to the parent ChatCompletionAgent
        class, allowing flexible initialization of the underlying Semantic Kernel
        agent with custom configurations, models, and settings.

        Args:
            *args: Variable length argument list passed to parent ChatCompletionAgent.
                  Typically includes service configuration and agent settings.
            **kwargs: Arbitrary keyword arguments passed to parent ChatCompletionAgent.
                     Common kwargs include name, description, instructions, and
                     execution_settings for the underlying AI model.

        Example:
            ```python
            agent = ConcreteAgent(
                name="BillingAgent",
                description="Handles billing inquiries",
                instructions="You are a billing specialist...",
                kernel=kernel,
                service_id="chat-service"
            )
            ```
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
        Process a user message asynchronously and return the structured response.

        This is the core abstract method that must be implemented by all concrete
        agent classes. It handles the domain-specific business logic for processing
        user messages while providing real-time updates through the callback function.

        The method should:
        1. Analyze the user message within the conversation context
        2. Perform domain-specific processing (e.g., data retrieval, calculations)
        3. Send intermediate updates via the callback function
        4. Generate and return the final structured response
        5. Update the conversation thread with the interaction

        Args:
            message: The user's message content to process
            message_id: Unique identifier for tracking this specific message
            thread_id: Unique identifier for the conversation thread
            thread: The chat history thread containing conversation context
            on_intermediate_response: Callback function for sending real-time updates.
                                    Should be called with (message_id, status, result, agent_name)

        Returns:
            AgentResponse: A tuple containing:
                - str: The final response message for the user
                - AgentThread: The updated thread after processing
                - str: The agent name that processed the message

        Raises:
            NotImplementedError: This is an abstract method that must be implemented
                               by all concrete agent classes
            Exception: Implementation-specific exceptions should be handled by
                      concrete implementations and converted to appropriate responses

        Example Implementation:
            ```python
            async def process_message_async(self, message, message_id, thread_id, 
                                          thread, on_intermediate_response):
                # Send initial update
                on_intermediate_response(message_id, "processing", 
                                       "Analyzing request...", self.name)
                
                # Process the message
                result = await self._process_domain_logic(message)
                
                # Send final update
                on_intermediate_response(message_id, "completed", 
                                       result, self.name)
                
                # Return structured response
                return (result, updated_thread, self.name)
            ```
        """
        pass  # This is an abstract method, no implementation here.
