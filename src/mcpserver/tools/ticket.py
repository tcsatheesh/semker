"""
Support ticket management tool module.

This module provides functionality to raise support tickets with chat history
and consent management.
"""

import random
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

mcp = FastMCP(
    name="TicketingTool",
    stateless_http=True,
)


class TicketResponse(BaseModel):
    """
    Represents the response from a support ticket creation request.

    Attributes:
        ticket_number: Unique identifier for the support ticket.
        status: Current status of the ticket (e.g., "Open", "Closed").
        description: Description of the ticket creation result.
    """

    ticket_number: str
    status: str
    description: str


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
    # Here you would implement the logic to raise a support ticket
    # For demonstration purposes, we will just return a success message
    if consent:
        print(
            f"Support ticket raised successfully with the following chat history:\n{chat_history} \nand consent response:\n{consent_response}"
        )

        return TicketResponse(
            ticket_number=str(random.randint(10000, 99999)),
            status="Open",
            description="Support ticket raised successfully.",
        )
    else:
        print("Consent not given. Support ticket not raised.")
        raise ValueError("Consent not given to raise a support ticket.")
