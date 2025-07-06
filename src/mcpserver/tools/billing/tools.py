"""
Billing tools for MCP server.

This module contains the MCP tools for retrieving billing data.
"""

from mcp.server.fastmcp import FastMCP

from .data import bills
from .schemas import BillingData, Bill

mcp = FastMCP(
    name="BillingTool",
    stateless_http=True,
)


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
