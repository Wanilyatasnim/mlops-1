# Deployment Guide

This guide covers deploying the microservices architecture to various environments.

## Architecture Overview

The project consists of 3 microservices:

1. **API Gateway** (Port 8080) - Routes requests to other services
2. **ML Service** (Port 8081) - Machine learning predictions
3. **User Service** (Port 8082) - User management and authentication

Plus monitoring:
- **Prometheus** (Port 9090) - Metrics collection
- **Grafana** (Port 3000) - Metrics visualization

## Local Development

### Prerequisites
- Docker and Docker Compose
- Python 3.10+ (for training)

### Steps

1. **Train the model**:
   ```bash
   cd 1
   pip install -r requirements.txt
   python src/train.py
   ```

2. **Start all services**:
   ```bash
   docker-compose up --build
   ```

3. **Access services**:
   - API Gateway: http://localhost:8080
   - ML Service: http://localhost:8081
   - User Service: http://localhost:8082
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3000 (admin/admin)

### Test the API

**Register a user**:
```bash
curl -X POST http://localhost:8080/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "password123"}'
```

**Login**:
```bash
curl -X POST http://localhost:8080/api/users/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'
```

**Make a prediction**:
```bash
curl -X POST http://localhost:8080/api/ml/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [8.3252, 41.0, 6.984127, 1.023810, 322.0, 2.555556, 37.88, -122.23]}'
```

## Cloud Deployment

### Option 1: GitHub Actions (Automated)

The CI/CD pipeline automatically:
1. Trains the model
2. Builds Docker images for all services
3. Pushes to Docker Hub or GCR
4. Deploys to GCP Cloud Run

**Setup**:

1. **Configure GitHub Secrets**:
   - `DOCKER_USERNAME` - Your Docker Hub username
   - `DOCKER_PASSWORD` - Your Docker Hub password (or access token)
   - `GCP_PROJECT_ID` - Your GCP project ID
   - `GCP_SA_KEY` - GCP service account JSON key (for Cloud Run deployment)

2. **Push to main branch**:
   ```bash
   git push origin main
   ```

3. **Monitor deployment**:
   - Check GitHub Actions tab for pipeline status
   - View service URLs in the deployment job output

### Option 2: Terraform (Infrastructure as Code)

**Prerequisites**:
- Terraform >= 1.0
- GCP account with billing enabled
- Docker images already pushed to registry

**Steps**:

1. **Configure Terraform**:
   ```bash
   cd terraform
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your values
   ```

2. **Authenticate with GCP**:
   ```bash
   gcloud auth application-default login
   ```

3. **Initialize and apply**:
   ```bash
   terraform init
   terraform plan
   terraform apply
   ```

4. **Get service URLs**:
   ```bash
   terraform output
   ```

### Option 3: Manual Cloud Run Deployment

**Deploy API Gateway**:
```bash
gcloud run deploy api-gateway \
  --image docker.io/YOUR_USERNAME/api-gateway:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "ML_SERVICE_URL=https://ml-service-...,USER_SERVICE_URL=https://user-service-..." \
  --port 8080
```

**Deploy ML Service**:
```bash
gcloud run deploy ml-service \
  --image docker.io/YOUR_USERNAME/ml-service:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "MODEL_PATH=/app/artifacts/model.pkl" \
  --port 8081
```

**Deploy User Service**:
```bash
gcloud run deploy user-service \
  --image docker.io/YOUR_USERNAME/user-service:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8082
```

## Docker Registry Setup

### Docker Hub

1. Create account at https://hub.docker.com
2. Login: `docker login`
3. Images will be pushed as: `docker.io/USERNAME/service-name:tag`

### Google Container Registry (GCR)

1. Enable Container Registry API
2. Configure authentication:
   ```bash
   gcloud auth configure-docker
   ```
3. Images will be pushed as: `gcr.io/PROJECT_ID/service-name:tag`

## Environment Variables

### API Gateway
- `ML_SERVICE_URL` - URL of ML service
- `USER_SERVICE_URL` - URL of User service
- `LOG_LEVEL` - Logging level (default: INFO)

### ML Service
- `MODEL_PATH` - Path to model artifact (default: /app/artifacts/model.pkl)
- `MODEL_GCS_PATH` - Optional GCS path (e.g., gs://bucket/models/model.pkl)
- `LOG_LEVEL` - Logging level (default: INFO)

### User Service
- `LOG_LEVEL` - Logging level (default: INFO)

## Monitoring

### Prometheus Metrics

All services expose metrics at `/metrics`:
- `http_requests_total` - Request count by method, endpoint, status
- `http_request_duration_seconds` - Request latency histogram

### Grafana Dashboards

1. Access Grafana at http://localhost:3000
2. Login with admin/admin
3. Add Prometheus data source: `http://prometheus:9090`
4. Create dashboards for:
   - Request rates
   - Latency percentiles
   - Error rates
   - Service health

## Troubleshooting

### Services not starting
- Check Docker logs: `docker-compose logs SERVICE_NAME`
- Verify ports are not in use
- Check environment variables

### ML Service model not found
- Ensure `artifacts/model.pkl` exists
- Run training script: `python src/train.py`
- Check MODEL_PATH environment variable

### Cloud Run deployment fails
- Verify Docker images are pushed to registry
- Check GCP service account permissions
- Review Cloud Run logs in GCP Console

### Service communication issues
- Verify service URLs in API Gateway environment variables
- Check network connectivity (Docker network or Cloud Run)
- Review service health endpoints

## Production Considerations

1. **Security**:
   - Remove public access (allUsers) from Cloud Run services
   - Use service-to-service authentication
   - Implement proper JWT validation in User Service
   - Use secrets management (GCP Secret Manager)

2. **Scalability**:
   - Configure auto-scaling limits
   - Use Cloud Load Balancer for high availability
   - Consider regional deployment

3. **Monitoring**:
   - Set up alerting in Grafana
   - Use Cloud Monitoring for Cloud Run
   - Implement distributed tracing

4. **Database**:
   - Replace in-memory storage with Cloud SQL or Firestore
   - Implement proper user data persistence

5. **CI/CD**:
   - Add staging environment
   - Implement blue-green deployments
   - Add automated testing in pipeline

