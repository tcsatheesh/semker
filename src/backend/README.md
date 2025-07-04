# Semker Backend - FastAPI Async Message Processing

A high-performance FastAPI backend service providing asynchronous message processing with real-time status tracking, comprehensive testing, and modern API design.

## Features

### 🚀 **Core Capabilities**
- **Asynchronous Processing**: Non-blocking message handling with background tasks
- **Real-time Status Tracking**: Live updates from received → processing → processed
- **Health Monitoring**: Built-in health checks with uptime and version info
- **Type Safety**: Full Pydantic model validation and OpenAPI documentation
- **CORS Support**: Configurable cross-origin resource sharing
- **Telemetry Ready**: Optional observability and monitoring

### 🧪 **Testing & Quality**
- **BDD Testing**: Comprehensive behavior-driven development test suite
- **API Documentation**: Auto-generated OpenAPI/Swagger docs
- **Error Handling**: Robust error responses with proper HTTP status codes
- **Validation**: Request/response validation with detailed error messages

## Quick Start

### Setup
```bash
# Navigate to backend directory
cd src/backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### Verify Installation
```bash
# Health check
curl http://localhost:8000/health

# API documentation
open http://localhost:8000/docs
```

## Project Structure

```
src/backend/
├── README.md                   # This file
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── api.py                     # Main FastAPI application
├── models/
│   ├── __init__.py
│   └── schemas.py             # Pydantic data models
├── process/
│   ├── __init__.py
│   └── message_processor.py   # Core message processing logic
├── config/
│   ├── __init__.py
│   ├── settings.py            # Environment-based configuration
│   └── constants.py           # Application constants
├── tests/
│   └── features/
│       ├── environment.py     # BDD test setup
│       ├── message_api.feature
│       ├── error_handling.feature
│       ├── smoke_test.feature
│       └── steps/
│           └── api_steps.py   # Test step definitions
├── scripts/
│   ├── test_cors.sh          # CORS testing script
│   └── README.md
└── telemetry/
    ├── __init__.py
    ├── middleware.py         # Telemetry middleware
    └── README.md
```

## API Endpoints

### Core Messages API
- **POST /messages** - Submit message for processing
- **GET /messages** - List all messages with pagination
- **GET /messages/{id}** - Get specific message details
- **GET /messages/{id}/updates** - Get real-time processing updates

### System Endpoints
- **GET /health** - Health check with uptime and version
- **GET /** - Root endpoint with API information
- **GET /docs** - Interactive API documentation
- **GET /redoc** - Alternative API documentation

### Example Usage

#### Submit Message
```bash
curl -X POST http://localhost:8000/messages \
  -H "Content-Type: application/json" \
  -d '{"message": "Process this message"}'

# Response
{
  "message_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "received", 
  "received_at": "2025-07-04T10:30:00.123456"
}
```

#### Check Processing Updates
```bash
curl http://localhost:8000/messages/550e8400-e29b-41d4-a716-446655440000/updates

# Response
[
  {
    "message_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "processing",
    "processed_at": "2025-07-04T10:30:00.234567",
    "result": "Message is being processed..."
  },
  {
    "message_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "processed", 
    "processed_at": "2025-07-04T10:30:02.345678",
    "result": "Processed message: Process this message..."
  }
]
```

## Configuration

### Environment Variables (.env)
```bash
# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CORS_ALLOW_CREDENTIALS=true
CORS_ALLOW_METHODS=*
CORS_ALLOW_HEADERS=*

# Message Processing
MESSAGE_PROCESSING_DELAY=2.0

# Logging
LOG_LEVEL=INFO

# Telemetry (optional)
TELEMETRY_ENABLED=false
TELEMETRY_SERVICE_NAME=semker-backend
TELEMETRY_SERVICE_VERSION=1.0.0
```

### Server Settings
The backend automatically configures itself based on environment variables with sensible defaults.

## Data Models

### Message Schema (Input)
```python
class Message(BaseModel):
    message: str = Field(description="The message content to be processed")
