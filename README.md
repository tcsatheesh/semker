# Semker

A full-stack asynchronous message processing system with a FastAPI backend and React TypeScript frontend featuring a modern real-time chat interface.

## Features

### 🎯 **Enhanced Chat Interface**
- **Real-time Communication**: Send messages and receive server responses with live status updates
- **Duration Tracking**: See request/response times for performance insights
- **Intermediate Status Updates**: Watch message processing with real-time polling
- **Modern UI**: Clean, responsive chat bubbles with animations and visual feedback
- **Connection Management**: Live connection status with auto-reconnect functionality
- **Mobile-Friendly**: Responsive design that works seamlessly on all devices

### 🔧 **Robust Backend API**
- **FastAPI Framework**: High-performance async API with automatic OpenAPI documentation
- **Asynchronous Processing**: Background message processing with status tracking
- **Health Monitoring**: Built-in health checks and uptime tracking
- **CORS Support**: Configurable cross-origin policies for frontend integration
- **BDD Testing**: Comprehensive behavior-driven development test suite

### 🖥️ **Type-Safe Frontend**
- **React TypeScript**: Modern functional components with full type safety
- **Component Architecture**: Modular, reusable component design
- **API Integration**: Robust error handling with retry mechanisms
- **Build Pipeline**: Optimized production builds with Create React App

## Quick Start

### Prerequisites
- **Python 3.12+** for backend
- **Node.js 18+** for frontend
- **npm** or **yarn** package manager

### 1. Backend Setup
```bash
cd src/backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup
```bash
cd src/frontend
npm install
npm start
```

### 3. Access the Application
- **Chat Interface**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## Usage

### Chat Interface Experience
1. Open http://localhost:3000 in your browser
2. Verify connection status shows "Connected" (green indicator)
3. Type your message and press Enter or click "Send"
4. Watch the complete message flow:
   - **Sending**: Loading indicator appears
   - **Received**: "✅ Message received and queued..." (with duration)
   - **Processing**: "⚡ Processing your message..." (with pulse animation)
   - **Complete**: "✅ Message processed successfully!" (final result)

### API Endpoints
- `GET /health` - Health check and uptime
- `POST /messages` - Submit message for processing
- `GET /messages` - List all processed messages
- `GET /messages/{id}` - Get specific message details
- `GET /messages/{id}/updates` - Get real-time processing updates

### Example API Usage
```bash
# Send a message
curl -X POST http://localhost:8000/messages \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, Semker!"}'

# Response: {"message_id": "...", "status": "received", "received_at": "..."}

# Check processing status
curl http://localhost:8000/messages/{message_id}/updates

# Get all messages
curl http://localhost:8000/messages

# Health check
curl http://localhost:8000/health
```

## Development

### Running Tests
```bash
# Backend BDD tests
cd src/backend
python -m behave tests/features/

# Frontend build verification
cd src/frontend
npm run build
npm test
```

### Project Structure
```
semker/
├── README.md                    # This file
├── src/
│   ├── backend/                 # FastAPI backend
│   │   ├── README.md           # Backend documentation
│   │   ├── api.py              # Main API application
│   │   ├── models/             # Pydantic data models
│   │   ├── process/            # Message processing logic
│   │   ├── config/             # Configuration and settings
│   │   ├── tests/              # BDD test suite
│   │   └── requirements.txt    # Python dependencies
│   └── frontend/               # React TypeScript frontend
│       ├── README.md          # Frontend documentation
│       ├── src/               # React components and services
│       ├── public/            # Static assets
│       └── package.json       # Node.js dependencies
└── scripts/                   # Utility and test scripts
```

## Configuration

### Environment Variables

#### Backend (.env in src/backend/)
```bash
# CORS settings
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CORS_ALLOW_CREDENTIALS=true

# Processing settings
MESSAGE_PROCESSING_DELAY=2.0

# Logging
LOG_LEVEL=INFO

# Telemetry (optional)
TELEMETRY_ENABLED=false
```

#### Frontend (.env in src/frontend/)
```bash
# API endpoint
REACT_APP_API_URL=http://localhost:8000
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
