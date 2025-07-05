"""
Custom telemetry hooks for FastAPI instrumentation.

This module provides custom hooks for OpenTelemetry FastAPI instrumentation
to add custom attributes and logging for request/response lifecycle.
"""

import logging
from typing import Any

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor # type: ignore[import-untyped]
from opentelemetry.trace import Span


class CustomHooks:
    """Custom hooks for FastAPI OpenTelemetry instrumentation."""

    @classmethod
    def server_request_hook(
        cls,
        span: Span,
        scope: dict[str, Any],
    ) -> None:
        """
        Hook called on server request start.

        Args:
            span: The OpenTelemetry span for this request.
            scope: ASGI scope containing request information.
        """
        logging.info("Server request hook called with scope: %s", scope)

    @classmethod
    def client_request_hook(
        cls,
        span: Span,
        scope: dict[str, Any],
        message: dict[str, Any],
    ) -> None:
        """
        Hook called on client request start.

        Args:
            span: The OpenTelemetry span for this request.
            scope: ASGI scope containing request information.
            message: ASGI message containing request details.
        """
        if span and span.is_recording():
            span.set_attribute(
                "custom_user_attribute_from_client_request_hook", "some-value"
            )
        logging.info("Client request hook called with message: %s", message)

    @classmethod
    def client_response_hook(
        cls,
        span: Span,
        scope: dict[str, Any],
        message: dict[str, Any],
    ) -> None:
        """
        Hook called on client response completion.

        Args:
            span: The OpenTelemetry span for this request.
            scope: ASGI scope containing request information.
            message: ASGI message containing response details.
        """
        logging.info("Client response hook called with message: %s", message)


def set_up_hooks() -> None:
    """
    Set up custom hooks for FastAPI OpenTelemetry instrumentation.

    Configures the FastAPIInstrumentor with custom hooks for server requests,
    client requests, and client responses.
    """
    FastAPIInstrumentor().instrument(
        server_request_hook=CustomHooks.server_request_hook,
        client_request_hook=CustomHooks.client_request_hook,
        client_response_hook=CustomHooks.client_response_hook,
    )