```

### MessageResponse Schema (Output)
```python
class MessageResponse(BaseModel):
    message_id: str = Field(description="Unique identifier for the message")
    status: str = Field(description="Current status of the message")
    received_at: datetime = Field(description="Timestamp when message was received")
```

### UpdateResponse Schema
```python
class UpdateResponse(BaseModel):
    message_id: str = Field(description="Unique identifier for the message")
    status: str = Field(description="Processing status")
    processed_at: datetime = Field(description="Timestamp when processing completed")
    result: Optional[str] = Field(None, description="Processing result or summary")
```

## Message Processing Flow

1. **Submit** → Message received, assigned UUID, stored with "received" status
2. **Queue** → Background task initiated for asynchronous processing
3. **Process** → Status updated to "processing", intermediate update stored
4. **Complete** → Status updated to "processed", final result stored
5. **Retrieve** → Client can poll `/updates` endpoint for real-time status

## Testing

### Run BDD Tests
```bash
# Run all tests
python -m behave tests/features/

# Run specific feature
python -m behave tests/features/message_api.feature

# Run with verbose output
python -m behave tests/features/ --verbose

# Run smoke tests only
python -m behave tests/features/ --tags=smoke
```

### Test Coverage
- **Message API**: Submit, retrieve, and update messages
- **Error Handling**: Invalid requests, missing resources, validation errors  
- **Health Checks**: Service availability and status
- **CORS**: Cross-origin request handling

### Manual Testing
```bash
# Test CORS
./scripts/test_cors.sh

# Health check
curl http://localhost:8000/health

# Submit test message
curl -X POST http://localhost:8000/messages \
  -H "Content-Type: application/json" \
  -d '{"message": "Test message"}'
```

## Development

### Architecture
- **FastAPI Framework**: Modern async Python web framework
- **Pydantic Models**: Type-safe data validation and serialization
- **Background Tasks**: Async message processing without blocking
- **In-Memory Storage**: Simple message storage (production: use database)
- **Middleware Stack**: CORS, telemetry, and custom middleware support

### Key Components
- **api.py**: Main application with route definitions
- **MessageProcessor**: Core business logic for message handling
- **Configuration**: Environment-based settings management
- **Models**: Pydantic schemas for request/response validation

### Adding New Features
1. Define new Pydantic models in `models/schemas.py`
2. Add business logic to appropriate processor
3. Create new routes in `api.py`
4. Add BDD tests in `tests/features/`
5. Update documentation

### Performance Considerations
- **Async Operations**: All I/O operations are async
- **Background Processing**: CPU-intensive tasks run in background
- **Memory Usage**: Current in-memory storage scales to available RAM
- **Connection Pooling**: FastAPI handles connection pooling automatically

## Deployment

### Production Considerations
```bash
# Production server with Gunicorn
pip install gunicorn
gunicorn api:app -w 4 -k uvicorn.workers.UvicornWorker

# Docker deployment
# See Dockerfile in project root

# Environment variables for production
CORS_ORIGINS=https://yourdomain.com
LOG_LEVEL=WARNING
MESSAGE_PROCESSING_DELAY=1.0
```

### Monitoring
- Health endpoint provides uptime and version info
- Optional telemetry integration for observability
- Structured logging for debugging and monitoring

## Troubleshooting

### Common Issues
1. **Import Errors**: Ensure virtual environment is activated
2. **Port Conflicts**: Check if port 8000 is available
3. **CORS Errors**: Verify CORS_ORIGINS includes frontend URL
4. **Permission Errors**: Check file permissions for .env files

### Debug Mode
```bash
# Enable debug logging
LOG_LEVEL=DEBUG python -m uvicorn api:app --reload

