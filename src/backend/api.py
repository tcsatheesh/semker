"""
Main FastAPI application for Semker Async Message Processing API.

This module provides the main FastAPI application with all API endpoints for
asynchronous message processing. It includes comprehensive OpenAPI documentation,
CORS middleware, and telemetry instrumentation.

The application handles:
- Message submission and processing with real-time status updates
- Health monitoring and system status
- Interactive API documentation
- Background task processing with AI agents
- Conversation thread management

Main Components:
- FastAPI app with OpenAPI documentation
- CORS middleware for cross-origin requests
- Message processing endpoints
- Health check endpoints
- Documentation endpoints
- Telemetry instrumentation

Example Usage:
    Run the application with:
    ```bash
    uvicorn api:app --host 0.0.0.0 --port 8000 --reload
    ```

    Access documentation at:
    - http://localhost:8000/docs (Swagger UI)
    - http://localhost:8000/redoc (ReDoc)
"""

from telemetry import instrument_fastapi

from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request, status
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from models import Message, MessageResponse, UpdateResponse, HealthResponse
from process import MessageProcessor
from config import (
    APISettings, ContactSettings, LicenseSettings, ServerSettings,
    Routes, Tags, Summaries, Descriptions
)

# Initialize the message processor
message_processor = MessageProcessor()

# FastAPI app with comprehensive OpenAPI documentation
app = FastAPI(
    title=APISettings.TITLE,
    description=APISettings.DESCRIPTION,
    version=APISettings.VERSION,
    contact={
        "name": ContactSettings.NAME,
        "email": ContactSettings.EMAIL,
    },
    license_info={
        "name": LicenseSettings.NAME,
        "url": LicenseSettings.URL,
    },
    servers=[
        {
            "url": ServerSettings.DEFAULT_URL,
            "description": ServerSettings.DEFAULT_DESCRIPTION
        }
    ]
)

instrument_fastapi(app)

# Add CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=ServerSettings.get_cors_origins(),
    allow_credentials=ServerSettings.CORS_ALLOW_CREDENTIALS,
    allow_methods=[ServerSettings.CORS_ALLOW_METHODS] if ServerSettings.CORS_ALLOW_METHODS != "*" else ["*"],
    allow_headers=[ServerSettings.CORS_ALLOW_HEADERS] if ServerSettings.CORS_ALLOW_HEADERS != "*" else ["*"],
)


@app.post(Routes.MESSAGES, 
         response_model=MessageResponse,
         status_code=status.HTTP_201_CREATED,
         tags=[Tags.MESSAGES],
         summary=Summaries.SUBMIT_MESSAGE,
         description=Descriptions.SUBMIT_MESSAGE)
async def receive_message(message: Message, background_tasks: BackgroundTasks, request: Request) -> MessageResponse:
    """
    Submit a message for asynchronous processing.

    This endpoint receives a message and immediately returns a response with a unique
    message ID and initial status. The actual processing is handled asynchronously
    in the background using AI agents.

    Args:
        message: The message object containing the user's message content
        background_tasks: FastAPI background tasks for async processing
        request: The HTTP request object to extract headers

    Returns:
        MessageResponse: Contains message_id, status ('received'), and received_at timestamp

    Raises:
        HTTPException: 
            - 400 Bad Request: If x-ms-conversation-id header is missing
            - 500 Internal Server Error: If message processing fails

    Note:
        Requires 'x-ms-conversation-id' header for conversation thread management.
        The message is processed asynchronously, so clients should poll the
        /messages/{message_id}/updates endpoint for real-time status updates.

    Example:
        ```bash
        curl -X POST "http://localhost:8000/messages" \
             -H "Content-Type: application/json" \
             -H "x-ms-conversation-id: thread-123" \
             -d '{"message": "Hello, world!"}'
        ```
    """
    # Extract conversation ID from header
    thread_id = request.headers.get("x-ms-conversation-id", None)
    if not thread_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Missing required header: x-ms-conversation-id"
        )
    
    response: MessageResponse = await message_processor.submit_message(message)
    
    # Start background processing with conversation ID
    background_tasks.add_task(
        message_processor.process_message_async, 
        response.message_id, 
        thread_id,
        message.message,
    )
    
    return response


@app.get(Routes.MESSAGE_UPDATES, 
        response_model=List[UpdateResponse],
        tags=[Tags.MESSAGES],
        summary=Summaries.GET_UPDATES,
        description=Descriptions.GET_UPDATES)
async def get_updates(message_id: str) -> List[UpdateResponse]:
    """
    Get all processing updates for a specific message.

    This endpoint retrieves the complete history of processing updates for a given
    message, including intermediate status changes, agent responses, and final results.
    Clients can poll this endpoint for real-time progress updates.

    Args:
        message_id: The unique identifier of the message to get updates for

    Returns:
        List[UpdateResponse]: Chronologically ordered list of all processing updates

    Raises:
        HTTPException: 
            - 404 Not Found: If the message_id doesn't exist in the system

    Note:
        Returns an empty list if the message exists but has no updates yet.
        Updates are added in real-time as the message progresses through processing.

    Example:
        ```bash
        curl "http://localhost:8000/messages/123e4567-e89b-12d3-a456-426614174000/updates"
        ```
    """
    try:
        updates: List[UpdateResponse] = message_processor.get_message_updates(message_id)
        return updates
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=str(e)
        )


