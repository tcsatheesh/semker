"""
Telemetry package for OpenTelemetry integration with .NET Aspire Dashboard
"""

from typing import Final
from .otel_config import configure_telemetry, get_tracer, get_meter, get_logger, instrument_fastapi, semker_metrics
from .middleware import TelemetryMiddleware
from config.telemetry import telemetry_config

__version__: Final[str] = telemetry_config.SERVICE_VERSION

__all__: Final[list[str]] = [
    "configure_telemetry",
    "instrument_fastapi",
    "get_tracer", 
    "get_meter",
    "get_logger",
    "semker_metrics",
    "TelemetryMiddleware"
]
