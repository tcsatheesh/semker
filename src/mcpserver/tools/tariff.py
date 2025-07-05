"""
Tariff and usage data management tool module.

This module provides functionality to retrieve tariff information and usage
details for customers.
"""

from typing import List, Optional, Literal
from datetime import date
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

mcp = FastMCP(
    name="TariffTool",
    stateless_http=True,
)


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


postpaid_sample_tariff = TariffPlan(
    name="SmartConnect 5G Max",
    service_types=["voice", "data", "sms", "roaming"],
    pricing_structure="postpaid",
    price=49.99,
    validity=ValidityPeriod(duration=1, unit="months"),
    usage_limits=[
        UsageLimit(limit=1000, unit="minutes", fair_usage_policy=False),
        UsageLimit(limit=50, unit="GB", fair_usage_policy=True, rollover=True),
        UsageLimit(limit=500, unit="SMS", fair_usage_policy=False)
    ],
    add_ons=[
        AddOn(
            name="International Calling Pack",
            description="100 minutes to EU and US",
            price=9.99,
            validity=ValidityPeriod(duration=1, unit="months")
        ),
        AddOn(
            name="Streaming Bundle",
            description="Unlimited access to music and video platforms",
            price=5.99,
            validity=ValidityPeriod(duration=1, unit="months")
        )
    ],
    network_access=NetworkAccess(access_types=["4G", "5G"]),
    customer_segment=CustomerSegment(segment="retail"),
    promotional_offers=[
        PromotionalOffer(
            description="20% off for first 3 months",
            start_date=date(2025, 7, 1),
            end_date=date(2025, 9, 30)
        )
    ],
    regulatory_compliance_notes="Compliant with Ofcom UK regulations."
)

prepaid_tariff = TariffPlan(
    name="FlexiConnect 4G Prepaid",
    service_types=["voice", "data", "sms"],
    pricing_structure="prepaid",
    price=14.99,
    validity=ValidityPeriod(duration=28, unit="days"),
    usage_limits=[
        UsageLimit(limit=300, unit="minutes", fair_usage_policy=False),
        UsageLimit(limit=10, unit="GB", fair_usage_policy=True, rollover=False),
        UsageLimit(limit=100, unit="SMS", fair_usage_policy=False)
    ],
    add_ons=[
        AddOn(
            name="Data Booster 5GB",
            description="Extra 5GB valid for 7 days",
            price=4.99,
            validity=ValidityPeriod(duration=7, unit="days")
        )
    ],
    network_access=NetworkAccess(access_types=["4G"]),
    customer_segment=CustomerSegment(segment="retail"),
    promotional_offers=[
        PromotionalOffer(
            description="Bonus 2GB on first recharge",
            start_date=date(2025, 7, 1),
            end_date=date(2025, 7, 31)
        )
    ],
    regulatory_compliance_notes="Compliant with Ofcom UK prepaid service guidelines."
)



@mcp.tool(description="A tool to retrieve tariff plan for customers")
async def get_tariff_plan(
    pricing_structure: PricingStructure,
) -> TariffPlan:
    """
    Get tariff plan for a customer based on pricing structure.

    Args:
        pricing_structure: The pricing structure type (prepaid, postpaid, etc.)

    Returns:
        TariffPlan: The tariff plan details for the specified pricing structure.
    """
    # In a real implementation, this would query a database or external service
    # Here we return a sample tariff plan for demonstration purposes
    return postpaid_sample_tariff

@mcp.tool(description="A tool to retrieve current tariff plan for a customer")
async def get_current_tariff_plan() -> TariffPlan:
    """
    Get the current tariff plan for a customer.

    Returns:
        TariffPlan: The current tariff plan details.
    """
    # In a real implementation, this would query a database or external service
    # Here we return a sample tariff plan for demonstration purposes
    return prepaid_tariff