"""
Application constants for the Semker API.

This module defines all fixed values used throughout the application that
never change across different environments or deployments. These immutable
constants ensure consistency and prevent magic strings in the codebase.

Constant Classes:
    Routes: API route path definitions
    Tags: OpenAPI documentation tags
    HTTPMethods: HTTP method constants
    StatusCodes: HTTP status code constants
    MessageStatus: Message processing status constants
    Summaries: API endpoint summary descriptions
    Descriptions: API endpoint detailed descriptions
    ContentTypes: HTTP content type constants
    HeaderNames: HTTP header name constants

Features:
    - Type-safe constant definitions using Final
    - Centralized constant management
    - Immutable values that prevent accidental changes
    - Comprehensive HTTP and API-related constants
    - OpenAPI documentation strings

Usage:
    ```python
    from config.constants import Routes, MessageStatus
    
    # Route definitions
    messages_route = Routes.MESSAGES  # "/messages"
    
    # Status constants
    status = MessageStatus.RECEIVED  # "received"
    ```

Note:
    All constants in this module use typing.Final to ensure immutability
    and provide type safety. These values should never be modified at runtime.
"""

from typing import Final


class Routes:
    """
    API route path constants for endpoint definitions.

    This class defines all URL paths used in the API routing system.
    These paths are immutable and provide a single source of truth
    for all endpoint definitions.

    Route Categories:
        - Root and documentation routes
        - Health and system monitoring routes  
        - Message processing routes

    Example:
        ```python
        from config.constants import Routes
        
        @app.get(Routes.HEALTH)
        async def health_check():
            return {"status": "healthy"}
        ```
    """
    
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
    """
    OpenAPI documentation tag constants for endpoint grouping.

    This class defines tags used to group related endpoints in the
    OpenAPI documentation interface. Tags help organize the API
    documentation into logical sections.

    Tag Categories:
        - Messages: Message processing endpoints
        - System: System and health endpoints
        - Documentation: Documentation-related endpoints
        - Health: Health check endpoints

    Example:
        ```python
        from config.constants import Tags
        
        @app.get("/messages", tags=[Tags.MESSAGES])
        async def list_messages():
            return {"messages": []}
        ```
    """
    
    MESSAGES: Final[str] = "Messages"
    SYSTEM: Final[str] = "System" 
    DOCUMENTATION: Final[str] = "Documentation"
    HEALTH: Final[str] = "Health"


class HTTPMethods:
    """
    HTTP method constants for request type definitions.

    This class provides constants for all standard HTTP methods used
    in REST API development. Using these constants ensures consistency
    and prevents typos in method names.

    Supported Methods:
        - GET: Retrieve data
        - POST: Create new resources
        - PUT: Update entire resources
        - PATCH: Update partial resources
        - DELETE: Remove resources
        - HEAD: Get headers only
        - OPTIONS: Check allowed methods

    Example:
        ```python
        from config.constants import HTTPMethods
        
        # Instead of using string literals
        method = HTTPMethods.POST  # "POST"
        ```
    """
    
    GET: Final[str] = "GET"
    POST: Final[str] = "POST" 
    PUT: Final[str] = "PUT"
    PATCH: Final[str] = "PATCH"
    DELETE: Final[str] = "DELETE"
    HEAD: Final[str] = "HEAD"
    OPTIONS: Final[str] = "OPTIONS"


class StatusCodes:
    """
    HTTP status code constants for response handling.

    This class provides constants for commonly used HTTP status codes
    in REST API responses. Using these constants improves code readability
    and ensures consistent status code usage.

    Status Categories:
        - 2xx Success: OK, CREATED, ACCEPTED, NO_CONTENT
        - 4xx Client Errors: BAD_REQUEST, UNAUTHORIZED, FORBIDDEN, NOT_FOUND, etc.
        - 5xx Server Errors: INTERNAL_SERVER_ERROR, BAD_GATEWAY, etc.

    Example:
        ```python
        from config.constants import StatusCodes
        
        raise HTTPException(
            status_code=StatusCodes.NOT_FOUND,
            detail="Resource not found"
        )
        ```
    """
    
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
    """
    Message processing status constants for state tracking.

    This class defines all possible states that a message can be in
    during its processing lifecycle. These constants ensure consistent
    status reporting across the application.

    Status Flow:
        RECEIVED → IN_PROGRESS → COMPLETED/FAILED/CANCELLED

    Status Definitions:
        - RECEIVED: Message has been received and queued
        - IN_PROGRESS: Message is currently being processed
        - COMPLETED: Message processing finished successfully
        - FAILED: Message processing encountered an error
        - CANCELLED: Message processing was cancelled

    Example:
        ```python
        from config.constants import MessageStatus
        
        message_status = MessageStatus.RECEIVED  # "received"
        
        if status == MessageStatus.COMPLETED:
            # Handle successful processing
            pass
        ```
    """
    
    RECEIVED: Final[str] = "received"
    IN_PROGRESS: Final[str] = "inprogress" 
    COMPLETED: Final[str] = "completed"
    FAILED: Final[str] = "failed"
    CANCELLED: Final[str] = "cancelled"


