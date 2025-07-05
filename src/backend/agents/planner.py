import json
from typing import cast


from pydantic import BaseModel

from semantic_kernel import Kernel
from semantic_kernel.agents import AgentThread, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings
from semantic_kernel.functions.kernel_arguments import KernelArguments

from agents.base import BaseAgent


from models.schemas import Message


class PlannerAgentResponse(BaseModel):
    reply: str
    agent_name: str


class PlannerAgent(BaseAgent):
    """Planner Agent for handling billing-related tasks."""

    def __init__(
        self,
        kernel: Kernel,
    ) -> None:

        settings = AzureChatPromptExecutionSettings()
        settings.response_format = PlannerAgentResponse
        settings.temperature = 0.0

        super().__init__(
            kernel=kernel,
            name="Planner",
            instructions=PlannerAgent._get_template(),
            arguments=KernelArguments(settings=settings),
        )

    @staticmethod
    def _get_template():
        """Generate the instruction template for the LLM."""
        return """
            You are the Planner Agent, responsible for planning tasks.
            You have access to the following agents:
            - Billing: Handles billing-related tasks.
            - Roaming: Manages roaming-related inquiries.
            - Broadband: Manages broadband-support-related inquiries.
            - Ticketing: Handles raising tickets tasks.
            Select one of the agents based on the user message.
            If you are unable to determine the appropriate agent, respond with a message indicating that you cannot assist.
            Your objective is to provide a clear and concise response to the user.
            Do not provide any personal or sensitive information.
            Ensure that you follow the provided instructions carefully.
        """

    async def process_message_async(
        self,
        message: str,
        message_id: str,
        thread_id: str,
        thread: ChatHistoryAgentThread,
        on_intermediate_response,
    ) -> tuple[str, AgentThread, str]:

        _response = await self.get_response(
            messages=message,
            thread=thread,
        )

        _result = PlannerAgentResponse.model_validate(
            json.loads(_response.message.content),
        )

        on_intermediate_response(
            message_id=message_id,
            status="Planner response recieved",
            result="Planner response processed successfully.",
        )

        _agent = None
        if _result.agent_name == "Billing":
            from agents.billing import BillingAgent

            _agent = BillingAgent(kernel=self.kernel)
        elif _result.agent_name == "Roaming":
            from agents.roaming import RoamingAgent

            _agent = RoamingAgent(kernel=self.kernel)

        if _agent:
            _thread = cast(
                ChatHistoryAgentThread,
                _response.thread,
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
