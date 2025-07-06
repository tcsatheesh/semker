"""
File logging setup for the backend service.

This module provides configuration for both standard Python logging and OpenTelemetry
logging capabilities for the semantic kernel backend.
"""
import json
import logging
import logging.handlers
import time
from typing import Any
from pathlib import Path

from opentelemetry._logs import set_logger_provider
from opentelemetry.metrics import set_meter_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, LogExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    PeriodicExportingMetricReader,
    MetricExporter,
    MetricExportResult,
)
from opentelemetry.sdk.metrics.view import DropAggregation, View
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SpanExporter, SpanExportResult
from opentelemetry.trace import set_tracer_provider

from config.telemetry import telemetry_config

# OpenTelemetry resource for the service
_RESOURCE = Resource.create({
    "service.name": telemetry_config.SERVICE_NAME_VALUE
})


class FileLogExporter(LogExporter):
    """Custom log exporter that writes OpenTelemetry logs to a file."""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        
    def export(self, batch: Any):
        """Export log records to file."""
        try:
            with open(self.file_path, 'a', encoding='utf-8') as f:
                for log_record in batch:
                    # Simple log format
                    timestamp = getattr(log_record, 'timestamp', time.time_ns())
                    level = getattr(log_record, 'severity_text', 'INFO')
                    message = str(getattr(log_record, 'body', ''))
                    
                    log_data = {
                        "timestamp": timestamp,
                        "level": level,
                        "message": message,
                        "source": "opentelemetry"
                    }
                    f.write(json.dumps(log_data) + '\n')
        except Exception as e:
            print(f"Failed to export logs: {e}")
    
    def shutdown(self):
        """Shutdown the exporter."""
        pass


class FileSpanExporter(SpanExporter):
    """Custom span exporter that writes OpenTelemetry spans to a file."""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        
    def export(self, spans: Any):
        """Export spans to file."""
        try:
            with open(self.file_path, 'a', encoding='utf-8') as f:
                for span in spans:
                    # Simple span format
                    name = getattr(span, 'name', 'unknown')
                    start_time = getattr(span, 'start_time', time.time_ns())
                    end_time = getattr(span, 'end_time', start_time)
                    
                    span_data = {
                        "timestamp": start_time,
                        "name": name,
                        "duration_ns": end_time - start_time if end_time else 0,
                        "source": "opentelemetry"
                    }
                    f.write(json.dumps(span_data) + '\n')
            return SpanExportResult.SUCCESS
        except Exception as e:
            print(f"Failed to export spans: {e}")
            return SpanExportResult.FAILURE
    
    def shutdown(self):
        """Shutdown the exporter."""
        pass


class FileMetricExporter(MetricExporter):
    """Custom metric exporter that writes OpenTelemetry metrics to a file."""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        
    def export(self, metrics_data: Any, timeout_millis: float = 30000, **kwargs: Any):
        """Export metrics to file."""
        try:
            with open(self.file_path, 'a', encoding='utf-8') as f:
                # Simple metric format
                metric_data = {
                    "timestamp": int(time.time() * 1000),
                    "type": "metrics_batch",
                    "count": len(getattr(metrics_data, 'resource_metrics', [])),
                    "source": "opentelemetry"
                }
                f.write(json.dumps(metric_data) + '\n')
            return MetricExportResult.SUCCESS
        except Exception as e:
            print(f"Failed to export metrics: {e}")
            return MetricExportResult.FAILURE
    
    def shutdown(self, timeout_millis: float = 30000, **kwargs: Any):
        """Shutdown the exporter."""
        pass
        
    def force_flush(self, timeout_millis: float = 30000):
        """Force flush the exporter."""
        return True


