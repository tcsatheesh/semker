"""
Broadband troubleshooting tool module.

This module provides functionality to retrieve troubleshooting steps
for different broadband router models.
"""

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

mcp = FastMCP(
    name="BroadbandTroubleshootingTool",
    stateless_http=True,
)


class TroubleshootingModel(BaseModel):
    """
    Represents troubleshooting steps for a specific router model.

    Attributes:
        model_name: The name/brand of the router model.
        steps: List of troubleshooting steps, each step is a dictionary
               with step number as key and instruction as value.
    """

    model_name: str
    steps: list[dict[str, str]]


class Troubleshooting(BaseModel):
    """
    Container for troubleshooting information.

    Attributes:
        troubleshooting_models: List of troubleshooting models with their steps.
    """

    troubleshooting_models: list[TroubleshootingModel]


troubleshooting_models: list[TroubleshootingModel] = [
    TroubleshootingModel(
        model_name="Netgear",
        steps=[
            {
                "1": "Check if the broadband lights are on.",
            },
            {
                "2a": "If broadband lights are not on check the broadband is connected to the mains.",
            },
            {
                "2b": "If broadband lights are on check the computer is connected to the network.",
            },
        ],
    )
]


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
    troubleshooting = Troubleshooting(
        troubleshooting_models=[
            model
            for model in troubleshooting_models
            if model.model_name.lower() == model_name.lower()
        ]
    )
    return troubleshooting
