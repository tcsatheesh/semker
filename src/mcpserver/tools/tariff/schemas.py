"""
Tariff data schemas and models.

This module contains the Pydantic models used for tariff and usage data.
"""

from typing import List, Optional, Literal
from datetime import date
from pydantic import BaseModel


# Type aliases for better type safety
ServiceType = Literal["voice", "data", "sms", "roaming", "value_added_service"]
PricingStructure = Literal["prepaid", "postpaid", "hybrid", "flat_rate", "tiered"]


class ValidityPeriod(BaseModel):
    duration: int
    unit: Literal["days", "weeks", "months", "years"]


class UsageLimit(BaseModel):
    limit: Optional[float] = None  # e.g., GB for data, minutes for voice
    unit: Optional[str] = None
    fair_usage_policy: bool = False
    rollover: bool = False


class AddOn(BaseModel):
    name: str
    description: Optional[str]
    price: float
    validity: Optional[ValidityPeriod]


class NetworkAccess(BaseModel):
    access_types: List[Literal["2G", "3G", "4G", "5G"]]


class CustomerSegment(BaseModel):
    segment: Literal["retail", "enterprise", "youth", "senior", "iot", "m2m"]


class PromotionalOffer(BaseModel):
    description: str
    start_date: date
    end_date: Optional[date]


class TariffPlan(BaseModel):
    name: str
    service_types: List[ServiceType]
    pricing_structure: PricingStructure
    price: float
    validity: ValidityPeriod
    usage_limits: List[UsageLimit] = []
    add_ons: List[AddOn] = []
    network_access: NetworkAccess
    customer_segment: CustomerSegment
    promotional_offers: List[PromotionalOffer] = []
    regulatory_compliance_notes: Optional[str] = None
