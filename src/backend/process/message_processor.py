"""MessageProcessor class for handling asynchronous message processing.

This module provides the core message processing functionality for the AI chat system,
including message storage, background processing, status tracking, and health monitoring.
The processor handles messages asynchronously and provides real-time updates through
intermediate response callbacks.

Classes:
    MessageProcessor: Main class for handling all message processing operations.

Module Variables:
    threads: Global dictionary storing chat history agent threads by thread ID.
"""

import uuid
from datetime import datetime
from typing import Dict, List, Any

from models import Message, MessageResponse, UpdateResponse, HealthResponse
from config.constants import MessageStatus

from semantic_kernel.agents import ChatHistoryAgentThread, AgentThread
from agents.skernel import KernelUtils

# Global thread storage for maintaining conversation history
threads: Dict[str, AgentThread] = {}


class MessageProcessor:
    """Handles all message processing operations including storage, background processing, and status tracking.
    
    This class provides the core functionality for the AI chat system's message processing pipeline.
    It manages in-memory storage of messages and their processing updates, handles asynchronous
    message processing through various AI agents, and provides real-time status tracking.
    
    The processor supports:
    - Message submission and storage
    - Background asynchronous processing with AI agents
    - Real-time status updates and intermediate responses
    - Conversation thread management
    - Health monitoring and system status
    
    Attributes:
        messages_store: In-memory dictionary storing message data by message ID
        updates_store: In-memory dictionary storing processing updates by message ID
        server_start_time: Timestamp when the server was started for uptime calculation
    """

    def __init__(self) -> None:
        """Initialize the message processor with empty storage and server start time.
        
        Sets up in-memory storage dictionaries for messages and updates,
        and records the server start time for uptime calculations.
        """
        # In-memory storage for messages and updates
        self.messages_store: Dict[str, Dict[str, Any]] = {}
        self.updates_store: Dict[str, List[UpdateResponse]] = {}

        # Track server start time for uptime calculation
        self.server_start_time: datetime = datetime.now()

    async def submit_message(self, message: Message) -> MessageResponse:
        """Submit a message for asynchronous processing.
        
        Creates a unique message ID, stores the message with initial status,
        and returns a response object for tracking. The actual processing
        is handled separately by background tasks.

        Args:
            message: The message object containing the user's message content

        Returns:
            MessageResponse: Response object with message ID, initial status, and timestamp
            
        Note:
            This method only handles message submission and storage. The actual
            AI processing is triggered separately through background tasks.
        """
        message_id = str(uuid.uuid4())
        timestamp = datetime.now()

        # Store the message
        self.messages_store[message_id] = {
            "content": message.message,
            "timestamp": timestamp,
            "status": MessageStatus.RECEIVED,
        }

        # Start background processing (will be triggered by FastAPI background tasks)
        return MessageResponse(
            message_id=message_id, status=MessageStatus.RECEIVED, received_at=timestamp
        )

    def _on_intermediate_response(
        self,
        message_id: str,
        status: str,  # Changed from MessageStatus to str since it's actually a string constant
        result: str,
        agent_name: str,
    ) -> None:
        """Handle intermediate response updates during message processing.
        
        This callback method is invoked by AI agents during message processing
        to provide real-time status updates. It stores each update with timestamps
        for client polling and progress tracking.

        Args:
            message_id: The unique identifier of the message being processed
            status: The current processing status (string constant from MessageStatus)
            result: The result or summary of the current processing step
            agent_name: The name of the agent providing this update
            
        Note:
            This method is typically called as a callback by AI agents and should
            not be called directly. Updates are stored in memory and accessible
            via get_message_updates().
        """
        if message_id not in self.updates_store:
            self.updates_store[message_id] = []

        update = UpdateResponse(
            message_id=message_id,
            status=status,
            processed_at=datetime.now(),
            result=result,
            agent_name=agent_name,
        )
        self.updates_store[message_id].append(update)

    async def process_message_async(
        self,
        message_id: str,
        thread_id: str,
        message_content: str,
    ) -> None:
        """Process a message asynchronously using AI agents with real-time status updates.
        
        This method handles the complete message processing pipeline:
        1. Updates message status to IN_PROGRESS
        2. Creates/retrieves conversation thread for context
        3. Initializes Semantic Kernel utilities and agents
        4. Processes the message through the appropriate AI agent
        5. Handles success/failure cases and final status updates
        6. Provides real-time updates via callback mechanism

        Args:
            message_id: The unique identifier of the message to process
            thread_id: The unique identifier for the conversation thread
            message_content: The actual content of the user's message
            
        Note:
            This method is designed to be run as a background task and communicates
            progress through the _on_intermediate_response callback. All updates
            are stored in memory for client polling.
            
        Raises:
            Exception: Any errors during processing are caught and stored as failed status
        """
        # Set initial processing status
        if message_id in self.messages_store:
            self.messages_store[message_id]["status"] = MessageStatus.IN_PROGRESS

            # Store intermediate update
            processing_update = UpdateResponse(
                message_id=message_id,
                status=MessageStatus.RECEIVED,
                processed_at=datetime.now(),
                result="Message received and sent to the agent.",
                agent_name=None,  # Agent name will be set later
            )

            if message_id not in self.updates_store:
                self.updates_store[message_id] = []
            self.updates_store[message_id].append(processing_update)


        thread = threads.get(thread_id, ChatHistoryAgentThread())
        # Ensure we have a ChatHistoryAgentThread for the agent call
        if not isinstance(thread, ChatHistoryAgentThread):
            thread = ChatHistoryAgentThread()

        _kernel_utils = KernelUtils(
            message_id=message_id,
            thread_id=thread_id,
        )
        _agent = _kernel_utils.get_agent()
        _response = None
        _status = None
        _agent_name = None
        try:
            _response, thread, _agent_name = await _agent.process_message_async(
                message=message_content,
                message_id=message_id,
                thread_id=thread_id,
                thread=thread,
                on_intermediate_response=self._on_intermediate_response,
            )
            _status = MessageStatus.COMPLETED
            _response = _response
        except Exception as e:
            _status = MessageStatus.FAILED
            _response = str(e)

        threads[thread_id] = thread
        # Update to final processed status
        if message_id in self.messages_store:
            self.messages_store[message_id]["status"] = _status
            self.messages_store[message_id]["processed_at"] = datetime.now()

            # Store the final update
            final_update = UpdateResponse(
                message_id=message_id,
                status=_status,
                processed_at=datetime.now(),
                result=_response,
                agent_name=_agent_name,
            )
            self.updates_store[message_id].append(final_update)

    def get_message_updates(self, message_id: str) -> List[UpdateResponse]:
        """Get all processing updates for a specific message.
        
        Retrieves the complete history of processing updates for a message,
        including intermediate status changes, agent responses, and final results.
        Used by clients to poll for real-time progress updates.

        Args:
            message_id: The unique identifier of the message

        Returns:
            List[UpdateResponse]: Chronologically ordered list of all updates for the message

        Raises:
            KeyError: If the message_id is not found in the message store
            
        Note:
            Returns an empty list if the message exists but has no updates yet.
        """
        if message_id not in self.messages_store:
            raise KeyError(f"Message with ID {message_id} not found")

        return self.updates_store.get(message_id, [])

    def get_message_status(self, message_id: str) -> Dict[str, Any]:
        """Get the current status and details of a message.
        
        Retrieves comprehensive information about a message including its current
        processing status, content, and timestamps. Used for status checks and
        message management.

        Args:
            message_id: The unique identifier of the message

        Returns:
            Dict[str, Any]: Dictionary containing:
                - message_id: The unique identifier
                - status: Current processing status
                - content: The original message content
                - timestamp: When the message was received

        Raises:
            KeyError: If the message_id is not found in the message store
        """
        if message_id not in self.messages_store:
            raise KeyError(f"Message with ID {message_id} not found")

        message_data: Dict[str, Any] = self.messages_store[message_id]
        return {
            "message_id": message_id,
            "status": message_data["status"],
            "content": message_data["content"],
            "timestamp": message_data["timestamp"],
        }

    def list_all_messages(self) -> Dict[str, Any]:
        """List all messages in the system with summary information.
        
        Provides an overview of all messages currently stored in the system,
        including their IDs, statuses, and timestamps. Useful for system
        monitoring and debugging.

        Returns:
            Dict[str, Any]: Dictionary containing:
                - total_messages: Total count of messages in the system
                - messages: List of message summaries with ID, status, and timestamp
                
        Note:
            This method returns summary information only. Use get_message_status()
            for detailed information about a specific message.
        """
        return {
            "total_messages": len(self.messages_store),
            "messages": [
                {
                    "message_id": msg_id,
                    "status": msg_data["status"],
                    "timestamp": msg_data["timestamp"],
                }
                for msg_id, msg_data in self.messages_store.items()
            ],
        }

    def get_health_status(self) -> HealthResponse:
        """Get the current health status and system information.
        
        Provides comprehensive system health information including uptime,
        version, and operational status. Used for health checks and monitoring.

        Returns:
            HealthResponse: Health status object containing:
                - status: Current system status ("healthy")
                - timestamp: Current system time
                - version: Application version
                - uptime_seconds: System uptime in seconds since start
                
        Note:
            The uptime is calculated from when the MessageProcessor instance
            was created, not the actual server start time.
        """
        current_time = datetime.now()
        uptime = (current_time - self.server_start_time).total_seconds()

        return HealthResponse(
            status="healthy",
            timestamp=current_time,
            version="1.0.0",
            uptime_seconds=uptime,
        )

    def message_exists(self, message_id: str) -> bool:
        """Check if a message exists in the message store.
        
        Performs a simple existence check for a message ID in the system.
        Useful for validation before performing operations on messages.

        Args:
            message_id: The unique identifier of the message to check

        Returns:
            bool: True if the message exists in the store, False otherwise
            
        Note:
            This is a lightweight operation that only checks for existence,
            not the validity or processing status of the message.
        """
        return message_id in self.messages_store
