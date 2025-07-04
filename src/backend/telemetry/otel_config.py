"""
OpenTelemetry configuration for Semker backend integration with .NET Aspire Dashboard
"""

import logging
import os
from typing import Optional, Dict, Any
from opentelemetry import trace, metrics, _logs
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION, SERVICE_INSTANCE_ID
import uuid

# Use string literals for resource attributes since semconv module structure has changed
SERVICE_NAMESPACE_KEY = "service.namespace"
DEPLOYMENT_ENVIRONMENT_KEY = "deployment.environment"

# Service information
SERVICE_NAME_VALUE = "semker-backend"
SERVICE_VERSION_VALUE = "0.1.0"
SERVICE_INSTANCE_ID_VALUE = str(uuid.uuid4())

# Default OTLP endpoint for .NET Aspire Dashboard
DEFAULT_OTLP_ENDPOINT = "http://localhost:4317"


def get_resource() -> Resource:
    """Create OpenTelemetry resource with service information."""
    return Resource.create({
        SERVICE_NAME: SERVICE_NAME_VALUE,
        SERVICE_VERSION: SERVICE_VERSION_VALUE,
        SERVICE_INSTANCE_ID: SERVICE_INSTANCE_ID_VALUE,
        SERVICE_NAMESPACE_KEY: "semker",
        DEPLOYMENT_ENVIRONMENT_KEY: os.getenv("ENVIRONMENT", "development"),
    })


def configure_telemetry(
    otlp_endpoint: Optional[str] = None,
    enable_console: bool = False,
    enable_metrics: bool = True,
    enable_logging: bool = True,
    enable_tracing: bool = True
) -> None:
    """
    Configure OpenTelemetry for the Semker backend.
    
    Args:
        otlp_endpoint: OTLP endpoint URL (defaults to Aspire Dashboard endpoint)
        enable_console: Enable console exporter for debugging
        enable_metrics: Enable metrics collection
        enable_logging: Enable logging collection
        enable_tracing: Enable tracing collection
    """
    if otlp_endpoint is None:
        otlp_endpoint = os.getenv("OTLP_ENDPOINT", DEFAULT_OTLP_ENDPOINT)
    
    resource = get_resource()
    
    # Configure Tracing
    if enable_tracing:
        trace_provider = TracerProvider(resource=resource)
        
        # OTLP Span Exporter
        otlp_span_exporter = OTLPSpanExporter(
            endpoint=otlp_endpoint,
            insecure=True  # For local development with Aspire
        )
        span_processor = BatchSpanProcessor(otlp_span_exporter)
        trace_provider.add_span_processor(span_processor)
        
        # Console exporter for debugging (optional)
        if enable_console:
            print("Console exporter not available, using OTLP only")
        
        trace.set_tracer_provider(trace_provider)
    
    # Configure Metrics
    if enable_metrics:
        metric_reader = PeriodicExportingMetricReader(
            OTLPMetricExporter(
                endpoint=otlp_endpoint,
                insecure=True
            ),
            export_interval_millis=5000,  # Export every 5 seconds
        )
        
        metric_provider = MeterProvider(
            resource=resource,
            metric_readers=[metric_reader]
        )
        metrics.set_meter_provider(metric_provider)
    
    # Configure Logging
    if enable_logging:
        logger_provider = LoggerProvider(resource=resource)
        
        # OTLP Log Exporter
        otlp_log_exporter = OTLPLogExporter(
            endpoint=otlp_endpoint,
            insecure=True
        )
        log_processor = BatchLogRecordProcessor(otlp_log_exporter)
        logger_provider.add_log_record_processor(log_processor)
        
        _logs.set_logger_provider(logger_provider)
        
        # Configure Python logging to use OpenTelemetry
        LoggingInstrumentor().instrument(set_logging_format=True)
    
    print(f"🔭 OpenTelemetry configured for Aspire Dashboard at {otlp_endpoint}")


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


