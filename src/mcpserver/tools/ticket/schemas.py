"""
Support ticket schemas and models.

This module contains the Pydantic models used for support ticket management.
"""

from pydantic import BaseModel


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
