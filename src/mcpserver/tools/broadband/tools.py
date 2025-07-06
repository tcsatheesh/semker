"""
Broadband MCP tool definitions.

This module contains the MCP server setup and tool definitions for broadband functionality.
"""

from mcp.server.fastmcp import FastMCP
from .schemas import Troubleshooting
from .data import get_troubleshooting_steps_data


mcp = FastMCP(
    name="BroadbandTroubleshootingTool",
    stateless_http=True,
)


@mcp.tool(description="A tool to retrieve broadband troubleshooting steps")
async def get_troubleshooting_steps(
    model_name: str,
) -> Troubleshooting:
    """
    Get troubleshooting steps for a specific broadband router model.

    Args:
        model_name: The name/brand of the router model to get troubleshooting
                   steps for (case-insensitive).

    Returns:
        Troubleshooting: Container with troubleshooting steps for the specified
                        router model.
    """
    return get_troubleshooting_steps_data(model_name)