def _server_request_hook(span: Any, scope: Dict[str, Any]) -> None:
    """Add custom attributes to server request spans."""
    if span and hasattr(span, 'is_recording') and span.is_recording():
        # Add custom attributes
        if hasattr(span, 'set_attribute'):
            span.set_attribute("semker.service", "backend")
            span.set_attribute("semker.version", SERVICE_VERSION_VALUE)
            
            # Add request information
            if "path" in scope:
                span.set_attribute("http.route", scope["path"])


def _client_request_hook(span: Any, request: Any) -> None:
    """Add custom attributes to client request spans."""
    if span and hasattr(span, 'is_recording') and span.is_recording():
        if hasattr(span, 'set_attribute'):
            span.set_attribute("semker.client", "requests")


def get_tracer(name: Optional[str] = None) -> trace.Tracer:
    """
    Get a tracer instance.
    
    Args:
        name: Tracer name (defaults to service name)
        
    Returns:
        OpenTelemetry Tracer instance
    """
    if name is None:
        name = SERVICE_NAME_VALUE
    return trace.get_tracer(name, SERVICE_VERSION_VALUE)


def get_meter(name: Optional[str] = None) -> metrics.Meter:
    """
    Get a meter instance.
    
    Args:
        name: Meter name (defaults to service name)
        
    Returns:
        OpenTelemetry Meter instance
    """
    if name is None:
        name = SERVICE_NAME_VALUE
    return metrics.get_meter(name, SERVICE_VERSION_VALUE)


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance configured with OpenTelemetry.
    
    Args:
        name: Logger name (defaults to service name)
        
    Returns:
        Python Logger instance
    """
    if name is None:
        name = SERVICE_NAME_VALUE
    return logging.getLogger(name)


# Custom metrics for Semker backend
class SemkerMetrics:
    """Custom metrics for the Semker backend service."""
    
    def __init__(self) -> None:
        self.meter = get_meter("semker.metrics")
        
        # Counters
        self.messages_received = self.meter.create_counter(
            "semker_messages_received_total",
            description="Total number of messages received",
            unit="1"
        )
        
        self.messages_processed = self.meter.create_counter(
            "semker_messages_processed_total", 
            description="Total number of messages processed",
            unit="1"
        )
        
        self.api_requests = self.meter.create_counter(
            "semker_api_requests_total",
            description="Total number of API requests",
            unit="1"
        )
        
        # Histograms
        self.message_processing_duration = self.meter.create_histogram(
            "semker_message_processing_duration_seconds",
            description="Time taken to process messages",
            unit="s"
        )
        
        # Gauges
        self.active_messages = self.meter.create_up_down_counter(
            "semker_active_messages",
            description="Number of messages currently being processed",
            unit="1"
        )
    
    def record_message_received(self, message_type: str = "unknown") -> None:
        """Record a message received event."""
        self.messages_received.add(1, {"message_type": message_type})
    
    def record_message_processed(self, message_type: str = "unknown", status: str = "success") -> None:
        """Record a message processed event."""
        self.messages_processed.add(1, {"message_type": message_type, "status": status})
    
    def record_api_request(self, endpoint: str, method: str, status_code: int) -> None:
        """Record an API request event."""
        self.api_requests.add(1, {
            "endpoint": endpoint,
            "method": method, 
            "status_code": str(status_code)
        })
    
    def record_processing_duration(self, duration_seconds: float, message_type: str = "unknown") -> None:
        """Record message processing duration."""
        self.message_processing_duration.record(duration_seconds, {"message_type": message_type})
    
    def increment_active_messages(self) -> None:
        """Increment active messages counter."""
        self.active_messages.add(1)
    
    def decrement_active_messages(self) -> None:
        """Decrement active messages counter."""
        self.active_messages.add(-1)


# Global metrics instance
semker_metrics = SemkerMetrics()
