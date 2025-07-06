"""
Ticket module package initialization.

This module provides access to support ticket functionality.
"""

# Re-export the public API
from .schemas import TicketResponse
from .tools import raise_support_ticket, mcp

__all__ = ["TicketResponse", "raise_support_ticket", "mcp"]
