# MCP Server - Customer Service Tools

A FastAPI-based Model Context Protocol (MCP) server providing customer service tools for billing, roaming, broadband troubleshooting, and ticket management, with comprehensive telemetry integration.

## Features

- **Billing Management**: Retrieve customer billing data and line items
- **Roaming Services**: Get roaming charges by country and month
- **Broadband Support**: Troubleshooting steps for different router models
- **Ticket Management**: Create and manage support tickets with consent tracking
- **Tariff Information**: Access tariff offers and usage details
- **Telemetry Integration**: OpenTelemetry observability with Aspire Dashboard support

## Project Structure

```
src/
├── main.py                 # Main FastAPI application with telemetry
├── pyproject.toml         # Project configuration and dependencies
├── telemetry/             # Telemetry and logging modules
│   ├── __init__.py        # Telemetry setup coordinator
│   ├── aspire.py          # Aspire Dashboard integration
│   └── hooks.py           # Custom OpenTelemetry hooks
└── tools/                 # MCP tool implementations
    ├── billing.py         # Customer billing data tool
    ├── broadband.py       # Broadband troubleshooting tool
    ├── roaming.py         # Roaming charges tool
    ├── tarriff.py         # Tariff and usage data tool
    └── ticket.py          # Support ticket management tool
```

## Development Setup

### Prerequisites

- Python 3.11+
- uv (Python package installer)

### Installation

1. Install dependencies:
```bash
uv sync
```

2. Run the application:
```bash
uv run python main.py
```

## API Endpoints

The application mounts the following MCP tools:

- `/bill` - Billing data retrieval
- `/roam` - Roaming charges information
- `/broadband` - Troubleshooting support
- `/ticket` - Support ticket management

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
- `LineItem`: Individual billing line items
- `Bill`: Monthly bill with line items
- `BillingData`: Container for billing information

### Roaming
- `Charges`: Monthly roaming charges by country
- `RoamingCharges`: Container for roaming data

### Broadband
- `TroubleshootingModel`: Router-specific troubleshooting steps
- `Troubleshooting`: Container for troubleshooting information

### Tickets
- `TicketResponse`: Support ticket creation response

### Tariffs
- `TariffData`: Tariff offer information
- `MonthlyUsage`: Monthly usage breakdown
- `UsageDetails`: Detailed usage information

## Error Handling

All tools include comprehensive error handling with:
- Input validation for parameters
- Proper exception chaining
- Informative error messages
- Type-safe error responses

## License

This project is configured for internal customer service operations.