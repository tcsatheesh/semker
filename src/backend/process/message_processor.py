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

from semantic_kernel.agents import ChatHistoryAgentThread
from agents.skernel import KernelUtils

threads = {}


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
            message: The message object containing the message content

        Returns:
            MessageResponse with message ID and initial status
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
        status: MessageStatus,
        result: str,
        agent_name: str,
    ) -> None:
        """
        Handle intermediate response updates during message processing.

        Args:
            message_id: The unique identifier of the message
            status: The current processing status
            result: The result or summary of the processing step
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
        """
        Simulate async message processing with intermediate status updates.

        Args:
            message_id: The unique identifier of the message
            message_content: The content of the message to process
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
            "timestamp": message_data["timestamp"],
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
                    "timestamp": msg_data["timestamp"],
                }
                for msg_id, msg_data in self.messages_store.items()
            ],
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
            uptime_seconds=uptime,
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
