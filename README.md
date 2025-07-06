# Semker

A comprehensive AI-powered telecommunications platform featuring multiple components for customer service automation, real-time messaging, and observability.

## Components

### 🤖 **MCP Server** (Model Context Protocol)
- **AI-Powered Tools**: Semantic Kernel-based customer service automation
- **Telecommunications Focus**: Billing, roaming, tariff, broadband, and ticket management
- **Interactive Documentation**: Auto-generated Swagger/OpenAPI docs
- **Type Safety**: Full mypy strict type checking with Pydantic models
- **Production Ready**: Telemetry integration with OpenTelemetry and Aspire Dashboard

### 💬 **Real-time Chat Interface** 
- **WebSocket Communication**: Send messages and receive server responses with live status updates
- **Duration Tracking**: See request/response times for performance insights
- **Intermediate Status Updates**: Watch message processing with real-time polling
- **Modern UI**: Clean, responsive chat bubbles with animations and visual feedback
- **Connection Management**: Live connection status with auto-reconnect functionality

### 📊 **Log Viewer**
- **React-based Interface**: Modern log viewing experience with syntax highlighting
- **Conversation Grouping**: Organized tree view of conversations and interactions
- **JSON Highlighting**: Syntax-highlighted request/response data
- **Theme Support**: Light/dark mode toggle matching the main frontend
- **Real-time Updates**: Live log monitoring and filtering capabilities

### 🔧 **FastAPI Backend**
- **Asynchronous Processing**: Background message processing with status tracking
- **Health Monitoring**: Built-in health checks and uptime tracking
- **File-based Logging**: Structured logging with automatic rotation
- **CORS Support**: Configurable cross-origin policies for frontend integration
- **BDD Testing**: Comprehensive behavior-driven development test suite

## Features

### 🎯 **AI-Powered Customer Service**
- **Multi-Agent Architecture**: Specialized agents for billing, roaming, tariff, broadband, and ticketing
- **Intelligent Routing**: Automatic request routing to appropriate service agents
- **Context Awareness**: Conversation context maintained across interactions
- **Tool Integration**: Native integration with customer service tools and APIs

### 📈 **Observability & Monitoring**
- **OpenTelemetry Integration**: Distributed tracing, metrics, and logging
- **Aspire Dashboard**: .NET Aspire integration for development observability
- **Log Aggregation**: Centralized logging with structured formats
- **Performance Tracking**: Request/response timing and system metrics

### 🖥️ **Type-Safe Development**
- **React TypeScript**: Modern functional components with full type safety
- **Component Architecture**: Modular, reusable component design
- **API Integration**: Robust error handling with retry mechanisms
- **Build Pipeline**: Optimized production builds with Create React App

## Quick Start

### Using the Convenient Scripts

The fastest way to get started is using the provided scripts in the `scripts/` directory:

```bash
# Start all components with one command each:

# 1. Start the MCP Server (AI customer service)
./scripts/start-mcpserver.sh
# Runs on http://localhost:8002
# Access docs at http://localhost:8002/docs

# 2. Start the main backend (message processing)
./scripts/start-backend.sh
# Runs on http://localhost:8000
# Access docs at http://localhost:8000/docs

# 3. Start the frontend (chat interface)
./scripts/start-frontend.sh
# Runs on http://localhost:3000

# 4. Start the log viewer (monitoring interface)
./scripts/start-logviewer.sh
# Runs on http://localhost:3001

# 5. Start with Aspire Dashboard (advanced monitoring)
./scripts/start-aspire.sh
# Backend on http://localhost:8000 with telemetry
# Aspire Dashboard typically on http://localhost:18888

# 6. Run comprehensive BDD tests
./scripts/run-bdd-tests.sh
```

### Manual Setup

If you prefer manual setup or need more control:

### Prerequisites
- **Python 3.12+** for backend components
- **Node.js 18+** for frontend components  
- **uv** for Python package management (recommended)
- **.NET 8+** for Aspire Dashboard (optional)

### 1. MCP Server Setup (AI Customer Service)
```bash
cd src/mcpserver
uv sync
python dev_server.py
# Access at http://localhost:8002/docs
```

