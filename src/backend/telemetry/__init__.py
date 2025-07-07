"""
Telemetry package for OpenTelemetry integration with .NET Aspire Dashboard
"""

import os
from typing import Final, Any

_logging_type: str = os.getenv("SEMKER_LOGGING_TYPE", "aspire").lower()

if _logging_type == "appinsights":
    from .appinsights import set_up_logging, set_up_tracing, set_up_metrics
elif _logging_type == "aspire":
    from .aspire import set_up_logging, set_up_tracing, set_up_metrics
else:
    from .filelog import set_up_logging, set_up_tracing, set_up_metrics

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor  # type: ignore
from opentelemetry.instrumentation.requests import RequestsInstrumentor  # type: ignore

__all__: Final[list[str]] = [
    "set_up_logging",
    "set_up_tracing",
    "set_up_metrics",
]


def instrument_fastapi(app: Any) -> None:
    """
    Instrument FastAPI application with OpenTelemetry.

    Args:
        app: FastAPI application instance
    """
    # Instrument FastAPI (without hooks to avoid type issues)
    FastAPIInstrumentor.instrument_app(app)

    # Instrument requests library
    RequestsInstrumentor().instrument()

    print("🔍 FastAPI instrumentation enabled")
