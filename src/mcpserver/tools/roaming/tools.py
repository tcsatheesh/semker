"""
Roaming MCP tool definitions.

This module contains the MCP server setup and tool definitions for roaming functionality.
"""

from typing import Annotated
from mcp.server.fastmcp import FastMCP

from .schemas import RoamingCharges
from .data import get_roaming_charges_data


mcp = FastMCP(
    name="RoamingTool",
    stateless_http=True,
)


@mcp.tool(
    description="A tool to get roaming charges for the customer by country and month"
)
async def get_roaming_charges(
    country: Annotated[
        str, "The country to get roaming charges for: Romania, Spain, Belgium"
    ],
    month: Annotated[int, "The month (1-12) to get roaming charges for"],
) -> RoamingCharges:
    """
    Get roaming charges for a specific country and month.

    Args:
        country: The country to retrieve roaming charges for.
                Must be one of: Romania, Spain, Belgium.
        month: The month number (1-12) to retrieve charges for.

    Returns:
        RoamingCharges: Container with roaming charge information for the
                       specified country and month.

    Raises:
        ValueError: If month is not between 1 and 12, or if country is not
                   one of the supported countries.
    """
    return get_roaming_charges_data(country, month)
