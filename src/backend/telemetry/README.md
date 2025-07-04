# Semker Backend - OpenTelemetry Integration with .NET Aspire Dashboard

This document describes the OpenTelemetry telemetry integration that enables monitoring and observability of the Semker backend through the .NET Aspire Dashboard.

## Features

### 🔭 **Distributed Tracing**
- **Request tracing**: Every API request is traced with detailed timing and context
- **Custom spans**: Message processing operations are instrumented with custom spans
- **Error tracking**: Failed requests and exceptions are captured with full context
- **Service correlation**: All operations are correlated with the `semker-backend` service

### 📊 **Metrics Collection**
- **API request metrics**: Count and timing of all API endpoints
- **Message processing metrics**: Statistics on message reception and processing
- **System metrics**: Active message counts and processing durations
- **Custom business metrics**: Semker-specific operational metrics

### 📝 **Structured Logging**
- **Contextual logs**: All logs include trace and span context for correlation
- **Request/response logging**: API request details and outcomes
- **Error logging**: Detailed error information with stack traces
- **Performance logging**: Processing times and system events

## Architecture

```
┌─────────────────┐    OTLP/gRPC     ┌──────────────────┐
│  Semker Backend │ ────────────────▶│ .NET Aspire      │
│                 │    Port 4317     │ Dashboard        │
│ ┌─────────────┐ │                  │                  │
│ │ OpenTelemetry│ │                  │ ┌──────────────┐ │
│ │ SDK         │ │                  │ │ Traces       │ │
│ │             │ │                  │ │ Metrics      │ │
│ │ • Tracing   │ │                  │ │ Logs         │ │
│ │ • Metrics   │ │                  │ │ Dashboard    │ │
│ │ • Logging   │ │                  │ └──────────────┘ │
│ └─────────────┘ │                  └──────────────────┘
└─────────────────┘                           │
                                              │ Port 18888
                                              ▼
                                    ┌──────────────────┐
                                    │   Web Dashboard  │
                                    │  http://localhost│
                                    │      :18888      │
                                    └──────────────────┘
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `TELEMETRY_ENABLED` | `true` | Enable/disable telemetry collection |
| `OTLP_ENDPOINT` | `http://localhost:4317` | OpenTelemetry collector endpoint |
| `TELEMETRY_CONSOLE` | `false` | Enable console output for debugging |
| `ENVIRONMENT` | `development` | Deployment environment name |

### Resource Attributes

The service is identified with these attributes:
- **Service Name**: `semker-backend`
- **Service Version**: `0.1.0`
- **Service Namespace**: `semker`
- **Service Instance ID**: Unique UUID per instance
- **Deployment Environment**: From `ENVIRONMENT` variable

## Usage

### Starting with Telemetry

#### Option 1: Using the Aspire Script (Recommended)
```bash
./scripts/start-with-aspire.sh
```

#### Option 2: Manual Configuration
```bash
export TELEMETRY_ENABLED=true
export OTLP_ENDPOINT=http://localhost:4317
uv run python main.py
```

#### Option 3: Disable Telemetry
```bash
export TELEMETRY_ENABLED=false
uv run python main.py
```

### .NET Aspire Dashboard Setup

1. **Install .NET Aspire** (requires .NET 8.0+):
   ```bash
   dotnet workload install aspire
   ```

2. **Create Aspire project**:
   ```bash
   dotnet new aspire-starter -n SemkerObservability
   cd SemkerObservability
   ```

3. **Start the dashboard**:
   ```bash
   dotnet run --project SemkerObservability.AppHost
   ```

4. **Access the dashboard**: http://localhost:18888

## Telemetry Data

### Traces

**HTTP Request Spans**:
- Span Name: `{METHOD} {route}`
- Attributes:
  - `http.method`: HTTP method
  - `http.route`: API route pattern
  - `http.url`: Full request URL
  - `http.status_code`: Response status
  - `http.user_agent`: Client user agent
  - `semker.endpoint`: Handler function name
  - `semker.service`: Always `backend`
  - `semker.processing_time`: Request duration

