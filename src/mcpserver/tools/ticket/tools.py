"""
Ticket MCP tool definitions.

This module contains the MCP server setup and tool definitions for ticket functionality.
"""

from typing import Annotated
from mcp.server.fastmcp import FastMCP
from .schemas import TicketResponse
from .data import raise_support_ticket_data


mcp = FastMCP(
    name="TicketingTool",
    stateless_http=True,
)


@mcp.tool(description="A tool raise a support ticket")
async def raise_support_ticket(
    chat_history: Annotated[
        str, "The chat history leading to the support ticket request"
    ],
    consent: Annotated[bool, "Consent to raise a support ticket was a true or false"],
    consent_response: Annotated[
        str,
        "The response to the consent question, e.g., 'Yes, I consent to raise a support ticket.'",
    ],
) -> TicketResponse:
    """
    Raise a support ticket with the provided chat history and consent.

    Args:
        chat_history: The conversation history that led to the support ticket request.
        consent: Boolean indicating whether the user has given consent to raise a ticket.
        consent_response: The user's explicit response to the consent question.

    Returns:
        TicketResponse: Information about the created support ticket including
                       ticket number, status, and description.

    Raises:
        ValueError: If consent is not given to raise a support ticket.
    """
    return raise_support_ticket_data(chat_history, consent, consent_response)