@app.get(Routes.MESSAGE_STATUS,
        tags=[Tags.MESSAGES],
        summary=Summaries.GET_STATUS,
        description=Descriptions.GET_STATUS)
async def get_message_status(message_id: str) -> Dict[str, Any]:
    """
    Get the current status and details of a specific message.

    This endpoint provides comprehensive information about a message including
    its current processing status, original content, and timing information.
    Useful for status checks and message management.

    Args:
        message_id: The unique identifier of the message to check

    Returns:
        Dict[str, Any]: Dictionary containing:
            - message_id: The unique identifier
            - status: Current processing status (received, inprogress, completed, failed)
            - content: The original message content
            - timestamp: When the message was received

    Raises:
        HTTPException: 
            - 404 Not Found: If the message_id doesn't exist in the system

    Example:
        ```bash
        curl "http://localhost:8000/messages/123e4567-e89b-12d3-a456-426614174000/status"
        ```
    """
    try:
        status_info: Dict[str, Any] = message_processor.get_message_status(message_id)
        return status_info
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=str(e)
        )


@app.get(Routes.MESSAGES,
        tags=[Tags.MESSAGES],
        summary=Summaries.LIST_MESSAGES,
        description=Descriptions.LIST_MESSAGES)
async def list_messages() -> Dict[str, Any]:
    """
    List all messages in the system with summary information.

    This endpoint provides an overview of all messages currently stored in the system,
    including their IDs, processing statuses, and timestamps. Useful for system
    monitoring, debugging, and administrative tasks.

    Returns:
        Dict[str, Any]: Dictionary containing:
            - total_messages: Total count of messages in the system
            - messages: List of message summaries with ID, status, and timestamp

    Note:
        This endpoint returns summary information only. Use get_message_status()
        for detailed information about a specific message. The response includes
        all messages regardless of their processing status.

    Example:
        ```bash
        curl "http://localhost:8000/messages"
        ```
    """
    messages: Dict[str, Any] = message_processor.list_all_messages()
    return messages


@app.get(Routes.HEALTH,
        response_model=HealthResponse,
        tags=[Tags.SYSTEM],
        summary=Summaries.HEALTH_CHECK,
        description=Descriptions.HEALTH_CHECK)
async def health_check() -> HealthResponse:
    """
    Health check endpoint for monitoring service status and system information.

    This endpoint provides comprehensive health information about the service,
    including operational status, uptime, version, and system timestamps.
    Used by monitoring systems and load balancers to verify service availability.

    Returns:
        HealthResponse: Health status object containing:
            - status: Current system status ("healthy")
            - timestamp: Current system time
            - version: Application version
            - uptime_seconds: System uptime in seconds since startup

    Note:
        This endpoint should always return a 200 OK response when the service
        is operational. If the service is down, the endpoint won't be reachable.
        The uptime is calculated from when the MessageProcessor was initialized.

    Example:
        ```bash
        curl "http://localhost:8000/health"
        ```
    """
    health_status: HealthResponse = message_processor.get_health_status()
    return health_status


@app.get(Routes.ROOT,
        tags=[Tags.SYSTEM],
        summary=Summaries.ROOT,
        description=Descriptions.ROOT)
async def root() -> RedirectResponse:
    """
    Root endpoint that redirects to interactive API documentation.

    This endpoint provides a convenient way for users to access the API documentation
    by redirecting them to the Swagger UI interface. It serves as the main entry point
    for developers exploring the API.

    Returns:
        RedirectResponse: HTTP 302 redirect to /docs endpoint

    Note:
        This is a convenience endpoint that automatically redirects users to the
        interactive API documentation. The redirect is permanent and helps users
        discover the API capabilities quickly.

    Example:
        ```bash
        curl -L "http://localhost:8000/"
        # Redirects to http://localhost:8000/docs
        ```
    """
    return RedirectResponse(url=Routes.DOCS)


@app.get(Routes.SWAGGER,
        tags=[Tags.DOCUMENTATION],
        summary=Summaries.SWAGGER_REDIRECT,
        description=Descriptions.SWAGGER_REDIRECT)
async def swagger_redirect() -> RedirectResponse:
    """
    Alternative endpoint that redirects to Swagger UI documentation.

    This endpoint provides an alternative route to access the Swagger UI documentation.
    It's useful for users who are familiar with the /swagger path convention and
    expect to find documentation there.

    Returns:
        RedirectResponse: HTTP 302 redirect to /docs endpoint

    Note:
        This is an alternative path to the main documentation. Both /swagger and /
        redirect to the same /docs endpoint for consistency and user convenience.

    Example:
        ```bash
        curl -L "http://localhost:8000/swagger"
        # Redirects to http://localhost:8000/docs
        ```
    """
    return RedirectResponse(url=Routes.DOCS)
