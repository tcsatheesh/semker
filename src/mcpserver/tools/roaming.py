"""
Roaming charges tool module for managing customer roaming data.

This module provides functionality to retrieve roaming charges by country
and month for customers traveling abroad.
"""

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

mcp = FastMCP(
    name="RoamingTool",
    stateless_http=True,
)


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


_roaming_data = RoamingCharges(
    roams=[
        Charges(
            month=11,
            details={
                "Romania": {
                    "Amount": 1.0,
                    "Unit": "GB",
                    "Cost": 3.99,
                    "Currency": "EUR",
                },
                "Spain": {
                    "Capacity": 3.0,
                    "Unit": "GB",
                    "Cost": 5.99,
                    "Currency": "EUR",
                },
                "Belgium": {
                    "Capacity": 2.0,
                    "Unit": "GB",
                    "Cost": 4.99,
                    "Currency": "EUR",
                },
            },
        ),
        Charges(
            month=10,
            details={
                "Romania": {
                    "Amount": 1.0,
                    "Unit": "GB",
                    "Cost": 3.99,
                    "Currency": "EUR",
                },
                "Spain": {
                    "Capacity": 3.0,
                    "Unit": "GB",
                    "Cost": 5.99,
                    "Currency": "EUR",
                },
                "Belgium": {
                    "Capacity": 2.0,
                    "Unit": "GB",
                    "Cost": 4.99,
                    "Currency": "EUR",
                },
            },
        ),
        Charges(
            month=9,
            details={
                "Romania": {
                    "Amount": 1.0,
                    "Unit": "GB",
                    "Cost": 1.99,
                    "Currency": "EUR",
                },
                "Spain": {
                    "Capacity": 3.0,
                    "Unit": "GB",
                    "Cost": 3.99,
                    "Currency": "EUR",
                },
                "Belgium": {
                    "Capacity": 2.0,
                    "Unit": "GB",
                    "Cost": 3.99,
                    "Currency": "EUR",
                },
            },
        ),
        Charges(
            month=8,
            details={
                "Romania": {
                    "Amount": 1.0,
                    "Unit": "GB",
                    "Cost": 1.99,
                    "Currency": "EUR",
                },
                "Spain": {
                    "Capacity": 3.0,
                    "Unit": "GB",
                    "Cost": 3.99,
                    "Currency": "EUR",
                },
                "Belgium": {
                    "Capacity": 2.0,
                    "Unit": "GB",
                    "Cost": 3.99,
                    "Currency": "EUR",
                },
            },
        ),
    ],
)


@mcp.tool(description="A tool to retrieve roaming charges by country")
async def get_roaming_charges_by_country(
    country: str,
    month: int,
) -> RoamingCharges:
    """
    Get roaming charges for a specific country and month.

    Args:
        country: The country name to get roaming charges for.
                Must be one of: Romania, Spain, Belgium.
        month: The month number (1-12) to retrieve charges for.

    Returns:
        RoamingCharges: Container with roaming charge information for the
                       specified country and month.

    Raises:
        ValueError: If month is not between 1 and 12, or if country is not
                   one of the supported countries.
    """
    if month < 1 or month > 12:
        raise ValueError("Month must be between 1 and 12")
    if country not in ["Romania", "Spain", "Belgium"]:
        raise ValueError("Country must be one of: Romania, Spain, Belgium")
    # Simulated roaming data
    filtered_data = [
        Charges(
            month=charge.month,
            details={country: charge.details.get(country, {})},
        )
        for charge in _roaming_data.roams
        if charge.month == month
    ]
    return RoamingCharges(roams=filtered_data)
