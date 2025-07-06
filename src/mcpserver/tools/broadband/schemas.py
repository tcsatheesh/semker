"""
Broadband troubleshooting schemas and models.

This module contains the Pydantic models used for broadband troubleshooting data.
"""

from pydantic import BaseModel


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
