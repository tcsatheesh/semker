from abc import abstractmethod
from semantic_kernel.agents import ChatCompletionAgent, AgentThread, ChatHistoryAgentThread

from typing import Callable, Any

# Define an abstract class
class BaseAgent(ChatCompletionAgent):

    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
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
        """Process a message asynchronously and return the response."""
        pass  # This is an abstract method, no implementation here.
