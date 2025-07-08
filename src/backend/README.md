# Semker Backend - AI-Powered Async Message Processing

A high-performance FastAPI backend service providing asynchronous message processing with intelligent AI agents, real-time status tracking, comprehensive testing, and modern API design.

## 🚀 Features

### **Core Capabilities**
- **AI-Powered Processing**: Multi-agent system for intelligent message handling (billing, roaming, FAQ, etc.)
- **Asynchronous Architecture**: Non-blocking message processing with background tasks
- **Real-time Status Tracking**: Live updates from received → inprogress → completed/failed
- **Conversation Management**: Thread-based conversation context with Semantic Kernel
- **Health Monitoring**: Built-in health checks with uptime, version, and system info
- **Type Safety**: Full Pydantic model validation and OpenAPI documentation
- **CORS Support**: Configurable cross-origin resource sharing
- **Comprehensive Telemetry**: OpenTelemetry integration with multiple backends

### **AI Agent System**
- **Semantic Kernel Integration**: Microsoft Semantic Kernel for AI orchestration
- **Multi-Agent Architecture**: Specialized agents for different domains
- **Model Context Protocol (MCP)**: Seamless integration with external services
- **Conversation Context**: Persistent thread management for coherent conversations
- **Intermediate Responses**: Real-time updates during AI processing

### **Testing & Quality**
- **BDD Testing**: Comprehensive behavior-driven development test suite
- **API Documentation**: Auto-generated OpenAPI/Swagger docs with examples
- **Error Handling**: Robust error responses with proper HTTP status codes
- **Data Validation**: Request/response validation with detailed error messages
- **Type Checking**: Full type safety with Python type hints

## 📋 Quick Start

### Prerequisites
- Python 3.12 or higher
- UV package manager (recommended) or pip
- Git for cloning the repository

### Installation & Setup

#### Option 1: Using UV (Recommended)
```bash
# Navigate to backend directory
cd src/backend

# Install dependencies with UV
uv sync

# Run the server
uv run python start_server.py
```

#### Option 2: Using Python Virtual Environment
```bash
# Navigate to backend directory
cd src/backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python start_server.py
```

#### Option 3: Using Startup Scripts
```bash
# Make script executable
chmod +x scripts/start_server.sh

# Run the server
./scripts/start_server.sh
```

### Verify Installation
```bash
# Health check
curl http://localhost:8000/health

# API documentation
open http://localhost:8000/docs

# Example message submission
curl -X POST http://localhost:8000/messages \
  -H "Content-Type: application/json" \
  -H "x-ms-conversation-id: test-thread-123" \
  -d '{"message": "What is my current bill?"}'
```

## 📁 Project Structure

```
src/backend/
├── README.md                   # This file - comprehensive documentation
├── pyproject.toml              # Project configuration and dependencies
├── uv.lock                     # UV dependency lock file
├── main.py                     # Application entry point
├── start_server.py             # Server startup script
├── api.py                      # FastAPI application and route definitions
├── agents/                     # AI agent implementations
│   ├── __init__.py
│   ├── base.py                 # Base agent class and interfaces
│   ├── billing.py              # Billing agent for account inquiries
│   ├── roaming.py              # Roaming agent for travel-related queries
│   ├── tariff.py               # Tariff agent for plan information
│   ├── faq.py                  # FAQ agent for general questions
│   ├── planner.py              # Planner agent for request routing
│   ├── skernel.py              # Semantic Kernel utilities
│   └── config.py               # Agent configuration settings
├── models/
│   ├── __init__.py
│   └── schemas.py              # Pydantic data models for API
├── process/
│   ├── __init__.py
│   └── message_processor.py    # Core message processing logic
├── config/
│   ├── __init__.py
│   ├── settings.py             # Environment-based configuration
│   ├── constants.py            # Application constants
│   └── telemetry.py            # Telemetry configuration
├── telemetry/                  # Observability and monitoring
│   ├── __init__.py
│   ├── aspire.py               # .NET Aspire Dashboard integration
│   ├── appinsights.py          # Azure Application Insights
│   ├── filelog.py              # File-based logging
│   └── httpx_logger.py         # HTTP request logging
├── tests/                      # Comprehensive test suite
│   ├── __init__.py
│   ├── config.py               # Test configuration
│   └── features/               # BDD tests with Behave
│       ├── environment.py      # Test environment setup
│       ├── *.feature           # Gherkin feature files
│       └── steps/              # Test step definitions
├── scripts/                    # Helper scripts
│   ├── start_server.sh         # Server startup script
│   ├── run_bdd_tests.sh        # Test runner script
│   ├── docker-build.sh         # Docker build script
│   ├── docker-run.sh           # Docker run script
│   └── check-types.sh          # Type checking script
├── .behaverc                   # Behave configuration
├── .python-version             # Python version specification
└── .env.example                # Environment variables template
```