### 2. Backend Setup (Message Processing)
```bash
cd src/backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup (Chat Interface)
```bash
cd src/frontend
npm install
npm start
```

### 4. Log Viewer Setup (Monitoring)
```bash
cd src/logviewer
npm install
npm run build
python app.py
# Access at http://localhost:3001
```

### 5. Access the Applications
- **MCP Server (AI Tools)**: http://localhost:8002/docs
- **Chat Interface**: http://localhost:3000  
- **Backend API**: http://localhost:8000/docs
- **Log Viewer**: http://localhost:3001
- **Aspire Dashboard**: http://localhost:18888 (when using start-aspire.sh)

## Usage

## Usage

### AI Customer Service (MCP Server)
1. Access the MCP Server at http://localhost:8002/docs
2. Explore the available AI tools:
   - **Billing**: Customer billing and invoice management
   - **Roaming**: International roaming charges by country
   - **Tariff**: Tariff plans and pricing structures
   - **Broadband**: Router troubleshooting guidance  
   - **Ticket**: Support ticket management with chat history
3. Test the interactive API endpoints directly in the Swagger UI

### Chat Interface Experience
1. Open http://localhost:3000 in your browser
2. Verify connection status shows "Connected" (green indicator)
3. Type your message and press Enter or click "Send"
4. Watch the complete message flow:
   - **Sending**: Loading indicator appears
   - **Received**: "✅ Message received and queued..." (with duration)
   - **Processing**: "⚡ Processing your message..." (with pulse animation)
   - **Complete**: "✅ Message processed successfully!" (final result)

### Log Monitoring
1. Open the Log Viewer at http://localhost:3001
2. Browse conversations in the tree view on the left
3. View detailed request/response data with syntax highlighting
4. Toggle between light/dark modes for comfortable viewing
5. Monitor real-time system activity and API calls

### API Integration Examples

#### MCP Server (AI Tools)
```bash
# Get customer billing data
curl -X POST http://localhost:8002/bill/mcp \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/call", "params": {"name": "get_billing_data", "arguments": {"month": 6}}}'

# Get roaming charges
curl -X POST http://localhost:8002/roam/mcp \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/call", "params": {"name": "get_roaming_charges", "arguments": {"country": "Spain", "month": 6}}}'

# Get tariff information
curl -X POST http://localhost:8002/tariff/mcp \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/call", "params": {"name": "get_tariff_plan", "arguments": {"pricing_structure": "prepaid"}}}'
```

#### Backend API (Message Processing)
```bash
# Send a message for processing
curl -X POST http://localhost:8000/messages \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, Semker!"}'

# Response: {"message_id": "...", "status": "received", "received_at": "..."}

# Check processing status
curl http://localhost:8000/messages/{message_id}/updates

# Health check
curl http://localhost:8000/health
```

## Development

## Development

### Available Scripts

The `scripts/` directory contains convenient startup scripts for development:

- **`start-mcpserver.sh`**: Start the MCP Server with AI customer service tools
- **`start-backend.sh`**: Start the main backend API server
- **`start-frontend.sh`**: Start the React frontend development server
- **`start-logviewer.sh`**: Start the log viewer interface
- **`start-aspire.sh`**: Start backend with .NET Aspire Dashboard integration
- **`run-bdd-tests.sh`**: Execute comprehensive behavior-driven development tests

### Running Tests
```bash
# Backend BDD tests
./scripts/run-bdd-tests.sh

# Or manually:
cd src/backend
python -m behave tests/features/

# Frontend build verification
cd src/frontend
npm run build
npm test

# MCP Server type checking
cd src/mcpserver
mypy --strict .
```

### Development with Observability

For advanced monitoring and observability during development:

```bash
# Start with Aspire Dashboard integration
./scripts/start-aspire.sh

