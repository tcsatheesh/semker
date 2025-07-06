"""
Main FastAPI application for Semker Async Message Processing API
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
    """Submit a message for asynchronous processing."""
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
    """Get all processing updates for a specific message."""
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
    """Get the current status of a message."""
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
    """List all messages in the system."""
    messages: Dict[str, Any] = message_processor.list_all_messages()
    return messages


@app.get(Routes.HEALTH,
        response_model=HealthResponse,
        tags=[Tags.SYSTEM],
        summary=Summaries.HEALTH_CHECK,
        description=Descriptions.HEALTH_CHECK)
async def health_check() -> HealthResponse:
    """Health check endpoint for monitoring service status."""
    health_status: HealthResponse = message_processor.get_health_status()
    return health_status


@app.get(Routes.ROOT,
        tags=[Tags.SYSTEM],
        summary=Summaries.ROOT,
        description=Descriptions.ROOT)
async def root() -> RedirectResponse:
    """Root endpoint - redirects to interactive API documentation."""
    return RedirectResponse(url=Routes.DOCS)


@app.get(Routes.SWAGGER,
        tags=[Tags.DOCUMENTATION],
        summary=Summaries.SWAGGER_REDIRECT,
        description=Descriptions.SWAGGER_REDIRECT)
async def swagger_redirect() -> RedirectResponse:
    """Alternative endpoint that redirects to Swagger UI documentation."""
    return RedirectResponse(url=Routes.DOCS)
