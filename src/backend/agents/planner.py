"""
Planner Agent module for routing user requests to appropriate specialized agents.

This module provides the PlannerAgent class that acts as a router/orchestrator,
analyzing user messages and delegating them to the most appropriate specialized
agent (Billing, Roaming, Broadband, Ticketing, etc.) based on the content.
"""

import json
from typing import Callable, Optional, cast, Final, List, Dict, Annotated

from pydantic import BaseModel
from semantic_kernel import Kernel
from semantic_kernel.agents import AgentThread, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings
from semantic_kernel.functions.kernel_arguments import KernelArguments

from agents.base import BaseAgent
from config.constants import MessageStatus


class Planner:
    """Planner agent-specific configuration settings."""

    # Agent identity
    AGENT_NAME: Final[str] = "Planner"

    # Available agents for routing
    AVAILABLE_AGENTS: Final[List[Dict[str, str]]] = [
        {"Billing": "Handles billing-related tasks."},
        {"Roaming": "Manages roaming-related inquiries."},
        {"Tariff": "Handles tariff-related inquiries."},
        {"Faq": "Provides answers to frequently asked questions."},
    ]

    # Agent template (raw template with placeholder)
    # _AGENT_TEMPLATE: Final[
    #     str
    # ] = """
    #     You are the Planner Agent, responsible for planning tasks.
    #     You have access to the following agents:
    #     {available_agents}
    #     Select one of the agents based on the user message.
    #     If you are unable to determine the appropriate agent, respond with a message indicating that you cannot assist.
    #     Your objective is to provide a clear and concise response to the user.
    #     Do not provide any personal or sensitive information.
    #     Show your reasoning. Explain your thought process before answering.
    #     Ensure that you follow the provided instructions carefully.
    # """

    _AGENT_TEMPLATE: Final[
        str
    ] = """
        You are a Planner Agent that orchestrates specialized sub-agents to complete complex tasks across domains (e.g., Telecom, AI orchestration, music theory, etc.). You must:

        List of Available Agents:
        {available_agents}

        1. Break down the user’s request into stepwise components.
        2. Show your thought process (“chain of thought”) progressively before executing subtasks.
        3. Share intermediate updates after each planning step.
        4. Invoke sub-agents only when necessary.
        5. Deliver a final synthesized response only after all relevant steps are completed.

        🧩 Key Behavior Rules:
        - You MUST show reasoning before action.
        - You MUST share progress updates before delivering the final answer.
        - You MAY only use sub-agents when they are needed to complete a step.
        - You MAY reuse results from previous steps if helpful.
        - You MUST produce a final answer summarizing all delegated subtasks and decisions.

        🎯 Prompt Template Logic:
            Step 1: Analyze the request and list necessary sub-goals. → [Reasoning Step 1 Output]
            Step 2: Determine which sub-agent(s) are needed. → [Reasoning Step 2 Output]
            Step 3: Describe what you expect from each sub-agent. → [Reasoning Step 3 Output]
            Step 4: Call sub-agent(s) and await response. → [Intermediate Update: Sub-agent response summaries]
            Step 5: Integrate all sub-agent inputs into a coherent final output. → [Reasoning Step 5 Output]
            Final Answer: → [Synthesized response using all results]
        """

    @classmethod
    def get_agent_template(cls) -> str:
        """Get the formatted planner agent template with available agents.

        Returns:
            Formatted template string with available agents list
        """
        agents_list = "\n        ".join(f"- {agent}" for agent in cls.AVAILABLE_AGENTS)
        return cls._AGENT_TEMPLATE.format(available_agents=agents_list)


class PlannerAgentResponse(BaseModel):
    """
    Response model for planner agent operations.

    Attributes:
        reply: The planner's response message to the user
        agent_name: The name of the specialized agent to handle the request
    """
    steps: Annotated[Optional[List[str]], "The chain of thoughts or steps taken to process the request"]
    reply: Annotated[str, "The agent's response message to the user"]
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
        async for _response in self.invoke(messages=message, thread=thread):
            _result = PlannerAgentResponse.model_validate(
                json.loads(_response.message.content),
            )

            on_intermediate_response(
                message_id=message_id,
                status=MessageStatus.IN_PROGRESS,
                result="\n".join(_result.steps),
                agent_name=self.name,
            )

        _result = PlannerAgentResponse.model_validate(
                json.loads(_response.message.content),
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
        elif _result.agent_name == "Faq":
            from agents.faq import FaqAgent

            _agent = FaqAgent(kernel=self.kernel)

        if _agent:
            _thread = cast(
                ChatHistoryAgentThread,
                _response.thread,
            )
            on_intermediate_response(
                message_id=message_id,
                status=MessageStatus.IN_PROGRESS,
                result=_result.reply,
                agent_name=self.name,
            )
            _inner_response = await _agent.process_message_async(
                message=message,
                message_id=message_id,
                thread_id=thread_id,
                thread=_thread,
                on_intermediate_response=on_intermediate_response,
            )
            # if _inner_response.able_to_serve is False:
            #     on_intermediate_response(
            #         message_id=message_id,
            #         status=MessageStatus.IN_PROGRESS,
            #         result=f"{_result.agent_name} agent unable to serve the request, looking for another agent.",
            #         agent_name=self.name,
            #     )

            #     _planner_second_pass = await self.get_response(
            #         messages=message,
            #         thread=_inner_response.thread,
            #     )
            #     _planner_second_pass_response = PlannerAgentResponse.model_validate(
            #         json.loads(_planner_second_pass.message.content),
            #     )

            #     return (
            #         _planner_second_pass_response.reply,
            #         _planner_second_pass.thread,
            #         self.name,
            #     )

            return (
                _inner_response.reply,
                _inner_response.thread,
                _inner_response.agent_name,
            )

        else:
            return _result.reply, _response.thread, self.name
