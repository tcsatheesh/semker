"""
Billing data storage and management.

This module contains the sample billing data used by the billing tools.
"""

from .schemas import Bill, LineItem


bills = [
    Bill(
        month=11,
        details=[
            LineItem(
                description="base",
                amount=20.0,
                notes="Base charge for the month",
            ),
            LineItem(
                description="roaming",
                amount=50.0,
                notes="Roaming charges in Spain incurred during the month for 21GB of data",
            ),
            LineItem(
                description="amazon",
                amount=10.0,
                notes="Amazon Prime subscription for the month",
            ),
            LineItem(
                description="spotify",
                amount=10.0,
                notes="Spotify subscription for the month",
            ),
        ],
        currency="EUR",
    ),
    Bill(
        month=10,
        details=[
            LineItem(
                description="base",
                amount=20.0,
                notes="Base charge for the month",
            ),
            LineItem(
                description="roaming",
                amount=0.0,
                notes="No roaming charges incurred during the month",
            ),
            LineItem(
                description="amazon",
                amount=40.0,
                notes="Amazon Prime subscription for the month, includes puchasing of two movies",
            ),
            LineItem(
                description="spotify",
                amount=10.0,
                notes="Spotify subscription for the month",
            ),
        ],
        currency="EUR",
    ),
    Bill(
        month=9,
        details=[
            LineItem(
                description="base",
                amount=20.0,
                notes="Base charge for the month. New base charge due to price increase",
            ),
            LineItem(
                description="roaming",
                amount=0.0,
                notes="No roaming charges incurred during the month",
            ),
            LineItem(
                description="amazon",
                amount=10.0,
                notes="Amazon Prime subscription for the month",
            ),
            LineItem(
                description="spotify",
                amount=10.0,
                notes="Spotify subscription for the month",
            ),
        ],
        currency="EUR",
    ),
    Bill(
        month=8,
        details=[
            LineItem(
                description="base",
                amount=10.0,
                notes="Base charge for the month",
            ),
            LineItem(
                description="roaming",
                amount=0.0,
                notes="No roaming charges incurred during the month",
            ),
            LineItem(
                description="amazon",
                amount=10.0,
                notes="Amazon Prime subscription for the month",
            ),
        ],
        currency="EUR",
    ),
]
