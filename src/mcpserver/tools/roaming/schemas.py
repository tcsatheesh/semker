"""
Roaming data schemas and models.

This module contains the Pydantic models used for roaming charges data.
"""

from pydantic import BaseModel


class Charges(BaseModel):
    """
    Represents roaming charges for a specific month.

    Attributes:
        month: The month number (1-12) for these charges.
        details: Dictionary mapping country names to their charge details.
                Each country's details contain capacity, unit, cost, and currency.
    """

    month: int
    details: dict[str, dict[str, str | float]]


class RoamingCharges(BaseModel):
    """
    Container for roaming charges data.

    Attributes:
        roams: List of charge records for different months.
    """

    roams: list[Charges]
