"""
Telemetry package for OpenTelemetry integration and observability.

This package provides a unified interface for telemetry setup across different
backends including .NET Aspire Dashboard, Azure Application Insights, and
file-based logging. It automatically selects the appropriate backend based
on the SEMKER_LOGGING_TYPE environment variable.

Supported Backends:
    - aspire: .NET Aspire Dashboard integration (default)
    - appinsights: Azure Application Insights integration
    - filelog: File-based logging fallback

Components:
    - Logging: Structured logging with automatic backend selection
    - Tracing: Distributed tracing for request correlation
    - Metrics: Performance metrics collection
    - FastAPI instrumentation: Automatic API telemetry

Environment Variables:
    SEMKER_LOGGING_TYPE: Selects telemetry backend ("aspire", "appinsights", "filelog")

Usage:
    ```python
    from telemetry import instrument_fastapi
    
    # Instrument FastAPI app
    instrument_fastapi(app)
    
    # Manual telemetry setup
    from telemetry import set_up_logging, set_up_tracing, set_up_metrics
    set_up_logging()
    set_up_tracing()
    set_up_metrics()
    ```

Features:
    - Automatic backend selection based on environment
    - FastAPI automatic instrumentation
    - Requests library instrumentation
    - Type-safe telemetry interfaces
    - Development-friendly console output
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
    Instrument FastAPI application with OpenTelemetry for comprehensive observability.

    This function sets up automatic instrumentation for FastAPI applications and
    the requests library, enabling distributed tracing, metrics collection, and
    performance monitoring without manual code changes.

    Args:
        app: FastAPI application instance to instrument

    Features:
        - Automatic request/response tracing
        - HTTP metrics collection
        - Request correlation across services
        - Performance monitoring
        - Error tracking and debugging

    Side Effects:
        - Instruments the provided FastAPI app
        - Instruments the requests library globally
        - Prints confirmation message to console

    Example:
        ```python
        from fastapi import FastAPI
        from telemetry import instrument_fastapi
        
        app = FastAPI()
        instrument_fastapi(app)
        ```

    Note:
        This function should be called once during application startup,
        typically right after creating the FastAPI app instance.
    """
    # Instrument FastAPI (without hooks to avoid type issues)
    FastAPIInstrumentor.instrument_app(app)

    # Instrument requests library
    RequestsInstrumentor().instrument()

    print("🔍 FastAPI instrumentation enabled")
