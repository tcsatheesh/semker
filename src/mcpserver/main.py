# main.py
"""
Main application module for the MCP server.

This module sets up a FastAPI application with telemetry and multiple MCP tools
for billing, roaming, broadband, and ticket management.
"""

import contextlib
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor # type: ignore[import-untyped]

from telemetry import set_up_logging
from tools import billing, broadband, roaming, ticket, tariff

set_up_logging()


# Create a combined lifespan to manage both session managers
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Manage the lifespan of the FastAPI application.

    This function handles the startup and shutdown of all MCP session managers
    for the various tools (billing, roaming, broadband, ticket).

    Args:
        app: The FastAPI application instance.

    Yields:
        None: Control is yielded back to the application during its lifetime.
    """
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(billing.mcp.session_manager.run())
        await stack.enter_async_context(roaming.mcp.session_manager.run())
        await stack.enter_async_context(tariff.mcp.session_manager.run())
        await stack.enter_async_context(broadband.mcp.session_manager.run())
        await stack.enter_async_context(ticket.mcp.session_manager.run())
        yield


app = FastAPI(lifespan=lifespan)

FastAPIInstrumentor.instrument_app(app)

app.mount("/bill", billing.mcp.streamable_http_app())
app.mount("/roam", roaming.mcp.streamable_http_app())
app.mount("/tariff", tariff.mcp.streamable_http_app())
app.mount("/broadband", broadband.mcp.streamable_http_app())
app.mount("/ticket", ticket.mcp.streamable_http_app())
