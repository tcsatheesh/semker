"""
Application settings and configuration management for the Semker API.

This module provides environment-based configuration classes that handle
all configurable aspects of the application. Settings are loaded from
environment variables with sensible defaults for development.

Configuration Classes:
    APISettings: API metadata and documentation settings
    ContactSettings: Contact information for API documentation
    LicenseSettings: License information for API documentation
    ServerSettings: Server configuration and runtime settings

Features:
    - Environment variable-based configuration
    - Sensible defaults for development
    - Type-safe configuration classes
    - CORS configuration management
    - Processing parameter tuning
    - Documentation customization

Usage:
    Settings are automatically loaded from environment variables:
    ```python
    from config.settings import APISettings
    print(APISettings.TITLE)  # "Semker Async Message Processing API"
    ```

Environment Variables:
    See individual class docstrings for complete lists of supported
    environment variables and their default values.
"""

import os
from typing import Optional


class APISettings:
    """
    API configuration settings for metadata and documentation.

    This class handles all API-level configuration including title, version,
    description, and debug settings. Values are loaded from environment
    variables with comprehensive defaults.

    Environment Variables:
        API_TITLE: API title shown in documentation (default: "Semker Async Message Processing API")
        API_VERSION: API version for documentation (default: "1.0.0")
        API_DESCRIPTION: API description with markdown support (default: comprehensive description)
        DEBUG: Enable debug mode (default: "false")

    Attributes:
        TITLE: API title for OpenAPI documentation
        VERSION: API version string
        DESCRIPTION: Comprehensive API description with markdown formatting
        DEBUG: Debug mode flag for development

    Example:
        ```python
        print(APISettings.TITLE)  # "Semker Async Message Processing API"
        print(APISettings.DEBUG)  # False
        ```
    """
    
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
    """
    Contact information settings for API documentation.

    This class manages contact information displayed in the OpenAPI documentation,
    allowing customization of support contact details.

    Environment Variables:
        CONTACT_NAME: Support contact name (default: "Semker API Support")
        CONTACT_EMAIL: Support email address (default: "support@semker.dev")
        CONTACT_URL: Support website URL (optional)

    Attributes:
        NAME: Contact name for API documentation
        EMAIL: Contact email address
        URL: Optional contact website URL

    Example:
        ```python
        print(ContactSettings.NAME)   # "Semker API Support"
        print(ContactSettings.EMAIL)  # "support@semker.dev"
        ```
    """
    
    NAME: str = os.getenv("CONTACT_NAME", "Semker API Support")
    EMAIL: str = os.getenv("CONTACT_EMAIL", "support@semker.dev")
    URL: Optional[str] = os.getenv("CONTACT_URL")


class LicenseSettings:
    """
    License information settings for API documentation.

    This class manages license information displayed in the OpenAPI documentation,
    providing legal information about the API usage.

    Environment Variables:
        LICENSE_NAME: License name (default: "MIT License")
        LICENSE_URL: License URL (default: "https://opensource.org/licenses/MIT")

    Attributes:
        NAME: License name for API documentation
        URL: License URL for legal reference

    Example:
        ```python
        print(LicenseSettings.NAME)  # "MIT License"
        print(LicenseSettings.URL)   # "https://opensource.org/licenses/MIT"
        ```
    """
    
    NAME: str = os.getenv("LICENSE_NAME", "MIT License")
    URL: str = os.getenv("LICENSE_URL", "https://opensource.org/licenses/MIT")


class ServerSettings:
    """
    Server configuration settings for runtime behavior.

    This class manages all server-related configuration including network settings,
    processing parameters, timeouts, and CORS configuration. All values can be
    customized through environment variables.

    Environment Variables:
        SERVER_HOST: Server bind address (default: "localhost")
        SERVER_PORT: Server port number (default: "8000")
        SERVER_URL: Server URL for documentation (default: "http://localhost:8000")
        SERVER_DESCRIPTION: Server description (default: "Development server")
        MESSAGE_PROCESSING_DELAY: Processing delay in seconds (default: "5.0")
        MAX_MESSAGE_LENGTH: Maximum message length (default: "10000")
        REQUEST_TIMEOUT: Request timeout in seconds (default: "30")
        MAX_CONNECTIONS: Maximum concurrent connections (default: "100")
        CORS_ORIGINS: Comma-separated allowed origins (default: "http://localhost:3000,http://127.0.0.1:3000")
        CORS_ALLOW_CREDENTIALS: Allow credentials in CORS (default: "true")
        CORS_ALLOW_METHODS: Allowed HTTP methods (default: "*")
        CORS_ALLOW_HEADERS: Allowed HTTP headers (default: "*")

    Attributes:
        HOST: Server host address
        PORT: Server port number
        DEFAULT_URL: Default server URL
        DEFAULT_DESCRIPTION: Server description
        MESSAGE_PROCESSING_DELAY: AI processing delay simulation
        MAX_MESSAGE_LENGTH: Maximum allowed message length
        REQUEST_TIMEOUT: HTTP request timeout
        MAX_CONNECTIONS: Maximum concurrent connections
        CORS_*: CORS configuration options

    Methods:
        get_cors_origins(): Returns CORS origins as a list

    Example:
        ```python
        print(ServerSettings.HOST)  # "localhost"
        print(ServerSettings.PORT)  # 8000
        origins = ServerSettings.get_cors_origins()  # ["http://localhost:3000", ...]
        ```
    """
    
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
        """
        Parse and return CORS origins as a list.

        This method parses the comma-separated CORS_ORIGINS environment variable
        into a list of individual origin URLs, removing any whitespace.

        Returns:
            list[str]: List of allowed CORS origins with whitespace stripped

        Example:
            ```python
            # If CORS_ORIGINS="http://localhost:3000, http://127.0.0.1:3000"
            origins = ServerSettings.get_cors_origins()
            # Returns: ["http://localhost:3000", "http://127.0.0.1:3000"]
            ```
        """
        return [origin.strip() for origin in cls.CORS_ORIGINS.split(",") if origin.strip()]
