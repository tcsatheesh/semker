# Semker

A semantic kernel-based project with a FastAPI backend service.

## Project Structure

This project is organized into a modular structure:

- **`src/backend/`** - FastAPI backend service with async message processing
  - **`models/`** - Pydantic data models
  - **`api.py`** - Main FastAPI application
  - **`README.md`** - Detailed backend documentation

## Quick Start

Navigate to the backend directory for the FastAPI service:

```bash
cd src/backend
python start_server.py
```

For detailed API documentation and usage instructions, see [`src/backend/README.md`](src/backend/README.md).

## API Documentation

Once the server is running:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Dependencies

This project uses:
- **FastAPI** - Modern web framework for building APIs
- **Pydantic** - Data validation and serialization
- **Uvicorn** - ASGI server for production
- **UV** - Fast Python package installer and resolver