**Message Processing Spans**:
- Message submission operations
- Background processing tasks
- Database/storage operations

### Metrics

**API Metrics**:
- `semker_api_requests_total`: Total API requests by endpoint, method, status
- `semker_messages_received_total`: Messages received by type
- `semker_messages_processed_total`: Messages processed by type and status
- `semker_message_processing_duration_seconds`: Processing time histogram
- `semker_active_messages`: Current active message count

### Logs

**Request Logs**:
```json
{
  "timestamp": "2025-07-04T13:00:00Z",
  "level": "INFO",
  "message": "API request received",
  "method": "POST",
  "path": "/messages",
  "route": "/messages",
  "endpoint": "receive_message",
  "user_agent": "curl/7.68.0",
  "trace_id": "abc123...",
  "span_id": "def456..."
}
```

**Error Logs**:
```json
{
  "timestamp": "2025-07-04T13:00:00Z",
  "level": "ERROR", 
  "message": "API request failed",
  "method": "GET",
  "path": "/messages/invalid-id/status",
  "route": "/messages/{message_id}/status",
  "error_type": "KeyError",
  "error_message": "Message not found",
  "processing_time": 0.045,
  "trace_id": "abc123...",
  "span_id": "def456..."
}
```

## Middleware

The `TelemetryMiddleware` automatically:
- Creates spans for each HTTP request
- Extracts route information for better grouping
- Records timing and response metrics
- Logs request/response details
- Handles error scenarios gracefully
- Correlates all telemetry data with trace context

## Custom Instrumentation

### Adding Custom Spans

```python
from telemetry import get_tracer

tracer = get_tracer("my.component")

with tracer.start_as_current_span("custom_operation") as span:
    span.set_attribute("custom.attribute", "value")
    # Your code here
```

### Recording Custom Metrics

```python
from telemetry import semker_metrics

# Record a message received
semker_metrics.record_message_received("text")

# Record processing duration
semker_metrics.record_processing_duration(1.5, "text")
```

### Custom Logging

```python
from telemetry import get_logger

logger = get_logger("my.component")
logger.info("Custom log message", extra={"custom_field": "value"})
```

## Dashboard Views

### In .NET Aspire Dashboard you can view:

1. **Traces Tab**: 
   - Request traces with timing breakdown
   - Distributed trace visualization
   - Error tracking and analysis

2. **Metrics Tab**:
   - Real-time metrics charts
   - Custom Semker business metrics
   - Performance indicators

3. **Logs Tab**:
   - Structured log search and filtering
   - Correlated logs by trace ID
   - Error log analysis

4. **Services Tab**:
   - Service health overview
   - Resource utilization
   - Deployment information

## Troubleshooting

### Common Issues

1. **Telemetry not appearing in dashboard**:
   - Check OTLP endpoint: `curl http://localhost:4317`
   - Verify Aspire dashboard is running: `curl http://localhost:18888`
   - Check environment variables

2. **High telemetry overhead**:
   - Disable console output: `TELEMETRY_CONSOLE=false`
   - Adjust export intervals in configuration
   - Consider sampling for high-traffic scenarios

3. **Missing traces/metrics**:
   - Ensure telemetry is enabled: `TELEMETRY_ENABLED=true`
   - Check for import errors in logs
   - Verify OpenTelemetry package versions

### Debug Mode

Enable console output for debugging:
```bash
export TELEMETRY_CONSOLE=true
export LOG_LEVEL=debug
```

This will output telemetry data to the console in addition to sending to Aspire.

## Performance Considerations

- **Minimal overhead**: OpenTelemetry is designed for production use
- **Asynchronous export**: Telemetry data is exported in background
- **Sampling support**: Can be configured for high-volume scenarios
- **Graceful degradation**: Application continues working if telemetry fails

## Integration Benefits

✅ **End-to-end observability** of API requests and message processing  
✅ **Performance monitoring** with detailed timing metrics  
✅ **Error tracking** with full context and stack traces  
✅ **Business insights** through custom metrics  
✅ **Operational dashboards** via .NET Aspire  
✅ **Production-ready** observability stack  
✅ **Easy debugging** with correlated logs and traces
