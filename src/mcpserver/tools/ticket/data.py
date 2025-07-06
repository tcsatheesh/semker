"""
Support ticket data access and business logic.

This module contains the functions for managing support tickets.
"""

import random
from .schemas import TicketResponse


def raise_support_ticket_data(
    chat_history: str,
    consent: bool,
    consent_response: str,
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
