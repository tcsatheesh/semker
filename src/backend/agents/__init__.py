"""
AI Agent Package for Semker Backend.

This package contains all AI agent implementations for the Semker backend system.
The agents are built using Microsoft Semantic Kernel and provide specialized
functionality for different domains such as billing, roaming, tariffs, and FAQs.

Modules:
    base: Abstract base classes and interfaces for all agents
    billing: Billing agent for account and payment inquiries
    roaming: Roaming agent for international usage and rates
    tariff: Tariff agent for plan and pricing information
    faq: FAQ agent for general questions and support
    planner: Planner agent for request routing and orchestration
    skernel: Semantic Kernel utilities and configuration
    config: Configuration settings and constants for agents

Agent Architecture:
    - BaseAgent: Abstract base class for all specialized agents
    - Specialized Agents: Domain-specific implementations
    - PlannerAgent: Smart router for request delegation
    - MCP Integration: Model Context Protocol for external services
    - Chain-of-Thought: Transparent reasoning for all responses

Features:
    - Intelligent request routing and delegation
    - Real-time intermediate response updates
    - Conversation context management
    - Secure data handling with tool validation
    - Professional response formatting
    - Comprehensive error handling

Example:
    ```python
    from agents.skernel import KernelUtils
    
    # Initialize agent system
    kernel_utils = KernelUtils("msg-123", "thread-456")
    agent = kernel_utils.get_agent()
    
    # Process message
    response = await agent.process_message_async(
        message="What is my current bill?",
        message_id="msg-123",
        thread_id="thread-456",
        thread=chat_thread,
        on_intermediate_response=callback
    )
    ```
"""
