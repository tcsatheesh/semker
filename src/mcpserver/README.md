# Semantic Kernel MCP Server

A FastAPI-based Model Context Protocol (MCP) server providing AI-powered customer service tools for telecommunications operations, with comprehensive Swagger documentation, telemetry integration, and type safety.

## Overview

The Semantic Kernel MCP (Model Context Protocol) Server provides a comprehensive REST API for telecommunications and customer service operations. The server includes automatic OpenAPI/Swagger documentation generation and supports multiple AI-powered tools for intelligent customer service automation.

## Features

- **🤖 AI-Powered Tools**: Multiple MCP tools for telecommunications and customer service
- **📚 Interactive Documentation**: Automatic Swagger/OpenAPI documentation generation
- **🔒 Type Safety**: Full mypy strict type checking with Pydantic models
- **📊 Telemetry Integration**: OpenTelemetry observability with Aspire Dashboard support
- **🏗️ Modular Architecture**: Clean separation of concerns with individual tool packages
- **⚡ Production Ready**: Proper error handling, async support, and health monitoring

### Available Tools

- **Billing Management**: Retrieve customer billing data and line items
- **Roaming Services**: Get roaming charges by country and month
- **Broadband Support**: Router troubleshooting steps for different models
- **Ticket Management**: Create and manage support tickets with consent tracking
- **Tariff Information**: Access tariff plans, pricing structures, and usage details

## Quick Start

### Prerequisites

- Python 3.11+
- uv (Python package installer)

### Installation

1. Install dependencies:
```bash
uv sync
```

2. Start the development server:
```bash
# Using the development script
python dev_server.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. Access the interactive documentation:
```bash
# Open in your browser
open http://localhost:8000/docs
```

## API Documentation

### Accessing Documentation

#### Interactive API Documentation (Swagger UI)
- **URL**: `http://localhost:8000/docs`
- **Features**: 
  - Interactive API testing
  - Request/response examples
  - Schema definitions
  - Try-it-now functionality

#### Alternative Documentation (ReDoc)
- **URL**: `http://localhost:8000/redoc`
- **Features**:
  - Clean, readable format
  - Detailed schema documentation
  - Code examples in multiple languages

#### OpenAPI Schema
- **URL**: `http://localhost:8000/openapi.json`
- **Use**: Raw OpenAPI 3.0 schema for integration with other tools

### Core API Endpoints

#### Root Information
- **GET** `/` - API information and available tools
- **GET** `/health` - Health check for monitoring

#### MCP Tool Endpoints
- **POST** `/bill/*` - Billing and invoice management tools
- **POST** `/roam/*` - International roaming charges tools  
- **POST** `/tariff/*` - Tariff plans and pricing tools
- **POST** `/broadband/*` - Router troubleshooting tools
- **POST** `/ticket/*` - Support ticket management tools

## Tool Descriptions

### Billing Tool (`/bill`)
- Retrieve customer billing data and monthly charges
- Get detailed line items and invoice history
- Access billing information with type-safe responses

### Roaming Tool (`/roam`) 
- Get roaming charges by country and month
- International rate information for Romania, Spain, Belgium
- Monthly roaming usage data with cost breakdowns

### Tariff Tool (`/tariff`)
- Access available tariff plans (prepaid, postpaid, hybrid, flat-rate, tiered)
- Get current customer tariff information
- Pricing structure and service offering details

### Broadband Tool (`/broadband`)
- Router troubleshooting steps for specific models
- Model-specific guidance (Netgear, TP-Link, ASUS)
- Technical support procedures and diagnostics

### Ticket Tool (`/ticket`)
- Create support tickets with chat history
- Manage customer consent and tracking
- Generate unique ticket numbers and status updates

## Project Structure

```
src/mcpserver/
├── main.py                    # Main FastAPI application with Swagger docs
├── dev_server.py             # Development server startup script
├── mypy.ini                  # Type checking configuration
├── pyproject.toml           # Project configuration and dependencies
├── telemetry/               # Telemetry and logging modules
│   ├── __init__.py          # Telemetry setup coordinator
│   ├── aspire.py            # Aspire Dashboard integration
│   └── hooks.py             # Custom OpenTelemetry hooks
└── tools/                   # Modular MCP tool implementations
    ├── billing/             # Billing tool package
    │   ├── __init__.py      # Package initialization
    │   ├── schemas.py       # Pydantic models
    │   ├── data.py          # Business logic and data access
    │   └── tools.py         # MCP tool definitions
    ├── roaming/             # Roaming tool package
    ├── tariff/              # Tariff tool package
    ├── broadband/           # Broadband tool package
    ├── ticket/              # Ticket tool package
    ├── billing.py           # Legacy compatibility layer
    ├── roaming.py           # Legacy compatibility layer
    ├── tariff.py            # Legacy compatibility layer
    ├── broadband.py         # Legacy compatibility layer
    └── ticket.py            # Legacy compatibility layer
```