## 🔌 API Endpoints

### Core Message Processing
- **POST /messages** - Submit message for AI processing
- **GET /messages/{id}/updates** - Get real-time processing updates
- **GET /messages/{id}/status** - Get current message status
- **GET /messages** - List all messages with pagination

### System & Health
- **GET /health** - Health check with uptime and version
- **GET /** - Root endpoint (redirects to documentation)

### Documentation
- **GET /docs** - Interactive Swagger UI documentation
- **GET /redoc** - Alternative ReDoc documentation
- **GET /swagger** - Alternative path to Swagger UI

### Example Usage

#### Submit Message for AI Processing
```bash
curl -X POST http://localhost:8000/messages \
  -H "Content-Type: application/json" \
  -H "x-ms-conversation-id: thread-123" \
  -d '{"message": "What is my current bill?"}'

# Response
{
  "message_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "received", 
  "received_at": "2025-07-09T10:30:00.123456"
}
```

#### Monitor Processing Updates
```bash
curl http://localhost:8000/messages/550e8400-e29b-41d4-a716-446655440000/updates

# Response
[
  {
    "message_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "received",
    "processed_at": "2025-07-09T10:30:00.234567",
    "result": "Message received and sent to the agent.",
    "agent_name": null
  },
  {
    "message_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "completed",
    "processed_at": "2025-07-09T10:30:02.345678",
    "result": "Your current bill is £45.50. This includes your monthly plan...",
    "agent_name": "BillingAgent"
  }
]
```

#### Check Message Status
```bash
curl http://localhost:8000/messages/550e8400-e29b-41d4-a716-446655440000/status

# Response
{
  "message_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "content": "What is my current bill?",
  "timestamp": "2025-07-09T10:30:00.123456"
}
```

## ⚙️ Configuration

The API uses environment variables for configuration with sensible defaults for development.

### Environment Variables

Create a `.env` file in the backend directory:

```bash
# Copy the example file
cp .env.example .env
```

#### **API Configuration**
```bash
# API Metadata
API_TITLE=Semker Async Message Processing API
API_VERSION=1.0.0
API_DESCRIPTION=AI-powered asynchronous message processing service
DEBUG=false

# Contact Information
CONTACT_NAME=Semker API Support
CONTACT_EMAIL=support@semker.dev
CONTACT_URL=https://semker.dev/support

# License Information
LICENSE_NAME=MIT License
LICENSE_URL=https://opensource.org/licenses/MIT
```

#### **Server Configuration**
```bash
# Server Settings
SERVER_HOST=localhost
SERVER_PORT=8000
SERVER_URL=http://localhost:8000
SERVER_DESCRIPTION=Development server

# Processing Parameters
MESSAGE_PROCESSING_DELAY=5.0
MAX_MESSAGE_LENGTH=10000

# Performance Settings
REQUEST_TIMEOUT=30
MAX_CONNECTIONS=100
```

#### **CORS Configuration**
```bash
# CORS Settings
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CORS_ALLOW_CREDENTIALS=true
CORS_ALLOW_METHODS=*
CORS_ALLOW_HEADERS=*
```

#### **Telemetry Configuration**
```bash
# Telemetry Backend Selection
SEMKER_LOGGING_TYPE=aspire  # Options: aspire, appinsights, filelog

# OpenTelemetry Settings
TELEMETRY_ENABLED=true
TELEMETRY_CONSOLE=false
OTLP_ENDPOINT=http://localhost:4317

# Logging Settings
LOG_LEVEL=INFO
LOG_FOLDER=logs
MAX_LOG_SIZE_MB=10
LOG_BACKUP_COUNT=5
```

#### **AI Agent Configuration**
```bash
# MCP Server Endpoints
BILLING_MCP_SERVER_URL=http://localhost:3001
ROAMING_MCP_SERVER_URL=http://localhost:3002
TARIFF_MCP_SERVER_URL=http://localhost:3003
FAQ_MCP_SERVER_URL=http://localhost:3004

# Semantic Kernel Settings
AZURE_OPENAI_ENDPOINT=https://your-openai-endpoint.openai.azure.com
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
```

### Configuration Classes

The configuration is organized into logical groups:

- **`APISettings`**: API metadata and documentation
- **`ContactSettings`**: Contact information for support
- **`LicenseSettings`**: License information for legal compliance
- **`ServerSettings`**: Server runtime configuration and performance tuning

### Example Production Configuration

```bash
# Production API settings
API_TITLE=Semker Production API
DEBUG=false
SERVER_HOST=0.0.0.0
SERVER_PORT=8080

# Production CORS (restrict origins)
CORS_ORIGINS=https://semker.app,https://admin.semker.app
CORS_ALLOW_CREDENTIALS=true

# Production telemetry
SEMKER_LOGGING_TYPE=appinsights
TELEMETRY_ENABLED=true
LOG_LEVEL=WARNING

# Production performance
MESSAGE_PROCESSING_DELAY=1.0
MAX_CONNECTIONS=1000
REQUEST_TIMEOUT=60
```

## 📊 Data Models

All data models use Pydantic for type safety, validation, and automatic OpenAPI documentation.

### Input Models

#### **Message** (Request)
```python
class Message(BaseModel):
    message: str  # The user's message content for AI processing
    
    # Example
    {
        "message": "What is my current bill?"
    }
```

### Response Models

#### **MessageResponse** (Message Submission)
```python
class MessageResponse(BaseModel):
    message_id: str      # Unique UUID for the message
    status: str          # Initial status (always "received")
    received_at: datetime # When message was received
    
    # Example
    {
        "message_id": "550e8400-e29b-41d4-a716-446655440000",
        "status": "received",
        "received_at": "2025-07-09T10:30:00.123456"
    }
```

#### **UpdateResponse** (Processing Updates)
```python
class UpdateResponse(BaseModel):
    message_id: str              # Message identifier
    status: str                  # Current processing status
    processed_at: datetime       # When this update was generated
    result: Optional[str]        # Processing result or status message
    agent_name: Optional[str]    # Name of the AI agent that generated this update
    
    # Example
    {
        "message_id": "550e8400-e29b-41d4-a716-446655440000",
        "status": "completed",
        "processed_at": "2025-07-09T10:30:02.345678",
        "result": "Your current bill is £45.50. This includes...",
        "agent_name": "BillingAgent"
    }
```

#### **HealthResponse** (System Health)
```python
class HealthResponse(BaseModel):
    status: str           # System health status
    timestamp: datetime   # Current system time
    version: str          # Application version
    uptime_seconds: float # System uptime in seconds
    
    # Example
    {
        "status": "healthy",
        "timestamp": "2025-07-09T10:30:00.123456",
        "version": "1.0.0",
        "uptime_seconds": 3600.0
    }
```

### Status Flow

Messages progress through the following statuses:

1. **`received`** - Message submitted and queued for processing
2. **`inprogress`** - AI agent is processing the message
3. **`completed`** - Processing finished successfully
4. **`failed`** - Processing encountered an error
5. **`cancelled`** - Processing was cancelled (future feature)

### Validation Features

- **Type Safety**: All fields have explicit types with runtime validation
- **Field Descriptions**: Comprehensive field documentation for API docs
- **Example Values**: Realistic examples for interactive documentation
- **Optional Fields**: Proper handling of optional data with defaults
- **DateTime Handling**: Automatic ISO format serialization/deserialization
- **UUID Validation**: Proper UUID format validation for message IDs

## Message Processing Flow

1. **Submit** → Message received, assigned UUID, stored with "received" status
2. **Queue** → Background task initiated for asynchronous processing
3. **Process** → Status updated to "processing", intermediate update stored
4. **Complete** → Status updated to "processed", final result stored
5. **Retrieve** → Client can poll `/updates` endpoint for real-time status

## 🧪 Testing

The backend uses comprehensive Behavior-Driven Development (BDD) testing with Behave and Gherkin syntax.

### Running Tests

#### **All Tests**
```bash
# Using the test script (recommended)
./scripts/run_bdd_tests.sh

# Using UV directly
uv run behave tests/features

# Using Python directly
python -m behave tests/features
```

#### **Specific Test Features**
```bash
# Message processing tests
./scripts/run_bdd_tests.sh message_api

# Error handling tests
./scripts/run_bdd_tests.sh error_handling

# Health check tests
./scripts/run_bdd_tests.sh health_check

# Smoke tests only
./scripts/run_bdd_tests.sh smoke
```

#### **Test Output Options**
```bash
# Verbose output
uv run behave tests/features --verbose

# Specific tags
uv run behave tests/features --tags=@smoke

# JSON output for CI/CD
uv run behave tests/features --format json
```

### Test Structure

```
tests/
├── config.py                    # Test configuration
├── features/                    # BDD feature files
│   ├── environment.py           # Test environment setup
│   ├── message_api.feature      # Core message processing tests
│   ├── error_handling.feature   # Error scenario tests
│   ├── health_check.feature     # Health endpoint tests
│   └── steps/                   # Step definitions
│       ├── __init__.py
│       └── api_steps.py         # Python step implementations
└── .behaverc                    # Behave configuration
```

### Test Coverage

#### **Message Processing Tests**
- Message submission with valid data
- Message processing with AI agents
- Real-time status updates
- Conversation thread management
- Background task execution

#### **Error Handling Tests**
- Invalid message format
- Missing required headers
- Message not found scenarios
- Server error responses
- Validation error handling

#### **Health & System Tests**
- Health check endpoint
- System uptime tracking
- Version information
- Service availability

#### **API Documentation Tests**
- OpenAPI schema validation
- Interactive documentation access
- Endpoint discoverability

### Example Test Scenarios

```gherkin
Feature: Message Processing API
    
    Scenario: Submit message for processing
        Given the API is running
        When I submit a message "What is my bill?" with thread ID "test-123"
        Then I should receive a message ID
        And the status should be "received"
        And the message should be processed asynchronously
        
    Scenario: Get processing updates
        Given I have submitted a message
        When I request updates for the message
        Then I should receive a list of updates
        And each update should have a timestamp
        And the final status should be "completed"
        
    Scenario: Handle missing conversation ID
        Given the API is running
        When I submit a message without a conversation ID header
        Then I should receive a 400 Bad Request error
        And the error message should mention "x-ms-conversation-id"
```

### Test Configuration

The test suite uses:
- **Behave**: BDD framework for Python
- **Requests**: HTTP client for API testing
- **Pytest**: Additional testing utilities
- **Mock**: Mocking external dependencies
- **Fixtures**: Test data and setup helpers

### Running Tests in CI/CD

```bash
# Install test dependencies
uv sync --group test

# Run tests with coverage
uv run behave tests/features --format json --outfile test_results.json

# Type checking
uv run mypy src/backend

# Linting
uv run ruff check src/backend
```

### Test Best Practices

- **Isolated Tests**: Each test is independent
- **Real API**: Tests run against the actual FastAPI application
- **Comprehensive Coverage**: All endpoints and error scenarios
- **Readable Scenarios**: Natural language test descriptions
- **Maintainable**: Clear step definitions and reusable test helpers

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

## 🏗️ Architecture Overview

The backend follows a clean, modular architecture with AI-powered message processing:

### Core Components

#### **API Layer** (`api.py`)
- FastAPI route definitions and endpoint handlers
- Request/response validation and serialization
- OpenAPI documentation generation
- CORS middleware and telemetry instrumentation

#### **AI Agent System** (`agents/`)
- **Base Agent** (`base.py`): Abstract base class for all agents
- **Specialized Agents**: Billing, Roaming, Tariff, FAQ, Planner agents
- **Semantic Kernel Integration** (`skernel.py`): Microsoft Semantic Kernel utilities
- **Model Context Protocol**: Integration with external services
- **Conversation Management**: Thread-based context preservation

#### **Message Processing** (`process/`)
- **MessageProcessor**: Core business logic for message handling
- Asynchronous processing with background tasks
- Real-time status updates and intermediate responses
- Thread management for conversation context

#### **Configuration** (`config/`)
- **Settings** (`settings.py`): Environment-dependent configuration
- **Constants** (`constants.py`): Immutable application constants
- **Telemetry** (`telemetry.py`): Observability configuration

#### **Data Models** (`models/`)
- **Pydantic Schemas**: Type-safe data validation
- Request/response models with comprehensive validation
- OpenAPI documentation generation

#### **Telemetry** (`telemetry/`)
- **Multi-backend Support**: Aspire, Application Insights, File logging
- **OpenTelemetry Integration**: Distributed tracing and metrics
- **Automatic Instrumentation**: FastAPI and requests library

### AI Processing Flow

1. **Message Submission** → API receives message with conversation ID
2. **Agent Selection** → Planner agent or direct routing to specialized agent
3. **Context Retrieval** → Load conversation thread for context
4. **AI Processing** → Semantic Kernel processes message with MCP integration
5. **Intermediate Updates** → Real-time status updates via callbacks
6. **Response Generation** → Final response with conversation context updated
7. **Status Tracking** → All updates stored for client polling

### Separation of Concerns

- **API Layer**: HTTP handling, validation, documentation
- **Business Logic**: Message processing, AI orchestration, status tracking
- **Data Layer**: In-memory storage with thread management
- **AI Layer**: Agent specialization, context management, external service integration
- **Configuration**: Environment-based settings vs. immutable constants
- **Observability**: Comprehensive telemetry and monitoring

### Key Design Principles

- **Async-First**: All operations designed for high concurrency
- **Type Safety**: Comprehensive type hints and Pydantic validation
- **Modularity**: Clear separation between components
- **Extensibility**: Easy to add new agents and services
- **Observability**: Built-in monitoring and tracing
- **Testability**: Comprehensive BDD test coverage

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

## 🚀 Deployment

The backend supports multiple deployment options from development to production.

### Development Deployment

```bash
# Local development server
uv run python start_server.py

# With auto-reload
uv run uvicorn api:app --reload --host 0.0.0.0 --port 8000

# With specific environment
ENV=development uv run python start_server.py
```

### Production Deployment

#### **Docker Deployment**
```bash
# Build and run with helper scripts
./scripts/docker-build.sh
./scripts/docker-run.sh

# Manual Docker commands
docker build -t semker-api:latest .
docker run -p 8000:8000 -e PORT=8000 semker-api:latest

# Docker Compose
docker-compose up -d api                    # Development
docker-compose --profile production up -d   # Production with nginx
```

#### **Production Server with Gunicorn**
```bash
# Install production dependencies
uv add gunicorn

# Run with multiple workers
gunicorn api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# With production settings
gunicorn api:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile - \
  --log-level info
```

#### **Environment-Specific Configuration**
```bash
# Production environment variables
export ENV=production
export DEBUG=false
export LOG_LEVEL=WARNING
export CORS_ORIGINS=https://semker.app
export SERVER_HOST=0.0.0.0
export SERVER_PORT=8080
```

### Monitoring & Observability

#### **Health Checks**
- **Kubernetes**: Use `/health` endpoint for liveness/readiness probes
- **Load Balancers**: Configure health checks on `/health`
- **Monitoring**: Set up alerts on health check failures

#### **Telemetry Integration**
```bash
# .NET Aspire Dashboard
SEMKER_LOGGING_TYPE=aspire
OTLP_ENDPOINT=http://localhost:4317

# Azure Application Insights
SEMKER_LOGGING_TYPE=appinsights
APPLICATIONINSIGHTS_CONNECTION_STRING=your_connection_string

# File-based logging
SEMKER_LOGGING_TYPE=filelog
LOG_LEVEL=INFO
LOG_FOLDER=/var/log/semker
```

#### **Performance Monitoring**
- **Metrics**: Request duration, success rates, error rates
- **Tracing**: End-to-end request tracing across services
- **Logging**: Structured logging with correlation IDs

### Production Considerations

#### **Security**
- Use HTTPS in production
- Restrict CORS origins to known domains
- Implement rate limiting
- Use secure headers middleware
- Regular security updates

#### **Performance**
- Configure appropriate worker counts
- Use connection pooling
- Enable compression
- Optimize database queries (when database is added)
- Cache frequently accessed data

#### **Reliability**
- Implement circuit breakers
- Add retry logic for external services
- Use health checks for automatic restarts
- Monitor system resources
- Set up backup and recovery procedures

### Cloud Deployment

#### **Azure Container Instances**
```bash
# Deploy to Azure
az container create \
  --resource-group semker-rg \
  --name semker-api \
  --image semker-api:latest \
  --cpu 1 \
  --memory 2 \
  --ports 8000 \
  --environment-variables ENV=production
```

#### **Kubernetes**
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: semker-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: semker-api
  template:
    metadata:
      labels:
        app: semker-api
    spec:
      containers:
      - name: semker-api
        image: semker-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: ENV
          value: "production"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
```

## 🔮 Future Enhancements

### Immediate Roadmap

#### **Database Integration**
- **PostgreSQL**: Replace in-memory storage with persistent database
- **Connection Pooling**: Implement efficient database connections
- **Migrations**: Database schema version management
- **Backup & Recovery**: Automated database backup strategies

#### **Enhanced AI Capabilities**
- **Multi-modal Support**: Image and document processing
- **Custom Agent Training**: Fine-tuned models for specific domains
- **Agent Orchestration**: Complex multi-agent workflows
- **Real-time Streaming**: WebSocket support for streaming responses

#### **Advanced Features**
- **Authentication & Authorization**: JWT-based user authentication
- **Rate Limiting**: API usage quotas and throttling
- **Caching**: Redis integration for improved performance
- **Message Queuing**: RabbitMQ or Apache Kafka for scalability

### Long-term Vision

#### **Scalability Improvements**
- **Microservices Architecture**: Split into specialized services
- **Event-Driven Architecture**: Asynchronous event processing
- **Auto-scaling**: Dynamic resource allocation based on load
- **Load Balancing**: Intelligent request distribution

#### **Enterprise Features**
- **Multi-tenancy**: Support for multiple organizations
- **Audit Logging**: Comprehensive audit trail
- **Compliance**: GDPR, HIPAA compliance features
- **Advanced Analytics**: Usage analytics and insights

#### **Integration Ecosystem**
- **Webhook Support**: Real-time event notifications
- **GraphQL API**: Alternative query interface
- **SDK Development**: Client libraries for multiple languages
- **Plugin System**: Extensible architecture for custom integrations

#### **AI & Machine Learning**
- **Sentiment Analysis**: Emotional intelligence in responses
- **Personalization**: User-specific response customization
- **Predictive Analytics**: Anticipate user needs
- **Automated Learning**: Continuous improvement from interactions

### Contributing to Development

#### **Development Setup**
1. Fork the repository
2. Create a feature branch
3. Follow coding standards (PEP 8, type hints)
4. Write comprehensive tests
5. Update documentation
6. Submit pull request

#### **Code Quality Standards**
- **Type Safety**: Full type annotations
- **Documentation**: Comprehensive docstrings
- **Testing**: BDD tests for all features
- **Performance**: Async/await patterns
- **Security**: Secure coding practices

#### **Review Process**
- Code review by maintainers
- Automated testing validation
- Performance impact assessment
- Documentation completeness check
- Security vulnerability scanning

---

The Semker backend is designed to be a foundation for intelligent, scalable, and maintainable AI-powered applications. Whether you're building a customer service chatbot, a technical support system, or a complex AI workflow, the modular architecture provides the flexibility to grow with your needs.
