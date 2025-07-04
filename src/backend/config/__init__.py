"""
Configuration module for Semker backend
"""

from typing import Final
from .settings import APISettings, ContactSettings, LicenseSettings, ServerSettings
from .constants import Routes, Tags, Summaries, Descriptions

__all__: Final[list[str]] = [
    "APISettings", 
    "ContactSettings", 
    "LicenseSettings", 
    "ServerSettings",
    "Routes", 
    "Tags", 
    "Summaries", 
    "Descriptions"
]
