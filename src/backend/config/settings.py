"""
Application settings and configuration values
These can vary between environments and deployments
"""

import os
from typing import Optional


class APISettings:
    """API configuration settings"""
    
    TITLE: str = os.getenv("API_TITLE", "Semker Async Message Processing API")
    VERSION: str = os.getenv("API_VERSION", "1.0.0")
    DESCRIPTION: str = os.getenv("API_DESCRIPTION", """
    ## Semker Async API
    
    A powerful asynchronous message processing service built with FastAPI.
    
    ### Features:
    * **Asynchronous Processing**: Submit messages for background processing
    * **Real-time Updates**: Get updates on message processing status
    * **RESTful Design**: Clean, well-documented API endpoints
    * **High Performance**: Built with FastAPI and async/await patterns
    
    ### Message Processing Flow:
    1. 📤 **Submit Message**: Send a message via `POST /messages`
    2. ⚡ **Immediate Response**: Get message ID and "received" status
    3. 🔄 **Background Processing**: Message processed asynchronously
    4. 📊 **Poll for Updates**: Check progress via `GET /messages/{id}/updates`
    5. ✅ **Get Results**: Retrieve final processing results
    
    ### Getting Started:
    1. Send a message using the `/messages` endpoint
    2. Use the returned `message_id` to poll for updates
    3. Check the `/docs` endpoint for interactive API documentation
    """)
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"


class ContactSettings:
    """Contact information settings"""
    
    NAME: str = os.getenv("CONTACT_NAME", "Semker API Support")
    EMAIL: str = os.getenv("CONTACT_EMAIL", "support@semker.dev")
    URL: Optional[str] = os.getenv("CONTACT_URL")


class LicenseSettings:
    """License information settings"""
    
    NAME: str = os.getenv("LICENSE_NAME", "MIT License")
    URL: str = os.getenv("LICENSE_URL", "https://opensource.org/licenses/MIT")


class ServerSettings:
    """Server configuration settings"""
    
    HOST: str = os.getenv("SERVER_HOST", "localhost")
    PORT: int = int(os.getenv("SERVER_PORT", "8000"))
    DEFAULT_URL: str = os.getenv("SERVER_URL", f"http://{HOST}:{PORT}")
    DEFAULT_DESCRIPTION: str = os.getenv("SERVER_DESCRIPTION", "Development server")
    
    # Processing settings
    MESSAGE_PROCESSING_DELAY: float = float(os.getenv("MESSAGE_PROCESSING_DELAY", "5.0"))
    MAX_MESSAGE_LENGTH: int = int(os.getenv("MAX_MESSAGE_LENGTH", "10000"))
    
    # Timeouts and limits
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "30"))
    MAX_CONNECTIONS: int = int(os.getenv("MAX_CONNECTIONS", "100"))
    
    # CORS settings
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
    CORS_ALLOW_CREDENTIALS: bool = os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() == "true"
    CORS_ALLOW_METHODS: str = os.getenv("CORS_ALLOW_METHODS", "*")
    CORS_ALLOW_HEADERS: str = os.getenv("CORS_ALLOW_HEADERS", "*")
    
    @classmethod
    def get_cors_origins(cls) -> list[str]:
        """Get CORS origins as a list"""
        return [origin.strip() for origin in cls.CORS_ORIGINS.split(",") if origin.strip()]
