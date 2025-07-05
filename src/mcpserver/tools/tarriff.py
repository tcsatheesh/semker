"""
Tariff and usage data management tool module.

This module provides functionality to retrieve tariff information and usage
details for customers.
"""

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

mcp = FastMCP(
    name="TariffTool",
    stateless_http=True,
)


class TariffData(BaseModel):
    """
    Represents tariff offer information for a customer.

    Attributes:
        offer_amount: The price of the tariff offer.
        offer_currency: Currency code for the offer (e.g., "EUR", "USD").
        offer_name: Name of the tariff offer.
        offer_description: Detailed description of the offer.
        offer_valid_from: Start date of the offer validity (ISO format).
        offer_valid_until: End date of the offer validity (ISO format).
        capacity: Data capacity included in the offer.
        capacity_unit: Unit of the data capacity (e.g., "GB", "MB").
    """

    offer_amount: float
    offer_currency: str
    offer_name: str
    offer_description: str
    offer_valid_from: str
    offer_valid_until: str
    capacity: float
    capacity_unit: str  # GB or MB


class MonthlyUsage(BaseModel):
    """
    Represents monthly usage data for a customer.

    Attributes:
        month: The month number (1-12).
        usage: Amount of data used in that month.
        usage_unit: Unit of the usage data (e.g., "GB", "MB").
    """

    month: int
    usage: float
    usage_unit: str


class UsageDetails(BaseModel):
    """
    Represents detailed usage information for a customer.

    Attributes:
        total_usage: Total amount of data used.
        total_usage_unit: Unit of the total usage (e.g., "GB", "MB").
        monthly_usage: List of monthly usage breakdowns.
    """

    total_usage: float
    total_usage_unit: str
    monthly_usage: list[MonthlyUsage]


@mcp.tool(description="A tool to retrieve tariff data for customers")
async def get_tariff_data_by_customer(
    customer_id: str,
) -> TariffData:
    """
    Get tariff offer data for a specific customer.

    Args:
        customer_id: Unique identifier for the customer.

    Returns:
        TariffData: The tariff offer information for the customer.
    """
    return TariffData(
        offer_amount=29.99,
        offer_currency="EUR",
        offer_name="Unlimited Data Plan",
        offer_description="An unlimited data plan with no restrictions.",
        offer_valid_from="2023-01-01",
        offer_valid_until="2024-01-01",
        capacity=100.0,
        capacity_unit="GB",
    )


@mcp.tool(description="A tool to retrieve usage data for customers")
async def get_usage_details_by_customer(
    customer_id: str,
) -> UsageDetails:
    """
    Get usage details for a specific customer.

    Args:
        customer_id: Unique identifier for the customer.

    Returns:
        UsageDetails: The usage information for the customer including
                     total usage and monthly breakdowns.
    """
    return UsageDetails(
        total_usage=50.0,
        total_usage_unit="GB",
        monthly_usage=[
            MonthlyUsage(month=1, usage=5.0, usage_unit="GB"),
        ],
    )
