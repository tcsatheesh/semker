"""
Pydantic models for the Semker Async API
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Message(BaseModel):
    """Message model for incoming requests"""
    message: str = Field(description="The message content to be processed")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "This is a sample message for processing"
            }
        }


class MessageResponse(BaseModel):
    """Response model when a message is received"""
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
    """Response model for message processing updates"""
    message_id: str = Field(description="Unique identifier for the message")
    status: str = Field(description="Processing status")
    processed_at: datetime = Field(description="Timestamp when processing completed")
    result: Optional[str] = Field(None, description="Processing result or summary")

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
    """Health check response model"""
    status: str = Field(description="Service health status")
    timestamp: datetime = Field(description="Current server timestamp")
    version: str = Field(description="API version")
    uptime_seconds: float = Field(description="Server uptime in seconds")
