# Semker - Async FastAPI Backend Service

A FastAPI backend service with asynchronous message processing capabilities.

## Project Structure

```
semker/
├── .gitignore                      # Git ignore rules
├── README.md                       # Root project README
└── src/
    └── backend/
        ├── models/
        │   ├── __init__.py
        │   └── schemas.py          # Pydantic models
        ├── process/
        │   ├── __init__.py
        │   └── message_processor.py # Message processing logic
        ├── tests/
        │   └── features/
        │       ├── environment.py  # BDD test environment setup
        │       ├── error_handling.feature  # Error handling tests
        │       ├── message_api.feature     # Main API tests
        │       ├── smoke_test.feature      # Smoke tests
        │       └── steps/
        │           └── api_steps.py        # Step definitions
        ├── config/
        │   ├── __init__.py
        │   ├── settings.py         # Environment-dependent configuration
        │   └── constants.py        # Immutable application constants
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
  "content": "Your message content here",
  "sender": "sender_name"
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
  -d '{"content": "Hello, async world!", "sender": "test_user"}'
```

2. Get updates (replace `{message_id}` with actual ID):
```bash
curl "http://localhost:8000/messages/{message_id}/updates"
```

3. Get message status:
```bash
curl "http://localhost:8000/messages/{message_id}/status"
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