# This provides:
# - Distributed tracing
# - Real-time metrics
# - Structured logging
# - Performance insights
```

### Project Structure
```
semker/
├── README.md                    # This file - main project documentation
├── LICENSE                     # MIT license
├── scripts/                    # Convenient startup and test scripts
│   ├── start-mcpserver.sh      # Start MCP Server (AI tools)
│   ├── start-backend.sh        # Start main backend API
│   ├── start-frontend.sh       # Start React frontend
│   ├── start-logviewer.sh      # Start log viewer interface
│   ├── start-aspire.sh         # Start with Aspire Dashboard
│   └── run-bdd-tests.sh        # Run BDD test suite
├── src/
│   ├── mcpserver/              # AI-powered MCP server
│   │   ├── README.md           # MCP server documentation
│   │   ├── main.py             # FastAPI MCP application
│   │   ├── dev_server.py       # Development server script
│   │   ├── tools/              # AI tool implementations
│   │   │   ├── billing/        # Billing management tools
│   │   │   ├── roaming/        # Roaming service tools
│   │   │   ├── tariff/         # Tariff management tools
│   │   │   ├── broadband/      # Broadband support tools
│   │   │   └── ticket/         # Ticket management tools
│   │   └── telemetry/          # OpenTelemetry integration
│   ├── backend/                # Main FastAPI backend
│   │   ├── README.md           # Backend documentation
│   │   ├── api.py              # Main API application
│   │   ├── models/             # Pydantic data models
│   │   ├── process/            # Message processing logic
│   │   ├── config/             # Configuration and settings
│   │   ├── telemetry/          # Observability and logging
│   │   ├── tests/              # BDD test suite
│   │   └── logs/               # Application log files
│   ├── frontend/               # React TypeScript frontend
│   │   ├── README.md           # Frontend documentation
│   │   ├── src/                # React components and services
│   │   ├── public/             # Static assets
│   │   └── package.json        # Node.js dependencies
│   └── logviewer/              # Log monitoring interface
│       ├── app.py              # Flask server for log viewer
│       ├── src/                # React log viewer components
│       ├── public/             # Static assets
│       └── package.json        # Node.js dependencies
└── .gitignore                  # Git ignore patterns
```

## Configuration

## Configuration

### Port Configuration
- **MCP Server**: 8002 (AI customer service tools)
- **Backend API**: 8000 (message processing)
- **Frontend**: 3000 (chat interface)
- **Log Viewer**: 3001 (monitoring interface)
- **Aspire Dashboard**: 18888 (observability, when enabled)

### Environment Variables

#### MCP Server (.env in src/mcpserver/)
```bash
# Server settings
PORT=8002
HOST=0.0.0.0

# OpenTelemetry settings
OTLP_ENDPOINT=http://localhost:4317
TELEMETRY_ENABLED=true
```

#### Backend (.env in src/backend/)
```bash
# CORS settings
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CORS_ALLOW_CREDENTIALS=true

# Processing settings
MESSAGE_PROCESSING_DELAY=2.0

# Logging
LOG_LEVEL=INFO
LOG_FOLDER=logs
MAX_LOG_SIZE_MB=10

# Telemetry (optional)
TELEMETRY_ENABLED=false
OTLP_ENDPOINT=http://localhost:4317
```

#### Frontend (.env in src/frontend/)
```bash
# API endpoints
REACT_APP_API_URL=http://localhost:8000
REACT_APP_MCP_URL=http://localhost:8002
```

#### Log Viewer (.env in src/logviewer/)
```bash
# Flask server settings
FLASK_ENV=development
PORT=3001
```

## Message Schema

### Request Format
```json
{
  "message": "Your message content here"
}
```

### Response Format
```json
{
  "message_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "received",
  "received_at": "2025-07-04T10:30:00.123456"
}
```

### Status Updates Format
```json
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
    "result": "Processed message: Your message content here..."
  }
]
```

## Key Features Detail

### Enhanced Chat Interface
- **Duration Tracking**: Every request shows timing (e.g., "15ms", "1.2s")
- **Intermediate Polling**: Real-time status updates with 1-second polling
- **Visual Feedback**: Pulse animations for in-progress messages
- **Status Progression**: received → processing → processed
- **Auto-cleanup**: Intermediate messages disappear when processing completes
- **Error Handling**: Graceful degradation with retry mechanisms

### Backend Processing
- **Async Operations**: Non-blocking message processing
- **Status Tracking**: Complete lifecycle from received to processed
- **Health Monitoring**: Uptime tracking and service health
- **Type Safety**: Full Pydantic model validation
- **Test Coverage**: Comprehensive BDD test suite

## Troubleshooting

### Common Issues
1. **CORS Errors**: Ensure CORS_ORIGINS includes frontend URL
2. **Connection Failed**: Check both servers are running on correct ports
3. **Build Errors**: Verify Node.js and Python versions meet requirements

### Debug Mode
```bash
# Backend with debug logging
cd src/backend
LOG_LEVEL=DEBUG python -m uvicorn api:app --reload

# Frontend development mode
cd src/frontend
npm start
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

For detailed backend and frontend documentation, see the respective README files in `src/backend/` and `src/frontend/`.
