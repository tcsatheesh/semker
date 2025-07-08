"""
Pydantic models for the Semker Async Message Processing API.

This module defines all the data models used throughout the API using Pydantic
for data validation, serialization, and automatic OpenAPI documentation generation.
All models include comprehensive field descriptions and example values.

Models:
    Message: Input model for message submission requests
    MessageResponse: Response model for message submission confirmations
    UpdateResponse: Response model for processing status updates
    HealthResponse: Response model for health check endpoints

Features:
    - Automatic data validation and type checking
    - JSON schema generation for OpenAPI documentation
    - Example values for interactive documentation
    - Comprehensive field descriptions for developer clarity
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Message(BaseModel):
    """
    Input model for message submission requests.

    This model represents the data structure for messages submitted to the API
    for asynchronous processing. It includes validation for message content
    and provides examples for API documentation.

    Attributes:
        message: The message content to be processed by AI agents

    Example:
        ```python
        message = Message(message="Hello, how can I check my bill?")
        ```
    """
    message: str = Field(description="The message content to be processed")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "This is a sample message for processing"
            }
        }


class MessageResponse(BaseModel):
    """
    Response model for message submission confirmations.

    This model represents the immediate response returned when a message is
    successfully submitted for processing. It includes the assigned message ID,
    initial status, and submission timestamp.

    Attributes:
        message_id: Unique identifier (UUID) assigned to the message
        status: Initial processing status (always "received" for new messages)
        received_at: Timestamp when the message was received by the system

    Example:
        ```python
        response = MessageResponse(
            message_id="123e4567-e89b-12d3-a456-426614174000",
            status="received",
            received_at=datetime.now()
        )
        ```
    """
    message_id: str = Field(description="Unique identifier for the message")
    status: str = Field(description="Current status of the message")
    received_at: datetime = Field(description="Timestamp when the message was received")

    class Config:
        json_schema_extra = {
            "example": {
                "message_id": "123e4567-e89b-12d3-a456-426614174000",
                "status": "received",
                "received_at": "2025-07-04T10:30:00.123456"
            }
        }


class UpdateResponse(BaseModel):
    """
    Response model for message processing status updates.

    This model represents individual updates generated during message processing.
    Each message can have multiple updates showing the progression through
    different processing stages and agent responses.

    Attributes:
        message_id: Unique identifier for the message being processed
        status: Current processing status (received, inprogress, completed, failed)
        processed_at: Timestamp when this update was generated
        result: Processing result, agent response, or status information
        agent_name: Name of the AI agent that generated this update

    Example:
        ```python
        update = UpdateResponse(
            message_id="123e4567-e89b-12d3-a456-426614174000",
            status="completed",
            processed_at=datetime.now(),
            result="Your current bill is £45.50",
            agent_name="BillingAgent"
        )
        ```
    """
    message_id: str = Field(description="Unique identifier for the message")
    status: str = Field(description="Processing status")
    processed_at: datetime = Field(description="Timestamp when processing completed")
    result: Optional[str] = Field(None, description="Processing result or summary")
    agent_name: Optional[str] = Field(None, description="Name of the agent that processed the message")

    class Config:
        json_schema_extra = {
            "example": {
                "message_id": "123e4567-e89b-12d3-a456-426614174000",
                "status": "processed",
                "processed_at": "2025-07-04T10:30:02.123456",
                "result": "Processed message: This is a sample message..."
            }
        }


class HealthResponse(BaseModel):
    """
    Response model for health check endpoints.

    This model provides comprehensive system health information including
    operational status, timing data, and version information. Used by
    monitoring systems and load balancers to verify service availability.

    Attributes:
        status: Service health status (typically "healthy")
        timestamp: Current server timestamp when health check was performed
        version: Application version for deployment tracking
        uptime_seconds: System uptime in seconds since startup

    Example:
        ```python
        health = HealthResponse(
            status="healthy",
            timestamp=datetime.now(),
            version="1.0.0",
            uptime_seconds=3600.0
        )
        ```
    """
    status: str = Field(description="Service health status")
    timestamp: datetime = Field(description="Current server timestamp")
    version: str = Field(description="API version")
    uptime_seconds: float = Field(description="Server uptime in seconds")
