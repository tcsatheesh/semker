"""
MessageProcessor class for handling asynchronous message processing
"""

import asyncio
import uuid
from datetime import datetime
from typing import Dict, List, Any

from models import Message, MessageResponse, UpdateResponse, HealthResponse
from config.settings import ServerSettings
from config.constants import MessageStatus


class MessageProcessor:
    """
    Handles all message processing operations including storage, 
    background processing, and status tracking.
    """
    
    def __init__(self) -> None:
        """Initialize the message processor with empty storage"""
        # In-memory storage for messages and updates
        self.messages_store: Dict[str, Dict[str, Any]] = {}
        self.updates_store: Dict[str, List[UpdateResponse]] = {}
        
        # Track server start time for uptime calculation
        self.server_start_time: datetime = datetime.now()
    
    async def submit_message(self, message: Message) -> MessageResponse:
        """
        Submit a message for asynchronous processing.
        
        Args:
            message: The message object containing content and sender
            
        Returns:
            MessageResponse with message ID and initial status
        """
        message_id = str(uuid.uuid4())
        timestamp = datetime.now()
        
        # Store the message
        self.messages_store[message_id] = {
            "content": message.content,
            "sender": message.sender,
            "timestamp": timestamp,
            "status": MessageStatus.RECEIVED
        }
        
        # Start background processing (will be triggered by FastAPI background tasks)
        return MessageResponse(
            message_id=message_id,
            status=MessageStatus.RECEIVED,
            received_at=timestamp
        )
    
    async def process_message_async(self, message_id: str, message_content: str) -> None:
        """
        Simulate async message processing.
        
        Args:
            message_id: The unique identifier of the message
            message_content: The content of the message to process
        """
        await asyncio.sleep(ServerSettings.MESSAGE_PROCESSING_DELAY)  # Configurable processing time
        
        # Update the message status
        if message_id in self.messages_store:
            self.messages_store[message_id]["status"] = MessageStatus.PROCESSED
            self.messages_store[message_id]["processed_at"] = datetime.now()
            
            # Store the update
            update = UpdateResponse(
                message_id=message_id,
                status=MessageStatus.PROCESSED,
                processed_at=datetime.now(),
                result=f"Processed message: {message_content[:50]}..."
            )
            
            if message_id not in self.updates_store:
                self.updates_store[message_id] = []
            self.updates_store[message_id].append(update)
    
    def get_message_updates(self, message_id: str) -> List[UpdateResponse]:
        """
        Get all processing updates for a specific message.
        
        Args:
            message_id: The unique identifier of the message
            
        Returns:
            List of updates for the message
            
        Raises:
            KeyError: If message_id is not found
        """
        if message_id not in self.messages_store:
            raise KeyError(f"Message with ID {message_id} not found")
        
        return self.updates_store.get(message_id, [])
    
    def get_message_status(self, message_id: str) -> Dict[str, Any]:
        """
        Get the current status of a message.
        
        Args:
            message_id: The unique identifier of the message
            
        Returns:
            Dictionary containing message details and status
            
        Raises:
            KeyError: If message_id is not found
        """
        if message_id not in self.messages_store:
            raise KeyError(f"Message with ID {message_id} not found")
        
        message_data: Dict[str, Any] = self.messages_store[message_id]
        return {
            "message_id": message_id,
            "status": message_data["status"],
            "content": message_data["content"],
            "sender": message_data["sender"],
            "timestamp": message_data["timestamp"]
        }
    
    def list_all_messages(self) -> Dict[str, Any]:
        """
        List all messages in the system.
        
        Returns:
            Dictionary containing total count and list of all messages
        """
        return {
            "total_messages": len(self.messages_store),
            "messages": [
                {
                    "message_id": msg_id,
                    "status": msg_data["status"],
                    "sender": msg_data["sender"],
                    "timestamp": msg_data["timestamp"]
                }
                for msg_id, msg_data in self.messages_store.items()
            ]
        }
    
    def get_health_status(self) -> HealthResponse:
        """
        Get the current health status and system information.
        
        Returns:
            HealthResponse with system status and uptime
        """
        current_time = datetime.now()
        uptime = (current_time - self.server_start_time).total_seconds()
        
        return HealthResponse(
            status="healthy",
            timestamp=current_time,
            version="1.0.0",
            uptime_seconds=uptime
        )
    
    def message_exists(self, message_id: str) -> bool:
        """
        Check if a message exists in the store.
        
        Args:
            message_id: The unique identifier of the message
            
        Returns:
            True if message exists, False otherwise
        """
        return message_id in self.messages_store
