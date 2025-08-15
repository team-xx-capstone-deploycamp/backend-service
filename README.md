# Car Price Prediction API

[![CI](https://github.com/team-xx-capstone-deploycamp/backend-service/actions/workflows/ci.yml/badge.svg)](https://github.com/team-xx-capstone-deploycamp/backend-service/actions/workflows/ci.yml)
[![Deployment](https://github.com/team-xx-capstone-deploycamp/backend-service/actions/workflows/deployment.yml/badge.svg)](https://github.com/team-xx-capstone-deploycamp/backend-service/actions/workflows/deployment.yml)

A FastAPI-based machine learning service that predicts used car prices based on various features like make, model, engine size, horsepower, and mileage.

## Features

- Machine learning model for car price prediction
- RESTful API with JSON request/response format
- Basic authentication for secure access
- Health check endpoints
- Swagger UI documentation
- Docker support for both development and production
- CI/CD pipeline with GitHub Actions

## Installation

### Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose (recommended)
- Git

### Local Setup

#### Using Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/team-xx-capstone-deploycamp/backend-service.git
   cd backend-service
   ```

2. Create a `.env` file with the required environment variables:
   ```bash
   APP_APP_NAME="FastAPI ML API"
   APP_ALLOW_ORIGINS="http://localhost:3000"
   APP_BASIC_AUTH_USERNAME="admin"
   APP_BASIC_AUTH_PASSWORD="changeme"
   APP_MODEL_PATH="model/used_car_price_model_v2.pkl"
   ```

3. Start the development server using Docker Compose:
   ```bash
   docker compose --profile dev up
   ```

#### Without Docker

1. Clone the repository:
   ```bash
   git clone https://github.com/team-xx-capstone-deploycamp/backend-service.git
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

4. Create a `.env` file with the required environment variables (see above).

5. Start the application with uvicorn:
   ```bash
   uvicorn app.main:app --reload
   ```

## Usage

The API will be available at http://localhost:8000

### API Endpoints

- `GET /healthz`: Health check endpoint
- `GET /v1/ping`: Simple ping-pong response
- `GET /v1/versions`: Returns versions of key ML libraries
- `POST /v1/predict`: Predicts car price based on input features (requires authentication)
- `GET /docs`: Swagger UI documentation
- `GET /openapi.json`: OpenAPI specification

### Authentication

The prediction endpoint requires Basic Authentication. Default credentials are:
- Username: `admin`
- Password: `changeme`

These can be changed via environment variables.

### Example API Requests

#### Predict with partial record (recommended)

```bash
curl -X POST http://localhost:8000/v1/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic YWRtaW46Y2hhbmdlbWU=" \
  -d '{
    "record": {
      "CarName": "toyota corolla",
      "enginesize": 130,
      "horsepower": 100,
      "citympg": 28
    }
  }'
```

#### Predict with full feature list

```bash
curl -X POST http://localhost:8000/v1/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic YWRtaW46Y2hhbmdlbWU=" \
  -d '{
    "features": [0,0,"toyota corolla","gas","std","four","sedan","fwd","front",96.5,175.4,65.2,54.1,2330,"ohc","four",130,"mpfi",3.47,2.68,9.0,100,5500,28,34]
  }'
```

## Development

### Project Structure

```
backend-service/
├── .github/workflows/    # CI/CD workflows
├── app/                  # Application code
│   ├── api/              # API endpoints
│   ├── core/             # Core functionality
│   ├── deps/             # Dependencies
│   ├── schemas/          # Pydantic models
│   └── services/         # Business logic
├── model/                # ML model files
└── tests/                # Test suite
```

### Testing

You can test the API endpoints using the provided `test_app.http` file with tools like REST Client for VS Code.

To run the automated test suite, execute:

```bash
pytest
```

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment:

### CI Pipeline (`ci.yml`)

Triggered on pull requests to the `prod` branch:
1. **Code Quality**: Runs dependency scanning and Dockerfile linting
2. **Tests**: Runs the test suite with pytest and uploads coverage reports
3. **SonarCloud Analysis**: Performs code quality analysis

### Deployment Pipeline (`deployment.yml`)

Triggered on pushes to the `prod` branch:
1. **Build**: Builds and pushes the Docker image to GitHub Container Registry
2. **Security Scan**: Scans the Docker image for vulnerabilities using Trivy
3. **Deploy**: Deploys the application to the production server

## Production Deployment

The service is deployed using Docker Compose on a VPS. The deployment process:
1. Builds and pushes a Docker image to GitHub Container Registry
2. Transfers necessary files to the VPS
3. Updates the Docker Compose configuration with the new image
4. Restarts the service

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| APP_APP_NAME | Application name | FastAPI ML API |
| APP_ALLOW_ORIGINS | CORS allowed origins | http://localhost:3000 |
| APP_BASIC_AUTH_USERNAME | Basic auth username | admin |
| APP_BASIC_AUTH_PASSWORD | Basic auth password | changeme |
| APP_MODEL_PATH | Path to the ML model file | model/used_car_price_model_v2.pkl |