## API Endpoints

The application provides the following endpoints:

### Core Service Endpoints
- **GET** `/` - Root API information and tool descriptions
- **GET** `/health` - Health check for monitoring and load balancers
- **GET** `/docs` - Interactive Swagger UI documentation
- **GET** `/redoc` - Alternative ReDoc documentation
- **GET** `/openapi.json` - OpenAPI 3.0 schema

### MCP Tool Endpoints
- `/bill` - Billing data retrieval and management
- `/roam` - Roaming charges information by country
- `/tariff` - Tariff plans and pricing structures
- `/broadband` - Router troubleshooting support
- `/ticket` - Support ticket management

## Development

### Type Safety
The project uses strict mypy type checking with comprehensive configuration:
```bash
# Run type checking
python -m mypy --strict .
```

### API Documentation
The API documentation is automatically updated when you modify the code. The FastAPI framework introspects your Python type annotations and Pydantic models to generate accurate, up-to-date documentation.

For more information about the MCP protocol, visit the [Model Context Protocol documentation](https://modelcontextprotocol.io/).

### Development Server
Use the included development server for hot-reload capabilities:
```bash
# Start with auto-reload
python dev_server.py

# Manual uvicorn command
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Code Organization
- **Schemas**: Pydantic models in `schemas.py` files
- **Data Layer**: Business logic in `data.py` files  
- **Tools**: MCP tool definitions in `tools.py` files
- **Compatibility**: Legacy imports maintained for backward compatibility

## Telemetry & Observability

### Features
- **Logging**: Structured logging with OpenTelemetry
- **Tracing**: Distributed tracing for request tracking
- **Metrics**: Performance and usage metrics
- **Dashboard**: Aspire Dashboard integration at `http://localhost:4317`

### Configuration
Set the telemetry logging type via environment variable:
```bash
# Aspire Dashboard (default)
TELEMETRY_LOGGING_TYPE=aspire

# Application Insights
TELEMETRY_LOGGING_TYPE=appinsights
```

## Data Models

### Billing
- `LineItem`: Individual billing line items with costs and descriptions
- `Bill`: Monthly bill container with line items
- `BillingData`: Complete billing information container

### Roaming
- `Charges`: Monthly roaming charges by country with cost details
- `RoamingCharges`: Container for roaming data across multiple countries

### Tariff
- `TariffPlan`: Complete tariff plan with pricing, limits, and add-ons
- `ValidityPeriod`: Service validity periods
- `UsageLimit`: Data, voice, and SMS usage limits
- `AddOn`: Additional services and pricing
- `PromotionalOffer`: Special offers and discounts

### Broadband
- `TroubleshootingModel`: Router-specific troubleshooting steps
- `Troubleshooting`: Container for troubleshooting information

### Tickets
- `TicketResponse`: Support ticket creation response with ticket number and status

## Features & Benefits

### For Developers
- **Type Safety**: Full mypy strict type checking prevents runtime errors
- **Auto Documentation**: Swagger UI automatically reflects code changes
- **Modular Design**: Clean separation allows independent tool development
- **Testing**: Built-in validation and error handling

### For Operations
- **Health Monitoring**: Built-in health check endpoints
- **Telemetry**: Comprehensive observability with OpenTelemetry
- **Production Ready**: Proper async support and error handling
- **Scalable**: FastAPI's async capabilities support high concurrency

### For Integration
- **OpenAPI Schema**: Machine-readable API specification
- **MCP Protocol**: Standard protocol for AI agent integration
- **RESTful Design**: Standard HTTP methods and status codes
- **JSON Responses**: Structured, predictable response formats

## Error Handling

All tools include comprehensive error handling with:
- Input validation for parameters
- Proper exception chaining
- Informative error messages
- Type-safe error responses

## License

This project is configured for internal customer service operations.