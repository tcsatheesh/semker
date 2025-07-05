from abc import abstractmethod
from semantic_kernel.agents import ChatCompletionAgent


# Define an abstract class
class BaseAgent(ChatCompletionAgent):

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(
            *args,
            **kwargs,
        )

    @abstractmethod
    def process_message_async(
        self,
        message: str,
    ) -> str:
        pass  # This is an abstract method, no implementation here.
