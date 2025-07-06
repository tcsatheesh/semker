"""
Billing data schemas and models.

This module contains Pydantic models for representing billing data structures.
"""

from pydantic import BaseModel


class LineItem(BaseModel):
    """
    Represents a single line item in a customer's bill.

    Attributes:
        description: Description of the charge.
        amount: The monetary amount for this line item.
        notes: Additional notes about the charge.
    """

    description: str
    amount: float
    notes: str


class Bill(BaseModel):
    """
    Represents a customer's bill for a specific month.

    Attributes:
        month: The month number (1-12) for this bill.
        details: List of line items for this bill.
        currency: The currency code for this bill (e.g., "EUR", "USD").
    """

    month: int
    details: list[LineItem]
    currency: str


class BillingData(BaseModel):
    """
    Container for billing data containing one or more bills.

    Attributes:
        bills: List of bills for the customer.
    """

    bills: list[Bill]
