"""
Application constants - fixed values that never change
These are immutable values used throughout the application
"""

from typing import Final


class Routes:
    """API route path constants - these should never change"""
    
    ROOT: Final[str] = "/"
    DOCS: Final[str] = "/docs"
    SWAGGER: Final[str] = "/swagger" 
    REDOC: Final[str] = "/redoc"
    OPENAPI: Final[str] = "/openapi.json"
    
    # Health and system routes
    HEALTH: Final[str] = "/health"
    METRICS: Final[str] = "/metrics"
    
    # Message processing routes
    MESSAGES: Final[str] = "/messages"
    MESSAGE_STATUS: Final[str] = "/messages/{message_id}/status"
    MESSAGE_UPDATES: Final[str] = "/messages/{message_id}/updates"


class Tags:
    """OpenAPI documentation tag constants"""
    
    MESSAGES: Final[str] = "Messages"
    SYSTEM: Final[str] = "System" 
    DOCUMENTATION: Final[str] = "Documentation"
    HEALTH: Final[str] = "Health"


class HTTPMethods:
    """HTTP method constants"""
    
    GET: Final[str] = "GET"
    POST: Final[str] = "POST" 
    PUT: Final[str] = "PUT"
    PATCH: Final[str] = "PATCH"
    DELETE: Final[str] = "DELETE"
    HEAD: Final[str] = "HEAD"
    OPTIONS: Final[str] = "OPTIONS"


class StatusCodes:
    """Common HTTP status code constants"""
    
    # Success
    OK: Final[int] = 200
    CREATED: Final[int] = 201
    ACCEPTED: Final[int] = 202
    NO_CONTENT: Final[int] = 204
    
    # Client errors
    BAD_REQUEST: Final[int] = 400
    UNAUTHORIZED: Final[int] = 401
    FORBIDDEN: Final[int] = 403
    NOT_FOUND: Final[int] = 404
    METHOD_NOT_ALLOWED: Final[int] = 405
    CONFLICT: Final[int] = 409
    UNPROCESSABLE_ENTITY: Final[int] = 422
    TOO_MANY_REQUESTS: Final[int] = 429
    
    # Server errors
    INTERNAL_SERVER_ERROR: Final[int] = 500
    BAD_GATEWAY: Final[int] = 502
    SERVICE_UNAVAILABLE: Final[int] = 503
    GATEWAY_TIMEOUT: Final[int] = 504


class MessageStatus:
    """Message processing status constants"""
    
    RECEIVED: Final[str] = "received"
    PROCESSING: Final[str] = "processing" 
    PROCESSED: Final[str] = "processed"
    FAILED: Final[str] = "failed"
    CANCELLED: Final[str] = "cancelled"


class Summaries:
    """API endpoint summary constants for OpenAPI documentation"""
    
    SUBMIT_MESSAGE: Final[str] = "Submit a message for processing"
    GET_UPDATES: Final[str] = "Get processing updates for a message"
    GET_STATUS: Final[str] = "Get message status"
    LIST_MESSAGES: Final[str] = "List all messages"
    HEALTH_CHECK: Final[str] = "Health check endpoint"
    ROOT: Final[str] = "API root endpoint"
    SWAGGER_REDIRECT: Final[str] = "Redirect to Swagger UI"


class Descriptions:
    """API endpoint description constants for OpenAPI documentation"""
    
    SUBMIT_MESSAGE: Final[str] = "Submit a message that will be processed asynchronously in the background"
    GET_UPDATES: Final[str] = "Retrieve all processing updates for a specific message ID"
    GET_STATUS: Final[str] = "Get the current status and details of a specific message"
    LIST_MESSAGES: Final[str] = "Get a list of all messages in the system with their current status"
    HEALTH_CHECK: Final[str] = "Get the current health status and system information"
    ROOT: Final[str] = "Root endpoint that redirects to API documentation"
    SWAGGER_REDIRECT: Final[str] = "Alternative endpoint that redirects to Swagger documentation"


class ContentTypes:
    """HTTP content type constants"""
    
    JSON: Final[str] = "application/json"
    XML: Final[str] = "application/xml"
    HTML: Final[str] = "text/html"
    PLAIN_TEXT: Final[str] = "text/plain"
    FORM_DATA: Final[str] = "application/x-www-form-urlencoded"
    MULTIPART: Final[str] = "multipart/form-data"


class HeaderNames:
    """HTTP header name constants"""
    
    CONTENT_TYPE: Final[str] = "Content-Type"
    AUTHORIZATION: Final[str] = "Authorization"
    USER_AGENT: Final[str] = "User-Agent"
    ACCEPT: Final[str] = "Accept"
    CACHE_CONTROL: Final[str] = "Cache-Control"
    ETAG: Final[str] = "ETag"
    LAST_MODIFIED: Final[str] = "Last-Modified"
