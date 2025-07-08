"""
Billing Agent module for handling billing-related tasks and inquiries.

This module provides the BillingAgent class that specializes in processing
billing-related user requests through the Model Context Protocol (MCP)
and Semantic Kernel framework.
"""

import json
from typing import Callable, Final

from pydantic import BaseModel
from semantic_kernel import Kernel
from semantic_kernel.agents import AgentThread, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings
from semantic_kernel.connectors.mcp import MCPStreamableHttpPlugin
from semantic_kernel.functions.kernel_arguments import KernelArguments

from agents.base import BaseAgent, AgentResponse, AgentLLMResponse
from config.constants import MessageStatus
from agents.config import Services, Headers



class Billing:
    """Billing agent-specific configuration settings."""

    # Agent identity
    AGENT_NAME: Final[str] = "Billing"
    PLUGIN_NAME: Final[str] = "BillingPlugin"
    PLUGIN_DESCRIPTION: Final[str] = "A plugin for handling billing."

    # Service endpoint
    @classmethod
    def get_mcp_endpoint(cls) -> str:
        """Get the MCP endpoint for billing service."""
        return Services.BILLING_MCP_SERVER_URL

    # Agent template
    # AGENT_TEMPLATE: Final[
    #     str
    # ] = """
    #     You are the Billing Agent, responsible for managing billing-related tasks.
    #     Your objective is to handle billing inquiries and provide accurate information.
    #     Do not provide any personal or sensitive information.
    #     If the billing data is not available, inform the user that you cannot access it.
    #     Use a tabular format to present billing information clearly.
    #     Ensure that you follow the provided instructions carefully.
    # """
    AGENT_TEMPLATE: Final[
        str
    ] = """
        You are a Billing Agent for telecom users. Your job is to analyze billing-related questions using structured, step-by-step reasoning. You ONLY respond using verified data from tools like `get_billing_data`. If the information needed for a step is unavailable via tools, you must clearly state that you cannot proceed — with no further redirection or links.

        🧠 Tool Access:
        - `get_billing_data`: retrieves user-specific billing details for the current cycle, including plan charges, roaming usage, overage fees, and payments.

        🔄 Workflow Requirements:
        You MUST follow a chain-of-thought approach:
        1. Analyze the user request and break it into steps.
        2. Decide what information you need for each step.
        3. Determine if tool access is sufficient.
        4. If YES → Proceed and show intermediate steps.
        5. If NO → Exit clearly and respectfully without providing a workaround or external reference but ask the user for missing info if required.

        🚫 DO NOT:
        - Answer based on assumptions, prior static knowledge, or examples.
        - Refer the user to customer support, websites, or help guides.
        - Guess billing breakdowns or interpolate missing data.

        ---

        🎯 Example User Query:
        > "Can you explain why my last bill had an unexpected £20 fee?"

        🧭 Chain-of-Thought Response (Template):
            🔎 Step 1: The user wants to understand the source of a £20 fee in the last billing cycle.

            ➡️ I need to:

                 A. Retrieve last cycle's billing breakdown.

                 B. Identify any unusual charges (e.g., overages, roaming, late fees).

            🧪 Step 2: Calling get_billing_data with parameters for last cycle...

            📨 Step 3: Tool response: → Error: Billing data for previous cycles not accessible via current tool.

            ❌ Step 4: I cannot retrieve historical billing details. This request requires unavailable data.

            🚫 Final Output: Unfortunately, I can't assist with this query. I don’t have tool access to billing data for past cycles.
    """

class BillingAgent(BaseAgent):
    """
    Billing Agent for handling billing-related tasks and inquiries.
    
    This agent specializes in processing billing-related requests by connecting
    to a billing service through MCP (Model Context Protocol) and providing
    accurate billing information while maintaining security and privacy.
    
    The agent is configured with specific instructions to:
    - Handle billing inquiries professionally
    - Protect sensitive information
    - Provide clear responses when data is unavailable
    """

    def __init__(
        self,
        kernel: Kernel,
    ) -> None:
        """
        Initialize the Billing Agent.
        
        Args:
            kernel: The Semantic Kernel instance for AI operations
        """
        settings = AzureChatPromptExecutionSettings()
        settings.response_format = AgentLLMResponse
        settings.temperature = 0.0

        super().__init__(  # type: ignore
            kernel=kernel,
            name=Billing.AGENT_NAME,
            instructions=Billing.AGENT_TEMPLATE,
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
        Process a billing-related message asynchronously.
        
        This method handles billing inquiries by:
        1. Connecting to the billing service via MCP plugin
        2. Processing the user's message through the AI model
        3. Providing intermediate status updates
        4. Returning the final billing response
        
        Args:
            message: The user's billing-related message
            message_id: Unique identifier for the message
            thread_id: Unique identifier for the conversation thread
            thread: Chat history thread for context
            on_intermediate_response: Callback for intermediate status updates
        
        Returns:
            A tuple containing:
                - The agent's final response message
                - The updated thread after processing
                - The agent name ("Billing")
        
        Raises:
            Exception: If there are issues connecting to the billing service
                      or processing the request
        """
        plugin = MCPStreamableHttpPlugin(
            name=Billing.PLUGIN_NAME,
            description=Billing.PLUGIN_DESCRIPTION,
            url=Billing.get_mcp_endpoint(),
            headers=Headers.get_mcp_headers(message_id, thread_id),
        )
        await plugin.connect()
        self.kernel.add_plugin(plugin)

        async for _response in self.invoke(messages=message, thread=thread):
            _result = AgentLLMResponse.model_validate(
                json.loads(_response.message.content),
            )

            print(f"# {_response.name}: {_response}")

            on_intermediate_response(
                message_id=message_id,
                status=MessageStatus.IN_PROGRESS,
                result=_result.reply,
                agent_name=self.name,
            )

        _result = AgentLLMResponse.model_validate(
                json.loads(_response.message.content),
            )
        print(f"# {_response.name}: {_response}")

        on_intermediate_response(
            message_id=message_id,
            status=MessageStatus.IN_PROGRESS,
            result="\n".join(_result.steps),
            agent_name=self.name,
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
