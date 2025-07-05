"""
Telemetry middleware for FastAPI integration
"""

import time
from typing import Callable, Any
from fastapi import Request, Response
from starlette.routing import Match
from starlette.middleware.base import BaseHTTPMiddleware
from .otel_config import semker_metrics, get_tracer, get_logger
from config.telemetry import telemetry_config

# Get tracer and logger instances
tracer = get_tracer(telemetry_config.MIDDLEWARE_TRACER_NAME)
logger = get_logger(telemetry_config.MIDDLEWARE_LOGGER_NAME)


class TelemetryMiddleware(BaseHTTPMiddleware):
    """Middleware to collect custom telemetry data for Semker API."""
    
    async def dispatch(self, request: Request, call_next: Callable[[Request], Any]) -> Response:
        """Process request and collect telemetry data."""
        start_time = time.time()
        
        # Extract route information
        route_path = telemetry_config.UNKNOWN_ROUTE
        endpoint_name = telemetry_config.UNKNOWN_ENDPOINT
        
        for route in request.app.routes:
            match, _ = route.matches({"type": "http", "path": request.url.path, "method": request.method})
            if match == Match.FULL:
                route_path = route.path
                if hasattr(route, 'endpoint') and hasattr(route.endpoint, '__name__'):
                    endpoint_name = route.endpoint.__name__
                break
        
        # Create span for the request
        with tracer.start_as_current_span(
            f"{request.method} {route_path}",
            attributes={
                "http.method": request.method,
                "http.route": route_path,
                "http.url": str(request.url),
                "http.user_agent": request.headers.get(telemetry_config.USER_AGENT_HEADER, telemetry_config.DEFAULT_USER_AGENT),
                "semker.endpoint": endpoint_name,
                "semker.service": telemetry_config.MIDDLEWARE_SERVICE_NAME,
            }
        ) as span:
            
            # Record API request metric
            semker_metrics.record_api_request(
                endpoint=route_path,
                method=request.method,
                status_code=0  # Will be updated after response
            )
            
            # Log request
            logger.info(
                "API request received",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "route": route_path,
                    "endpoint": endpoint_name,
                    "user_agent": request.headers.get(telemetry_config.USER_AGENT_HEADER, telemetry_config.DEFAULT_USER_AGENT),
                }
            )
            
            try:
                # Process the request
                response: Response = await call_next(request)
                
                # Calculate processing time
                processing_time = time.time() - start_time
                
                # Update span with response information
                span.set_attribute("http.status_code", response.status_code)
                span.set_attribute("http.response_size", len(response.body) if hasattr(response, 'body') else 0)
                span.set_attribute("semker.processing_time", processing_time)
                
                # Record metrics
                semker_metrics.record_api_request(
                    endpoint=route_path,
                    method=request.method,
                    status_code=response.status_code
                )
                
                # Log response
                logger.info(
                    "API request completed",
                    extra={
                        "method": request.method,
                        "path": request.url.path,
                        "route": route_path,
                        "status_code": response.status_code,
                        "processing_time": processing_time,
                    }
                )
                
                return response
                
            except Exception as e:
                # Calculate processing time for failed requests
                processing_time = time.time() - start_time
                
                # Update span with error information
                span.set_attribute("error", True)
                span.set_attribute("error.type", type(e).__name__)
                span.set_attribute("error.message", str(e))
                span.set_attribute("semker.processing_time", processing_time)
                
                # Record error metrics
                semker_metrics.record_api_request(
                    endpoint=route_path,
                    method=request.method,
                    status_code=500
                )
                
                # Log error
                logger.error(
                    "API request failed",
                    extra={
                        "method": request.method,
                        "path": request.url.path,
                        "route": route_path,
                        "error_type": type(e).__name__,
                        "error_message": str(e),
                        "processing_time": processing_time,
                    },
                    exc_info=True
                )
                
                # Re-raise the exception to let FastAPI handle it
                raise
            finally:
                # End the span regardless of success or failure
                span.end()