# Check configuration
python -c "from config.settings import ServerSettings; print(vars(ServerSettings))"
```

## Contributing

1. Follow PEP 8 style guidelines
2. Add type hints to all functions
3. Write BDD tests for new features
4. Update documentation
5. Ensure all tests pass before submitting PR

## Dependencies

### Core Dependencies
- **fastapi**: Modern web framework
- **uvicorn**: ASGI server
- **pydantic**: Data validation and serialization
- **python-multipart**: Form data parsing

### Development Dependencies  
- **behave**: BDD testing framework
- **requests**: HTTP client for testing

For complete dependency list, see `requirements.txt`.
        ├── .behaverc               # Behave configuration
        ├── .python-version         # Python version specification
        ├── __init__.py
        ├── api.py                  # FastAPI application and route definitions
        ├── pyproject.toml          # Project configuration and dependencies
        ├── README.md               # This file (Backend documentation)
        ├── scripts/                # Shell scripts directory
        │   ├── run_bdd_tests.sh    # BDD test runner script
        │   ├── start_server.sh     # Shell script to start server
        │   ├── docker-build.sh     # Docker build script
        │   ├── docker-run.sh       # Docker run script
        │   └── check-types.sh      # Type checking script
        └── uv.lock                 # UV lock file
```

## Architecture

The backend follows a clean, modular architecture:

### Core Components

- **`api.py`**: FastAPI route definitions and endpoint handlers - contains only method signatures
- **`config/`**: Configuration and constants management
  - **`settings.py`**: Environment-dependent configuration (API metadata, server settings, processing parameters)
  - **`constants.py`**: Immutable application constants (routes, status codes, HTTP methods, etc.)
- **`process/`**: Business logic layer containing all message processing functionality
  - **`MessageProcessor`**: Main class handling message storage, processing, and status tracking
- **`models/`**: Data models and schemas using Pydantic
- **`tests/`**: Comprehensive BDD test suite using Behave

### Separation of Concerns

- **API Layer** (`api.py`): Handles HTTP requests/responses, validation, and routing
- **Business Logic** (`process/`): Contains all core functionality wrapped in classes
- **Data Models** (`models/`): Defines data structures and validation rules
- **Tests** (`tests/`): Behavioral driven development tests ensuring functionality

### Configuration vs Constants

- **Settings** (`config/settings.py`): Environment-dependent values that can be configured via environment variables
  - API metadata (title, version, description)
  - Server configuration (host, port, timeouts)
  - Processing parameters (delays, limits)
  
- **Constants** (`config/constants.py`): Immutable values that never change across environments
  - Route paths and HTTP methods
  - Status codes and message states
  - Content types and header names

This architecture ensures:
- **Maintainability**: Clear separation between API and business logic
- **Configurability**: Easy to adjust settings per environment without code changes
- **Testability**: Business logic can be tested independently
- **Scalability**: Easy to extend with new processors or storage backends
- **Readability**: Clean, focused code with single responsibilities

## Features

- **Asynchronous Message Processing**: Send messages that are processed in the background
- **Real-time Updates**: Get updates on message processing status
- **RESTful API**: Clean and well-documented API endpoints
- **Swagger Documentation**: Interactive API documentation
- **Modular Architecture**: Organized code structure with separate models and processing logic
- **In-memory Storage**: Fast message and update storage (can be extended to use databases)

## API Endpoints

### 1. Send Message
- **URL**: `POST /messages`
- **Description**: Submit a message for asynchronous processing
- **Request Body**:
```json
{
  "message": "Your message content here"
}
```
- **Response**:
```json
{
  "message_id": "uuid-string",
  "status": "received",
  "received_at": "2025-07-03T10:30:00"
}
```

### 2. Get Updates
- **URL**: `GET /messages/{message_id}/updates`
- **Description**: Get all updates for a specific message
- **Response**:
```json
[
  {
    "message_id": "uuid-string",
    "status": "processed",
    "processed_at": "2025-07-03T10:30:02",
    "result": "Processed message: Your message content..."
  }
]
```

