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

current_tariff = TariffPlan(
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

hybrid_tariff_5g = TariffPlan(
    name="HybridSaver 5G+",
    service_types=["voice", "data", "sms"],
    pricing_structure="hybrid",
    price=29.99,
    validity=ValidityPeriod(duration=30, unit="days"),
    usage_limits=[
        UsageLimit(limit=600, unit="minutes", fair_usage_policy=False),
        UsageLimit(limit=25, unit="GB", fair_usage_policy=True, rollover=True),
        UsageLimit(limit=250, unit="SMS", fair_usage_policy=False)
    ],
    add_ons=[
        AddOn(
            name="Weekend Unlimited 5G",
            description="Unlimited 5G data on weekends",
            price=4.99,
            validity=ValidityPeriod(duration=7, unit="days")
        ),
        AddOn(
            name="Extra Talktime 300",
            description="300 additional minutes",
            price=3.49,
            validity=ValidityPeriod(duration=30, unit="days")
        )
    ],
    network_access=NetworkAccess(access_types=["5G"]),
    customer_segment=CustomerSegment(segment="retail"),
    promotional_offers=[
        PromotionalOffer(
            description="Free 5G weekend data for first month",
            start_date=date(2025, 7, 1),
            end_date=date(2025, 7, 31)
        )
    ],
    regulatory_compliance_notes="Compliant with 5G hybrid service regulations."
)


prepaid_tariff_5g = TariffPlan(
    name="UltraFlex 5G Prepaid",
    service_types=["voice", "data", "sms"],
    pricing_structure="prepaid",
    price=19.99,
    validity=ValidityPeriod(duration=28, unit="days"),
    usage_limits=[
        UsageLimit(limit=400, unit="minutes", fair_usage_policy=False),
        UsageLimit(limit=15, unit="GB", fair_usage_policy=True, rollover=False),
        UsageLimit(limit=150, unit="SMS", fair_usage_policy=False)
    ],
    add_ons=[
        AddOn(
            name="5G Data Boost 10GB",
            description="Extra 10GB of 5G data valid for 7 days",
            price=6.99,
            validity=ValidityPeriod(duration=7, unit="days")
        )
    ],
    network_access=NetworkAccess(access_types=["5G"]),
    customer_segment=CustomerSegment(segment="retail"),
    promotional_offers=[
        PromotionalOffer(
            description="Bonus 5GB on first recharge",
            start_date=date(2025, 7, 1),
            end_date=date(2025, 7, 31)
        )
    ],
    regulatory_compliance_notes="Prepaid 5G plan approved under national telecom guidelines."
)


flat_rate_tariff = TariffPlan(
    name="UnlimitedMax 5G Flat",
    service_types=["voice", "data", "sms"],
    pricing_structure="flat_rate",
    price=59.99,
    validity=ValidityPeriod(duration=1, unit="months"),
    usage_limits=[
        UsageLimit(limit=None, unit="minutes", fair_usage_policy=True),  # Unlimited with FUP
        UsageLimit(limit=None, unit="GB", fair_usage_policy=True),       # Unlimited with FUP
        UsageLimit(limit=None, unit="SMS", fair_usage_policy=False)      # Truly unlimited SMS
    ],
    add_ons=[
        AddOn(
            name="International Roaming Pack",
            description="Unlimited roaming in EU and North America",
            price=14.99,
            validity=ValidityPeriod(duration=1, unit="months")
        )
    ],
    network_access=NetworkAccess(access_types=["5G"]),
    customer_segment=CustomerSegment(segment="retail"),
    promotional_offers=[
        PromotionalOffer(
            description="First month free for new subscribers",
            start_date=date(2025, 7, 1),
            end_date=date(2025, 7, 31)
        )
    ],
    regulatory_compliance_notes="Flat rate plan complies with unlimited usage guidelines and fair usage policies."
)


tiered_tariff = TariffPlan(
    name="StepUp 5G Tiered",
    service_types=["voice", "data", "sms"],
    pricing_structure="tiered",
    price=34.99,  # Base tier price
    validity=ValidityPeriod(duration=1, unit="months"),
    usage_limits=[
        UsageLimit(limit=300, unit="minutes", fair_usage_policy=False),
        UsageLimit(limit=10, unit="GB", fair_usage_policy=True, rollover=False),
        UsageLimit(limit=100, unit="SMS", fair_usage_policy=False)
    ],
    add_ons=[
        AddOn(
            name="Tier 2 Upgrade",
            description="Upgrade to 20GB data and 600 minutes",
            price=10.00,
            validity=ValidityPeriod(duration=1, unit="months")
        ),
        AddOn(
            name="Tier 3 Upgrade",
            description="Upgrade to 40GB data and 1000 minutes",
            price=20.00,
            validity=ValidityPeriod(duration=1, unit="months")
        )
    ],
    network_access=NetworkAccess(access_types=["5G"]),
    customer_segment=CustomerSegment(segment="retail"),
    promotional_offers=[
        PromotionalOffer(
            description="Free upgrade to Tier 2 for first month",
            start_date=date(2025, 7, 1),
            end_date=date(2025, 7, 31)
        )
    ],
    regulatory_compliance_notes="Tiered pricing complies with consumer transparency regulations."
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
    _selected_tariff = None
    if pricing_structure == "postpaid":
        _selected_tariff = postpaid_sample_tariff
    elif pricing_structure == "prepaid":
        _selected_tariff = prepaid_tariff_5g
    elif pricing_structure == "hybrid":
        _selected_tariff = hybrid_tariff_5g
    elif pricing_structure == "flat_rate":
        _selected_tariff = flat_rate_tariff
    elif pricing_structure == "tiered":
        _selected_tariff = tiered_tariff
    else:
        raise ValueError(f"Unsupported pricing structure: {pricing_structure}")
    return _selected_tariff

@mcp.tool(description="A tool to retrieve current tariff plan for a customer")
async def get_current_tariff_plan() -> TariffPlan:
    """
    Get the current tariff plan for a customer.

    Returns:
        TariffPlan: The current tariff plan details.
    """
    # In a real implementation, this would query a database or external service
    # Here we return a sample tariff plan for demonstration purposes
    return current_tariff