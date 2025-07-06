"""
Roaming data access and business logic.

This module contains the data and functions for managing roaming charges.
"""

from .schemas import Charges, RoamingCharges


_roaming_data = RoamingCharges(
    roams=[
        Charges(
            month=11,
            details={
                "Romania": {
                    "Amount": 1.0,
                    "Unit": "GB",
                    "Cost": 3.99,
                    "Currency": "EUR",
                },
                "Spain": {
                    "Capacity": 3.0,
                    "Unit": "GB",
                    "Cost": 5.99,
                    "Currency": "EUR",
                },
                "Belgium": {
                    "Capacity": 2.0,
                    "Unit": "GB",
                    "Cost": 4.99,
                    "Currency": "EUR",
                },
            },
        ),
        Charges(
            month=10,
            details={
                "Romania": {
                    "Amount": 1.0,
                    "Unit": "GB",
                    "Cost": 3.99,
                    "Currency": "EUR",
                },
                "Spain": {
                    "Capacity": 3.0,
                    "Unit": "GB",
                    "Cost": 5.99,
                    "Currency": "EUR",
                },
                "Belgium": {
                    "Capacity": 2.0,
                    "Unit": "GB",
                    "Cost": 4.99,
                    "Currency": "EUR",
                },
            },
        ),
        Charges(
            month=9,
            details={
                "Romania": {
                    "Amount": 1.0,
                    "Unit": "GB",
                    "Cost": 1.99,
                    "Currency": "EUR",
                },
                "Spain": {
                    "Capacity": 3.0,
                    "Unit": "GB",
                    "Cost": 5.99,
                    "Currency": "EUR",
                },
                "Belgium": {
                    "Capacity": 2.0,
                    "Unit": "GB",
                    "Cost": 4.99,
                    "Currency": "EUR",
                },
            },
        ),
    ]
)


def get_roaming_charges_data(country: str, month: int) -> RoamingCharges:
    """
    Retrieve roaming charges for a specific country and month.

    Args:
        country: The country to retrieve roaming charges for.
                Must be one of: Romania, Spain, Belgium.
        month: The month number (1-12) to retrieve charges for.

    Returns:
        RoamingCharges: Container with roaming charge information for the
                       specified country and month.

    Raises:
        ValueError: If month is not between 1 and 12, or if country is not
                   one of the supported countries.
    """
    if month < 1 or month > 12:
        raise ValueError("Month must be between 1 and 12")
    if country not in ["Romania", "Spain", "Belgium"]:
        raise ValueError("Country must be one of: Romania, Spain, Belgium")
    # Simulated roaming data
    filtered_data = [
        Charges(
            month=charge.month,
            details={country: charge.details.get(country, {})},
        )
        for charge in _roaming_data.roams
        if charge.month == month
    ]
    return RoamingCharges(roams=filtered_data)