def setup_file_logging(log_level: str = "INFO") -> None:
    """
    Set up file-based logging for the backend service.
    
    Creates rotating log files for general logs and error logs with proper
    formatting and filtering.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Raises:
        OSError: If log directory cannot be created
        ValueError: If log_level is invalid
    """
    try:
        # Validate log level
        numeric_level = getattr(logging, log_level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError(f"Invalid log level: {log_level}")
        
        # Create logs directory
        logs_dir = Path(telemetry_config.LOG_FOLDER)
        logs_dir.mkdir(parents=True, exist_ok=True)

        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(numeric_level)

        # Clear existing handlers to avoid duplicates
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # Create formatter for consistent log format
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Set up main log file with rotation
        main_log_file = logs_dir / f"{telemetry_config.SERVICE_NAME_VALUE}.log"
        main_handler = logging.handlers.RotatingFileHandler(
            main_log_file,
            maxBytes=telemetry_config.MAX_LOG_SIZE_MB * 1024 * 1024,
            backupCount=telemetry_config.LOG_BACKUP_COUNT,
            encoding="utf-8",
        )
        main_handler.setFormatter(formatter)
        
        # Apply log filter if configured
        if hasattr(telemetry_config, 'LOG_FILTER_NAME') and telemetry_config.LOG_FILTER_NAME:
            main_handler.addFilter(logging.Filter(telemetry_config.LOG_FILTER_NAME))
        
        root_logger.addHandler(main_handler)

        # Set up separate error log file
        error_log_file = logs_dir / f"{telemetry_config.SERVICE_NAME_VALUE}_errors.log"
        error_handler = logging.handlers.RotatingFileHandler(
            error_log_file,
            maxBytes=telemetry_config.MAX_LOG_SIZE_MB * 1024 * 1024,
            backupCount=telemetry_config.LOG_BACKUP_COUNT,
            encoding="utf-8",
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        root_logger.addHandler(error_handler)

        print(f"📝 File logging configured: {main_log_file}")
        print(f"🚨 Error logging configured: {error_log_file}")
        
    except Exception as e:
        print(f"❌ Failed to setup file logging: {e}")
        raise


def set_up_logging() -> None:
    """
    Set up OpenTelemetry logging with file export.
    
    This configures OpenTelemetry's logging infrastructure for structured
    telemetry data collection and writes to a file.
    """
    try:
        # Create logs directory
        logs_dir = Path(telemetry_config.LOG_FOLDER)
        logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Create file exporter
        otel_log_file = logs_dir / "opentelemetry_logs.jsonl"
        exporter = FileLogExporter(otel_log_file)

        # Create and configure logger provider
        logger_provider = LoggerProvider(resource=_RESOURCE)
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
        set_logger_provider(logger_provider)

        # Create OpenTelemetry logging handler
        otel_handler = LoggingHandler()
        
        # Attach to root logger for OpenTelemetry integration
        logger = logging.getLogger()
        logger.addHandler(otel_handler)
        
        print(f"🔧 OpenTelemetry logging configured: {otel_log_file}")
        
    except Exception as e:
        print(f"❌ Failed to setup OpenTelemetry logging: {e}")
        raise


def set_up_tracing() -> None:
    """
    Set up OpenTelemetry tracing with file export.
    
    This configures distributed tracing capabilities for the service
    and writes to a file.
    """
    try:
        # Create logs directory
        logs_dir = Path(telemetry_config.LOG_FOLDER)
        logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Create file exporter
        otel_trace_file = logs_dir / "opentelemetry_traces.jsonl"
        exporter = FileSpanExporter(otel_trace_file)

        # Initialize tracer provider
        tracer_provider = TracerProvider(resource=_RESOURCE)
        tracer_provider.add_span_processor(BatchSpanProcessor(exporter))
        set_tracer_provider(tracer_provider)
        
        print(f"🔍 OpenTelemetry tracing configured: {otel_trace_file}")
        
    except Exception as e:
        print(f"❌ Failed to setup OpenTelemetry tracing: {e}")
        raise


def set_up_metrics() -> None:
    """
    Set up OpenTelemetry metrics with file export.
    
    This configures metrics collection and export, with views to filter
    metrics to semantic_kernel related instruments only and writes to a file.
    """
    try:
        # Create logs directory
        logs_dir = Path(telemetry_config.LOG_FOLDER)
        logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Create file exporter
        otel_metrics_file = logs_dir / "opentelemetry_metrics.jsonl"
        exporter = FileMetricExporter(otel_metrics_file)

        # Initialize meter provider with filtering views
        meter_provider = MeterProvider(
            metric_readers=[
                PeriodicExportingMetricReader(exporter, export_interval_millis=5000)
            ],
            resource=_RESOURCE,
            views=[
                # Drop all instruments except semantic_kernel related ones
                View(instrument_name="*", aggregation=DropAggregation()),
                View(instrument_name="semantic_kernel*"),
            ],
        )
        set_meter_provider(meter_provider)
        
        print(f"📊 OpenTelemetry metrics configured: {otel_metrics_file}")
        
    except Exception as e:
        print(f"❌ Failed to setup OpenTelemetry metrics: {e}")
        raise

setup_file_logging(telemetry_config.LOG_LEVEL)
set_up_logging()
set_up_tracing()
# set_up_metrics()
    
print("✅ Telemetry initialization complete")


