"""
Broadband troubleshooting data access and business logic.

This module contains the data and functions for managing broadband troubleshooting.
"""

from .schemas import TroubleshootingModel, Troubleshooting


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


def get_troubleshooting_steps_data(model_name: str) -> Troubleshooting:
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
