# Multi-stage Dockerfile for Semker API
# Stage 1: Build stage with uv for dependency management
FROM python:3.12-slim AS builder

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_CACHE_DIR=/tmp/.uv-cache

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies using uv
RUN uv sync --frozen --no-dev --no-cache

# Stage 2: Production stage
FROM python:3.12-slim AS production

# Install system dependencies for production
RUN apt-get update && apt-get install -y \
    curl \
    dumb-init \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user for security
RUN groupadd -r semker && useradd -r -g semker -d /app semker

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app" \
    HOST=0.0.0.0 \
    PORT=8000 \
    HEALTH_CHECK_URL="http://127.0.0.1:8000/health"

# Set working directory
WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy application code with proper ownership
COPY --chown=semker:semker *.py ./
COPY --chown=semker:semker models/ ./models/
COPY --chown=semker:semker process/ ./process/
COPY --chown=semker:semker config/ ./config/

# Create necessary directories with proper permissions
RUN mkdir -p /app/logs /app/data && \
    chown -R semker:semker /app && \
    chmod -R 755 /app

# Switch to non-root user
USER semker

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f ${HEALTH_CHECK_URL} || exit 1

# Use dumb-init for proper signal handling
ENTRYPOINT ["dumb-init", "--"]

# Default command with configurable host and port
CMD ["sh", "-c", "uvicorn api:app --host ${HOST} --port ${PORT} --workers 1"]