class Summaries:
    """
    API endpoint summary constants for OpenAPI documentation.

    This class provides brief, descriptive summaries for each API endpoint
    that appear in the OpenAPI documentation. These summaries give users
    a quick understanding of what each endpoint does.

    Usage:
        These constants are used in FastAPI route decorators to provide
        consistent and professional API documentation.

    Example:
        ```python
        from config.constants import Summaries
        
        @app.post("/messages", summary=Summaries.SUBMIT_MESSAGE)
        async def submit_message():
            pass
        ```
    """
    
    SUBMIT_MESSAGE: Final[str] = "Submit a message for processing"
    GET_UPDATES: Final[str] = "Get processing updates for a message"
    GET_STATUS: Final[str] = "Get message status"
    LIST_MESSAGES: Final[str] = "List all messages"
    HEALTH_CHECK: Final[str] = "Health check endpoint"
    ROOT: Final[str] = "API root endpoint"
    SWAGGER_REDIRECT: Final[str] = "Redirect to Swagger UI"


class Descriptions:
    """
    API endpoint detailed description constants for OpenAPI documentation.

    This class provides comprehensive descriptions for each API endpoint
    that appear in the OpenAPI documentation. These descriptions give users
    detailed information about endpoint behavior, parameters, and usage.

    Usage:
        These constants are used in FastAPI route decorators to provide
        thorough documentation that helps developers understand and use the API.

    Example:
        ```python
        from config.constants import Descriptions
        
        @app.post("/messages", description=Descriptions.SUBMIT_MESSAGE)
        async def submit_message():
            pass
        ```
    """
    
    SUBMIT_MESSAGE: Final[str] = "Submit a message that will be processed asynchronously in the background"
    GET_UPDATES: Final[str] = "Retrieve all processing updates for a specific message ID"
    GET_STATUS: Final[str] = "Get the current status and details of a specific message"
    LIST_MESSAGES: Final[str] = "Get a list of all messages in the system with their current status"
    HEALTH_CHECK: Final[str] = "Get the current health status and system information"
    ROOT: Final[str] = "Root endpoint that redirects to API documentation"
    SWAGGER_REDIRECT: Final[str] = "Alternative endpoint that redirects to Swagger documentation"


class ContentTypes:
    """
    HTTP content type constants for request and response headers.

    This class provides constants for commonly used MIME types in HTTP
    communications. Using these constants ensures consistent content type
    handling throughout the application.

    Content Type Categories:
        - JSON: application/json (most common for REST APIs)
        - XML: application/xml
        - HTML: text/html
        - Plain text: text/plain
        - Form data: application/x-www-form-urlencoded, multipart/form-data

    Example:
        ```python
        from config.constants import ContentTypes
        
        response.headers["Content-Type"] = ContentTypes.JSON
        ```
    """
    
    JSON: Final[str] = "application/json"
    XML: Final[str] = "application/xml"
    HTML: Final[str] = "text/html"
    PLAIN_TEXT: Final[str] = "text/plain"
    FORM_DATA: Final[str] = "application/x-www-form-urlencoded"
    MULTIPART: Final[str] = "multipart/form-data"


class HeaderNames:
    """
    HTTP header name constants for request and response handling.

    This class provides constants for commonly used HTTP header names
    to ensure consistent header handling and prevent typos in header
    name strings throughout the application.

    Header Categories:
        - Content handling: Content-Type, Accept, Cache-Control
        - Authentication: Authorization
        - Client information: User-Agent
        - Caching: ETag, Last-Modified, Cache-Control

    Example:
        ```python
        from config.constants import HeaderNames
        
        auth_header = request.headers.get(HeaderNames.AUTHORIZATION)
        ```
    """
    
    CONTENT_TYPE: Final[str] = "Content-Type"
    AUTHORIZATION: Final[str] = "Authorization"
    USER_AGENT: Final[str] = "User-Agent"
    ACCEPT: Final[str] = "Accept"
    CACHE_CONTROL: Final[str] = "Cache-Control"
    ETAG: Final[str] = "ETag"
    LAST_MODIFIED: Final[str] = "Last-Modified"
