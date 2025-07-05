"""
Telemetry setup module for the MCP application.

This module provides configuration and setup for different types of logging
and telemetry based on environment variables.
"""


def set_up_logging() -> None:
    """
    Set up logging based on the TELEMETRY_LOGGING_TYPE environment variable.

    Supported logging types:
    - "aspire": Sets up Aspire-style logging (default)
    - "appinsights": Sets up Application Insights logging

    Also sets up telemetry hooks regardless of the logging type.
    """
    import os

    _logging_type = os.getenv("TELEMETRY_LOGGING_TYPE", "aspire").lower()

    if _logging_type == "aspire":
        from .aspire import set_up_logging as setup_aspire_logging

        setup_aspire_logging()
    from .hooks import set_up_hooks

    set_up_hooks()
