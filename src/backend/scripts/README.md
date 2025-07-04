# Semker Backend Scripts

This directory contains all shell scripts for the Semker backend project.

## Available Scripts

### 🐳 Docker Scripts

- **`docker-build.sh`** - Build the Docker image for the Semker backend
  ```bash
  ./scripts/docker-build.sh
  ```

- **`docker-run.sh`** - Run the Semker backend in a Docker container
  ```bash
  ./scripts/docker-run.sh [options]
  ```
  Options:
  - `--host <host>` - Set the host (default: 0.0.0.0)
  - `--port <port>` - Set the port (default: 8000)
  - `--name <name>` - Set container name (default: semker-backend)
  - `--detach` - Run in detached mode

### 🚀 Development Scripts

- **`start_server.sh`** - Start the development server using uvicorn
  ```bash
  ./scripts/start_server.sh
  ```

- **`start-with-aspire.sh`** - Start the server with .NET Aspire Dashboard telemetry integration
  ```bash
  ./scripts/start-with-aspire.sh
  ```

### 🧪 Testing Scripts

- **`run_bdd_tests.sh`** - Run BDD (Behavior Driven Development) tests using behave
  ```bash
  ./scripts/run_bdd_tests.sh
  ```

### 🔒 Type Safety Scripts

- **`check-types.sh`** - Run strict type checking using mypy
  ```bash
  ./scripts/check-types.sh
  ```

## Usage

All scripts are executable and should be run from the backend root directory:

```bash
cd /path/to/semker/src/backend
./scripts/<script-name>.sh
```

## Script Organization

- All scripts are organized in this `scripts/` directory for better project structure
- Scripts have executable permissions (`chmod +x`)
- Each script includes appropriate error handling and user feedback
- Scripts use environment variables for configuration when applicable