### 3. Get Message Status
- **URL**: `GET /messages/{message_id}/status`
- **Description**: Get the current status of a message
- **Response**:
```json
{
  "message_id": "uuid-string",
  "status": "processed",
  "content": "Your message content here",
  "sender": "sender_name",
  "timestamp": "2025-07-03T10:30:00"
}
```

### 4. List All Messages
- **URL**: `GET /messages`
- **Description**: Get a list of all messages
- **Response**:
```json
{
  "messages": [
    {
      "message_id": "uuid-string",
      "status": "processed",
      "sender": "sender_name",
      "timestamp": "2025-07-03T10:30:00"
    }
  ]
}
```

## Installation

1. Install dependencies using uv:
```bash
uv sync
```

2. Or install individual packages:
```bash
uv add fastapi uvicorn pydantic requests behave
```

## Running the Server

### Option 1: Using the startup script (recommended)
```bash
./scripts/start_server.sh
```

### Option 2: Using the Python startup script
```bash
python start_server.py
```

### Option 3: Using the main entry point
```bash
python main.py
```

### Option 4: Using uv directly
```bash
uv run python start_server.py
# or
uv run uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### Option 5: From project root using uvicorn
```bash
# From the project root directory
uvicorn src.backend.api:app --host 0.0.0.0 --port 8000 --reload
```

The server will start on `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc documentation**: http://localhost:8000/redoc

## Example Usage

## Testing

### Behavior Driven Development (BDD) Tests

