"""
Tariff module package initialization.

This module provides access to tariff plan functionality.
"""

# Re-export the public API
from .schemas import (
    TariffPlan, ValidityPeriod, UsageLimit, AddOn, NetworkAccess,
    CustomerSegment, PromotionalOffer, PricingStructure, ServiceType
)
from .tools import get_tariff_plan, get_current_tariff_plan, mcp

__all__ = [
    "TariffPlan", "ValidityPeriod", "UsageLimit", "AddOn", "NetworkAccess",
    "CustomerSegment", "PromotionalOffer", "PricingStructure", "ServiceType",
    "get_tariff_plan", "get_current_tariff_plan", "mcp"
]
