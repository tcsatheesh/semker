"""
Tariff MCP tool definitions.

This module contains the MCP server setup and tool definitions for tariff functionality.
"""

from mcp.server.fastmcp import FastMCP
from .schemas import TariffPlan, PricingStructure
from .data import get_tariff_plan_data, get_current_tariff_plan_data


mcp = FastMCP(
    name="TariffTool",
    stateless_http=True,
)


@mcp.tool(description="A tool to retrieve tariff plan for customers")
async def get_tariff_plan(
    pricing_structure: PricingStructure,
) -> TariffPlan:
    """
    Get tariff plan for a customer based on pricing structure.

    Args:
        pricing_structure: The pricing structure type (prepaid, postpaid, etc.)

    Returns:
        TariffPlan: The tariff plan details for the specified pricing structure.
    """
    return get_tariff_plan_data(pricing_structure)


@mcp.tool(description="A tool to retrieve current tariff plan for a customer")
async def get_current_tariff_plan() -> TariffPlan:
    """
    Get the current tariff plan for a customer.

    Returns:
        TariffPlan: The current tariff plan details.
    """
    return get_current_tariff_plan_data()
