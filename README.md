# Backend Service

[![Code Scanning](https://github.com/team-xx-capstone-deploycamp/backend-service/actions/workflows/code-scanning.yml/badge.svg)](https://github.com/team-xx/backend-service/actions/workflows/code-scanning.yml)
[![Deployment](https://github.com/team-xx-capstone-deploycamp/backend-service/actions/workflows/deployment.yml/badge.svg)](https://github.com/team-xx/backend-service/actions/workflows/deployment.yml)

A simple FastAPI backend service that provides REST API endpoints.

## Features

- Root endpoint that returns a greeting message
- Hello endpoint that greets a specific user

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)

### Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/team-xx/backend-service.git
   cd backend-service
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

Start the application with uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at http://127.0.0.1:8000

### API Endpoints

- `GET /`: Returns a greeting message
- `GET /hello/{name}`: Returns a personalized greeting for the specified name

### Docker

You can also run the application using Docker:

```bash
# Build the Docker image
docker build -t backend-service .

# Run the container
docker run -p 8000:8000 backend-service
```

## Development

### Testing

You can test the API endpoints using the provided `test_app.http` file with tools like REST Client for VS Code.

To run the automated test suite, execute:

```bash
pytest
```

## CI/CD

This project uses GitHub Actions for:
- Code scanning to identify security vulnerabilities
- Automated deployment
