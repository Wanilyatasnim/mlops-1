# Microservices Architecture

## Overview

This project implements an **End-to-End CI/CD Platform for Microservices** with the following architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway (8080)                      │
│              Routes requests to microservices                 │
└──────────────┬──────────────────────────────┬───────────────┘
               │                                │
       ┌───────▼────────┐            ┌─────────▼──────────┐
       │  ML Service    │            │   User Service     │
       │    (8081)      │            │     (8082)         │
       │                │            │                    │
       │ - Predictions  │            │ - Registration     │
       │ - Model API    │            │ - Authentication   │
       │ - Metrics      │            │ - User Management │
       └────────────────┘            └────────────────────┘
               │                                │
               └────────────┬───────────────────┘
                            │
                   ┌─────────▼──────────┐
                   │    Prometheus      │
                   │      (9090)        │
                   │  Metrics Storage   │
                   └─────────┬──────────┘
                             │
                   ┌─────────▼──────────┐
                   │     Grafana        │
                   │      (3000)        │
                   │  Visualization     │
                   └────────────────────┘
```

## Services

### 1. API Gateway (`services/api-gateway/`)

**Purpose**: Single entry point for all client requests, routes to appropriate microservices.

**Port**: 8080

**Endpoints**:
- `GET /` - Service information
- `GET /health` - Health check (checks all services)
- `POST /api/ml/predict` - Forward to ML service
- `GET /api/ml/health` - ML service health
- `POST /api/users/register` - Forward to user service
- `POST /api/users/login` - Forward to user service
- `GET /api/users` - Forward to user service
- `GET /api/users/health` - User service health
- `GET /metrics` - Prometheus metrics

**Features**:
- Request routing and forwarding
- CORS support
- Health aggregation
- Metrics collection
- Error handling and timeout management

### 2. ML Service (`services/ml-service/`)

**Purpose**: Machine learning inference service for housing price predictions.

**Port**: 8081

**Endpoints**:
- `GET /` - Service information
- `GET /health` - Health check
- `POST /predict` - Make prediction (8 features required)
- `GET /metrics` - Prometheus metrics

**Features**:
- Model loading (local or GCS)
- Feature scaling
- Prediction with error handling
- Performance metrics
- Structured logging

**Model**: Ridge Regression on California Housing dataset

### 3. User Service (`services/user-service/`)

**Purpose**: User management and authentication service.

**Port**: 8082

**Endpoints**:
- `GET /` - Service information
- `GET /health` - Health check
- `POST /users/register` - Register new user
- `POST /users/login` - Authenticate user (returns token)
- `GET /users` - List users (requires authentication)
- `GET /metrics` - Prometheus metrics

**Features**:
- User registration
- Password hashing (SHA256 - demo only)
- Token-based authentication
- User listing
- In-memory storage (replace with database in production)

## Technology Stack

### Services
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **httpx** - HTTP client (API Gateway)

### Monitoring
- **Prometheus** - Metrics collection and storage
- **Grafana** - Metrics visualization
- **prometheus-client** - Python metrics library

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Local orchestration
- **GitHub Actions** - CI/CD automation
- **Terraform** - Infrastructure as Code
- **GCP Cloud Run** - Serverless deployment

## Service Communication

### Local (Docker Compose)
- Services communicate via Docker network
- Service names resolve to container IPs
- Example: `http://ml-service:8081`

### Cloud (Cloud Run)
- Services communicate via HTTPS URLs
- URLs provided via environment variables
- Example: `https://ml-service-PROJECT-REGION.a.run.app`

## Data Flow

### Prediction Request Flow
```
Client → API Gateway → ML Service → Model → Response → Client
```

### User Registration Flow
```
Client → API Gateway → User Service → Store User → Response → Client
```

### Metrics Flow
```
All Services → Prometheus → Grafana → Dashboards
```

## Environment Variables

### API Gateway
```bash
ML_SERVICE_URL=http://ml-service:8081  # or Cloud Run URL
USER_SERVICE_URL=http://user-service:8082  # or Cloud Run URL
LOG_LEVEL=INFO
```

### ML Service
```bash
MODEL_PATH=/app/artifacts/model.pkl
MODEL_GCS_PATH=gs://bucket/models/model.pkl  # Optional
LOG_LEVEL=INFO
```

### User Service
```bash
LOG_LEVEL=INFO
```

## Deployment

### Local Development
```bash
docker-compose up --build
```

### Cloud Deployment
- **GitHub Actions**: Automated on push to main
- **Terraform**: Infrastructure as Code
- **Manual**: gcloud CLI commands

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## Monitoring

All services expose Prometheus metrics at `/metrics`:

- `http_requests_total{method, endpoint, status}` - Request counter
- `http_request_duration_seconds{method, endpoint}` - Latency histogram
- Service-specific metrics (e.g., `predictions_total`)

## Testing

### Manual Testing
```bash
# Register user
curl -X POST http://localhost:8080/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "email": "test@example.com", "password": "pass123"}'

# Login
curl -X POST http://localhost:8080/api/users/login \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "pass123"}'

# Make prediction
curl -X POST http://localhost:8080/api/ml/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [8.3252, 41.0, 6.984127, 1.023810, 322.0, 2.555556, 37.88, -122.23]}'
```

## Future Enhancements

1. **Service Mesh**: Add Istio or Linkerd for advanced traffic management
2. **Message Queue**: Add RabbitMQ/Kafka for async communication
3. **Database**: Replace in-memory storage with PostgreSQL/MongoDB
4. **Caching**: Add Redis for session management
5. **API Gateway**: Consider Kong or AWS API Gateway
6. **Authentication**: Implement proper JWT with refresh tokens
7. **Rate Limiting**: Add rate limiting per service
8. **Distributed Tracing**: Add OpenTelemetry/Jaeger
9. **Circuit Breaker**: Implement resilience patterns
10. **Kubernetes**: Deploy to GKE for advanced orchestration

