"""
Billing tool module for managing customer billing data.

This module provides functionality to retrieve and manage billing information
for customers, including monthly charges and line items.
"""

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

mcp = FastMCP(
    name="BillingTool",
    stateless_http=True,
)


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


bills = [
    Bill(
        month=11,
        details=[
            LineItem(
                description="base",
                amount=20.0,
                notes="Base charge for the month",
            ),
            LineItem(
                description="roaming",
                amount=50.0,
                notes="Roaming charges in Spain incurred during the month for 21GB of data",
            ),
            LineItem(
                description="amazon",
                amount=10.0,
                notes="Amazon Prime subscription for the month",
            ),
            LineItem(
                description="spotify",
                amount=10.0,
                notes="Spotify subscription for the month",
            ),
        ],
        currency="EUR",
    ),
    Bill(
        month=10,
        details=[
            LineItem(
                description="base",
                amount=20.0,
                notes="Base charge for the month",
            ),
            LineItem(
                description="roaming",
                amount=0.0,
                notes="No roaming charges incurred during the month",
            ),
            LineItem(
                description="amazon",
                amount=40.0,
                notes="Amazon Prime subscription for the month, includes puchasing of two movies",
            ),
            LineItem(
                description="spotify",
                amount=10.0,
                notes="Spotify subscription for the month",
            ),
        ],
        currency="EUR",
    ),
    Bill(
        month=9,
        details=[
            LineItem(
                description="base",
                amount=20.0,
                notes="Base charge for the month. New base charge due to price increase",
            ),
            LineItem(
                description="roaming",
                amount=0.0,
                notes="No roaming charges incurred during the month",
            ),
            LineItem(
                description="amazon",
                amount=10.0,
                notes="Amazon Prime subscription for the month",
            ),
            LineItem(
                description="spotify",
                amount=10.0,
                notes="Spotify subscription for the month",
            ),
        ],
        currency="EUR",
    ),
    Bill(
        month=8,
        details=[
            LineItem(
                description="base",
                amount=10.0,
                notes="Base charge for the month",
            ),
            LineItem(
                description="roaming",
                amount=0.0,
                notes="No roaming charges incurred during the month",
            ),
            LineItem(
                description="amazon",
                amount=10.0,
                notes="Amazon Prime subscription for the month",
            ),
        ],
        currency="EUR",
    ),
]


@mcp.tool(description="A tool to retrieve billing data for customers")
async def get_billing_data(
    month: int,
) -> BillingData:
    """
    Get billing data for a customer for a specific month.

    Args:
        month: The month number (1-12) to retrieve billing data for.

    Returns:
        BillingData: Container with the billing information for the specified month.

    Raises:
        ValueError: If month is not between 1 and 12, or if no billing data
                   is found for the specified month.
    """
    # Simulated billing data
    if month < 1 or month > 12:
        raise ValueError("Month must be between 1 and 12")
    try:
        _bill: Bill = next(bill for bill in bills if bill.month == month)
        billing_data = BillingData(bills=[_bill])
        return billing_data
    except StopIteration:
        raise ValueError(f"No billing data found for month {month}") from None
