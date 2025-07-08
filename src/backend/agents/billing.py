"""
Billing Agent module for handling billing-related tasks and inquiries.

This module provides the BillingAgent class that specializes in processing
billing-related user requests through the Model Context Protocol (MCP)
and Semantic Kernel framework. The agent connects to external billing services
to retrieve accurate billing information while maintaining security and privacy.

Classes:
    Billing: Configuration class containing agent settings and templates
    BillingAgent: Main agent class for processing billing inquiries

Features:
    - Secure MCP integration with billing services
    - Structured chain-of-thought reasoning
    - Real-time intermediate response updates
    - Data privacy and security enforcement
    - Tool-based data retrieval validation
    - Tabular billing information presentation

Example:
    ```python
    agent = BillingAgent(kernel)
    response = await agent.process_message_async(
        message="What is my current bill?",
        message_id="msg-123",
        thread_id="thread-456",
        thread=thread,
        on_intermediate_response=callback
    )
    ```
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
    """
    Configuration class for the Billing Agent.

    This class contains all configuration settings, constants, and templates
    needed for the Billing Agent to function properly. It provides a centralized
    location for agent-specific settings including MCP endpoint configuration,
    agent identity, and processing instructions.

    Class Attributes:
        AGENT_NAME: The identifier name for this agent
        PLUGIN_NAME: The name of the MCP plugin for billing services
        PLUGIN_DESCRIPTION: Description of the plugin functionality
        AGENT_TEMPLATE: Comprehensive instructions for the agent's behavior

    Methods:
        get_mcp_endpoint: Returns the MCP server endpoint for billing services

    Features:
        - Secure data handling with privacy protection
        - Structured reasoning with chain-of-thought approach
        - Tool-based data validation to prevent hallucination
        - Clear error handling for unavailable data
        - Tabular presentation of billing information
    """

    # Agent identity
    AGENT_NAME: Final[str] = "Billing"
    PLUGIN_NAME: Final[str] = "BillingPlugin"
    PLUGIN_DESCRIPTION: Final[str] = "A plugin for handling billing."

    # Service endpoint
    @classmethod
    def get_mcp_endpoint(cls) -> str:
        """
        Get the MCP endpoint URL for the billing service.

        Returns:
            str: The complete URL endpoint for the billing MCP server

        Note:
            This method retrieves the endpoint from the Services configuration
            which can be customized via environment variables.
        """
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
            → Present response in a concise, well-structured format, using stepwise explanation when helpful.
            → All billing information should be presented in a table format and MUST be preceeded by briefly describing what the table contains, with clear headings for each column.
            
    """

class BillingAgent(BaseAgent):
    """
    Specialized agent for handling billing-related inquiries and tasks.
    
    This agent extends the BaseAgent class to provide specialized functionality
    for processing billing-related requests. It connects to external billing
    services through the Model Context Protocol (MCP) to retrieve accurate
    billing information while maintaining strict security and privacy standards.
    
    The BillingAgent implements a structured chain-of-thought approach to:
    - Analyze billing-related queries step by step
    - Retrieve data only from verified tools and services
    - Protect sensitive billing information
    - Present information in clear, tabular formats
    - Handle error cases gracefully without hallucination
    
    Key Features:
        - MCP integration for secure billing data access
        - Chain-of-thought reasoning for transparency
        - Real-time intermediate response updates
        - Strict data validation and privacy protection
        - Professional billing information presentation
        - Graceful handling of unavailable data
    
    Security Measures:
        - No assumptions or hallucinated billing data
        - Tool-based data validation only
        - Clear error messages for unavailable information
        - No redirection to external support channels
    
    Example Usage:
        ```python
        billing_agent = BillingAgent(kernel)
        response = await billing_agent.process_message_async(
            message="What are my current charges?",
            message_id="msg-123",
            thread_id="thread-456",
            thread=chat_thread,
            on_intermediate_response=update_callback
        )
        ```
    """

    def __init__(
        self,
        kernel: Kernel,
    ) -> None:
        """
        Initialize the Billing Agent with Semantic Kernel configuration.
        
        This constructor sets up the billing agent with specific execution settings
        optimized for billing inquiries, including structured response formatting
        and temperature settings for consistent, accurate responses.
        
        Args:
            kernel: The Semantic Kernel instance configured with AI services
                   and necessary connectors for billing operations
        
        Configuration:
            - Response format set to AgentLLMResponse for structured output
            - Temperature set to 0.0 for consistent, deterministic responses
            - Agent name, instructions, and settings applied from Billing config
        
        Example:
            ```python
            kernel = Kernel()
            # Configure kernel with AI services...
            billing_agent = BillingAgent(kernel)
            ```
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
        Process a billing-related message asynchronously with MCP integration.
        
        This method handles billing inquiries by connecting to external billing
        services through MCP, processing the user's message with chain-of-thought
        reasoning, and providing real-time updates throughout the process.
        
        Processing Flow:
        1. Establish MCP connection to billing service
        2. Add billing plugin to the kernel
        3. Process message through AI model with structured reasoning
        4. Send intermediate updates for each reasoning step
        5. Generate final structured response
        6. Clean up MCP connection
        
        Args:
            message: The user's billing-related message or question
            message_id: Unique identifier for tracking this message
            thread_id: Unique identifier for the conversation thread
            thread: Chat history thread containing conversation context
            on_intermediate_response: Callback function for sending real-time updates
                                    Called with (message_id, status, result, agent_name)
        
        Returns:
            AgentResponse: Structured response containing:
                - reply: The final billing response message
                - human_input_required: Whether additional input is needed
                - able_to_serve: Whether the agent could serve the request
                - thread: Updated conversation thread
                - agent_name: "Billing"
        
        Raises:
            Exception: If MCP connection fails or message processing encounters errors
        
        Security Features:
            - All data retrieved through verified MCP tools only
            - No assumptions or hallucinated billing information
            - Clear error handling for unavailable data
            - Automatic connection cleanup for security
        
        Example:
            ```python
            response = await billing_agent.process_message_async(
                message="What is my current bill?",
                message_id="msg-123",
                thread_id="thread-456",
                thread=chat_thread,
                on_intermediate_response=lambda id, status, result, name: print(f"{status}: {result}")
            )
            print(response.reply)  # Final billing response
            ```
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
