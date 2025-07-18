# main.py
"""
Main application module for the MCP server.

This module sets up a FastAPI application with telemetry and multiple MCP tools
for billing, roaming, broadband, and ticket management.
"""

import contextlib
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor # type: ignore[import-untyped]

from telemetry import set_up_logging
from tools import billing, broadband, roaming, ticket, tariff, faq

set_up_logging()


class HealthStatus(BaseModel):
    """Response model for health check."""
    status: str
    service: str
    version: str


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
        await stack.enter_async_context(faq.mcp.session_manager.run())
        yield


# FastAPI app with comprehensive Swagger documentation
app = FastAPI(
    title="Semantic Kernel MCP Server",
    description="""
## Semantic Kernel Model Context Protocol (MCP) Server

This server provides multiple AI-powered tools for telecommunications and customer service operations.

### Available Tools

* **Billing Tool** (`/bill/mcp`) - Retrieve customer billing data and monthly charges
* **Roaming Tool** (`/roam/mcp`) - Get roaming charges by country and month  
* **Tariff Tool** (`/tariff/mcp`) - Access tariff plans and pricing structures
* **Broadband Tool** (`/broadband/mcp`) - Troubleshooting steps for router models
* **Ticket Tool** (`/ticket/mcp`) - Support ticket management with chat history
* **FAQ Tool** (`/faq/mcp`) - Retrieve frequently asked questions (FAQ)

### Features

- **Type-safe**: Full TypeScript-style type checking with mypy
- **Modular**: Clean separation of concerns with individual tool packages
- **Telemetry**: OpenTelemetry instrumentation for monitoring and tracing
- **Production-ready**: Proper error handling and async support

### Usage

Each tool is mounted as a separate MCP endpoint that can be used by AI agents
to provide intelligent customer service and telecommunications support.

For detailed API documentation, see the individual endpoint sections below.
    """,
    version="1.0.0",
    contact={
        "name": "Semantic Kernel Team",
        "url": "https://github.com/microsoft/semantic-kernel",
        "email": "semantic-kernel@microsoft.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "billing",
            "description": "Customer billing and invoice management operations",
        },
        {
            "name": "roaming", 
            "description": "International roaming charges and country-specific rates",
        },
        {
            "name": "tariff",
            "description": "Tariff plans, pricing structures, and service offerings",
        },
        {
            "name": "broadband",
            "description": "Router troubleshooting and technical support guidance",
        },
        {
            "name": "ticket",
            "description": "Support ticket creation and customer service management",
        },
        {
            "name": "faq",
            "description": "Support answering frequently asked questions (FAQ)",
        },
    ],
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

FastAPIInstrumentor.instrument_app(app)

# Mount MCP tools with proper documentation
app.mount(
    "/bill", 
    billing.mcp.streamable_http_app(),
    name="billing"
)
app.mount(
    "/roam", 
    roaming.mcp.streamable_http_app(),
    name="roaming"
)
app.mount(
    "/tariff", 
    tariff.mcp.streamable_http_app(),
    name="tariff"
)
app.mount(
    "/broadband", 
    broadband.mcp.streamable_http_app(),
    name="broadband"
)
app.mount(
    "/ticket", 
    ticket.mcp.streamable_http_app(),
    name="ticket"
)
app.mount(
    "/faq", 
    faq.mcp.streamable_http_app(),
    name="faq"
)

# Add a root endpoint that redirects to docs
@app.get("/", tags=["root"])
async def root() -> RedirectResponse:
    """
    Root endpoint that redirects to the interactive API documentation.
    
    Returns:
        RedirectResponse: Redirect to the Swagger UI documentation
    """
    return RedirectResponse(url="/docs")

# Add health check endpoint
@app.get("/health", tags=["monitoring"], response_model=HealthStatus)
async def health_check() -> HealthStatus:
    """
    Health check endpoint for monitoring and load balancer probes.
    
    Returns:
        HealthStatus: Health status information
    """
    return HealthStatus(
        status="healthy",
        service="mcp-server",
        version="1.0.0"
    )