The project uses [Behave](https://behave.readthedocs.io/) for BDD testing with Gherkin syntax.

#### Running All Tests
```bash
# Using shell script (recommended)
./scripts/run_bdd_tests.sh

# Direct behave command
uv run behave tests/features
```

#### Running Specific Feature Tests
```bash
# Specific features
./scripts/run_bdd_tests.sh message_api
./scripts/run_bdd_tests.sh error_handling

# Smoke tests only
./scripts/run_bdd_tests.sh smoke
```

#### Test Structure
```
tests/
├── features/
│   ├── environment.py              # Test environment setup
│   ├── message_api.feature         # Main API functionality tests
│   ├── error_handling.feature      # Error handling tests
│   └── steps/
│       └── api_steps.py            # Step definitions
└── run_tests.py                    # Test runner script
```

#### Test Features
- **Message Processing**: Submit messages and verify async processing
- **Status Checking**: Get message status and processing updates
- **Error Handling**: Proper error responses for invalid requests
- **Health Monitoring**: Service health and uptime verification

### Manual Testing

### Using curl

1. Send a message:
```bash
curl -X POST "http://localhost:8000/messages" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, async world!"}'
```

2. Get updates (replace `{message_id}` with actual ID):
```bash
curl "http://localhost:8000/messages/{message_id}/updates"
```

3. Get message status:
```bash
curl "http://localhost:8000/messages/{message_id}/status"
```

## Configuration

The API can be configured using environment variables. Copy `.env.example` to `.env` and modify as needed:

```bash
cp .env.example .env
```

### Available Environment Variables

#### CORS Configuration
- **`CORS_ORIGINS`**: Comma-separated list of allowed origins (default: `http://localhost:3000,http://127.0.0.1:3000`)
- **`CORS_ALLOW_CREDENTIALS`**: Allow credentials in CORS requests (default: `true`)
- **`CORS_ALLOW_METHODS`**: Allowed HTTP methods (default: `*`)
- **`CORS_ALLOW_HEADERS`**: Allowed HTTP headers (default: `*`)

#### API Settings
- **`API_TITLE`**: API title in OpenAPI documentation
- **`API_VERSION`**: API version
- **`API_DESCRIPTION`**: API description
- **`DEBUG`**: Enable debug mode (default: `false`)

#### Server Settings
- **`SERVER_HOST`**: Server host (default: `localhost`)
- **`SERVER_PORT`**: Server port (default: `8000`)
- **`SERVER_URL`**: Server URL for OpenAPI documentation
- **`MESSAGE_PROCESSING_DELAY`**: Processing delay in seconds (default: `2.0`)
- **`MAX_MESSAGE_LENGTH`**: Maximum message length (default: `10000`)

#### Contact Information
- **`CONTACT_NAME`**: API contact name
- **`CONTACT_EMAIL`**: API contact email
- **`CONTACT_URL`**: API contact URL

#### Telemetry (Optional)
- **`TELEMETRY_ENABLED`**: Enable OpenTelemetry (default: `true`)
- **`TELEMETRY_CONSOLE`**: Enable console telemetry output (default: `false`)
- **`OTLP_ENDPOINT`**: OpenTelemetry collector endpoint

### Example Configuration

```bash
# CORS for frontend integration
CORS_ORIGINS=http://localhost:3000,https://my-frontend.com
CORS_ALLOW_CREDENTIALS=true

# API customization
API_TITLE=My Custom API
DEBUG=true

# Server settings
SERVER_HOST=0.0.0.0
SERVER_PORT=8080
```

## Message Processing Flow

1. **Message Submission**: Client sends a message via POST `/messages`
2. **Immediate Response**: Server returns message ID and "received" status
3. **Background Processing**: Message is processed asynchronously (simulated with 2-second delay)
4. **Status Updates**: Client can poll for updates using GET `/messages/{id}/updates`
5. **Completion**: Processing completes and updates are available

## Architecture

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server for production
- **Background Tasks**: Async processing without blocking the API
- **In-memory Storage**: Fast storage for demo purposes

## Docker Deployment

The API includes production-ready Docker support with multi-stage builds and security best practices.

### Quick Start with Docker

1. **Build and run with helper scripts**:
```bash
# Build the Docker image
./scripts/docker-build.sh

# Run in development mode
./scripts/docker-run.sh

# Run in production mode (with nginx reverse proxy)
./scripts/docker-run.sh production
```

2. **Manual Docker commands**:
```bash
# Build the image
docker build -t semker-api:latest .

# Run the container
docker run -p 8000:8000 semker-api:latest

# Run with environment variables
docker run -p 8000:8000 -e PORT=8080 semker-api:latest
```

3. **Using Docker Compose**:
```bash
# Development mode (API only)
docker-compose up -d api

# Production mode (API + Nginx reverse proxy)
docker-compose --profile production up -d
```

### Docker Features

- **Multi-stage build**: Optimized for production with minimal image size
- **Security**: Non-root user, minimal attack surface
- **Health checks**: Built-in monitoring and automatic restarts
- **Environment variables**: Configurable port and settings
- **Signal handling**: Proper shutdown with dumb-init
- **Nginx integration**: Production-ready reverse proxy setup

### Docker Files

- **`Dockerfile`**: Multi-stage production-ready container
- **`docker-compose.yml`**: Development and production orchestration
- **`.dockerignore`**: Optimized build context
- **`nginx.conf`**: Production reverse proxy configuration
- **`scripts/docker-build.sh`**: Build helper script
- **`scripts/docker-run.sh`**: Run helper script

### Production Deployment

The Docker setup includes:
- **Load balancing**: Nginx reverse proxy
- **Security headers**: XSS protection, content security policy
- **Compression**: Gzip compression for better performance
- **Health monitoring**: Automatic health checks and restarts
- **Logging**: Structured logging with volume mounts

Access the API:
- **Development**: http://localhost:8000
- **Production**: http://localhost (via nginx) or http://localhost:8000 (direct)

## Future Enhancements

- Database integration (PostgreSQL, MongoDB)
- WebSocket support for real-time updates
- Message queuing (Redis, RabbitMQ)
- Authentication and authorization
- Rate limiting and API quotas
- Logging and monitoring
- Kubernetes deployment manifests
- CI/CD pipeline integration
