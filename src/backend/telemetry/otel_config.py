"""
OpenTelemetry configuration for Semker backend integration with .NET Aspire Dashboard
"""

import logging
import logging.handlers
import os
from pathlib import Path
from typing import Optional, Any
from opentelemetry import trace, metrics, _logs
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor  # type: ignore
from opentelemetry.instrumentation.requests import RequestsInstrumentor  # type: ignore
from opentelemetry.instrumentation.logging import LoggingInstrumentor  # type: ignore
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION, SERVICE_INSTANCE_ID
import uuid
from config.telemetry import telemetry_config

# Use string literals for resource attributes since semconv module structure has changed
SERVICE_NAMESPACE_KEY = "service.namespace"
DEPLOYMENT_ENVIRONMENT_KEY = "deployment.environment"

# Service information from config
SERVICE_NAME_VALUE = telemetry_config.SERVICE_NAME
SERVICE_VERSION_VALUE = telemetry_config.SERVICE_VERSION
SERVICE_INSTANCE_ID_VALUE = str(uuid.uuid4())

# Default OTLP endpoint for .NET Aspire Dashboard
DEFAULT_OTLP_ENDPOINT = telemetry_config.DEFAULT_OTLP_ENDPOINT


def setup_file_logging(log_level: str = "INFO") -> None:
    """
    Set up file logging for the backend service.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Create logs directory if it doesn't exist
    logs_dir = Path(telemetry_config.LOG_FOLDER)
    logs_dir.mkdir(exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove any existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create file handler with rotation
    log_file = logs_dir / f"{SERVICE_NAME_VALUE}.log"
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=telemetry_config.MAX_LOG_SIZE_MB * 1024 * 1024,
        backupCount=telemetry_config.LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    
    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    
    # Add handler to root logger
    root_logger.addHandler(file_handler)
    
    # Also set up a separate file for errors
    error_log_file = logs_dir / f"{SERVICE_NAME_VALUE}_errors.log"
    error_handler = logging.handlers.RotatingFileHandler(
        error_log_file,
        maxBytes=telemetry_config.MAX_LOG_SIZE_MB * 1024 * 1024,
        backupCount=telemetry_config.LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    root_logger.addHandler(error_handler)
    
    print(f"📝 File logging configured: {log_file}")
    print(f"🚨 Error logging configured: {error_log_file}")


def get_resource() -> Resource:
    """Create OpenTelemetry resource with service information."""
    return Resource.create({
        SERVICE_NAME: SERVICE_NAME_VALUE,
        SERVICE_VERSION: SERVICE_VERSION_VALUE,
        SERVICE_INSTANCE_ID: SERVICE_INSTANCE_ID_VALUE,
        SERVICE_NAMESPACE_KEY: telemetry_config.SERVICE_NAMESPACE,
        DEPLOYMENT_ENVIRONMENT_KEY: os.getenv("ENVIRONMENT", "development"),
    })


def configure_telemetry(
    otlp_endpoint: Optional[str] = None,
    enable_console: bool = False,
    enable_metrics: bool = True,
    enable_logging: bool = True,
    enable_tracing: bool = True,
    log_level: str = "INFO"
) -> None:
    """
    Configure OpenTelemetry for the Semker backend.
    
    Args:
        otlp_endpoint: OTLP endpoint URL (defaults to Aspire Dashboard endpoint)
        enable_console: Enable console exporter for debugging
        enable_metrics: Enable metrics collection
        enable_logging: Enable logging collection
        enable_tracing: Enable tracing collection
        log_level: File logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    if otlp_endpoint is None:
        otlp_endpoint = os.getenv("OTLP_ENDPOINT", DEFAULT_OTLP_ENDPOINT)
    
    # Set up file logging first
    setup_file_logging(log_level)
    
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
    Get a logger instance configured with OpenTelemetry and file logging.
    
    Args:
        name: Logger name (defaults to service name)
        
    Returns:
        Python Logger instance configured for file output
    """
    if name is None:
        name = SERVICE_NAME_VALUE
    
    logger = logging.getLogger(name)
    
    # Ensure logger doesn't propagate to avoid duplicate logs
    if name != SERVICE_NAME_VALUE:
        logger.propagate = True
    
    return logger


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


# Convenience function for easy backend logging setup
def init_backend_logging(log_level: str = "INFO") -> logging.Logger:
    """
    Initialize complete logging setup for the backend and return a logger.
    
    This is a convenience function that:
    1. Sets up file logging with rotation
    2. Configures OpenTelemetry
    3. Returns a configured logger
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        Configured logger instance
    """
    configure_telemetry(log_level=log_level)
    return get_logger()
