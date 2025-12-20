# 🚀 End-to-End CI/CD Platform for Microservices

**A production-ready MLOps platform demonstrating microservices architecture, automated CI/CD, cloud deployment, and infrastructure as code.**

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Services](#-services)
- [Deployment](#-deployment)
- [Documentation](#-documentation)

---

## 🎯 Overview

This project is a complete **End-to-End CI/CD Platform for Microservices** that demonstrates:

- ✅ **4 Microservices** (API Gateway, ML Service, User Service, Notification Service)
- ✅ **Automated CI/CD** with GitHub Actions
- ✅ **Multi-Cloud Deployment** (GCP Cloud Run, AWS ECS, GCP VMs)
- ✅ **Infrastructure as Code** with Terraform
- ✅ **Containerization** with Docker
- ✅ **Monitoring** with Prometheus + Grafana
- ✅ **Structured Logging** across all services

---

## 🏗️ Architecture

```
                    ┌─────────────────┐
                    │  API Gateway    │
                    │    (8080)       │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼────────┐  ┌───────▼────────┐  ┌───────▼──────────┐
│  ML Service    │  │  User Service  │  │ Notification Svc  │
│    (8081)      │  │    (8082)     │  │     (8083)         │
└────────────────┘  └────────────────┘  └───────────────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                    ┌────────▼────────┐
                    │   Prometheus    │
                    │     (9090)      │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │    Grafana      │
                    │     (3000)      │
                    └─────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Docker & Docker Compose
- (Optional) GCP/AWS accounts for cloud deployment

### Local Development

1. **Train the model**:
   ```bash
   pip install -r requirements.txt
   python training/train.py
   ```

2. **Start all services**:
   ```bash
   docker-compose up --build
   ```

3. **Access services**:
   - API Gateway: http://localhost:8080
   - ML Service: http://localhost:8081
   - User Service: http://localhost:8082
   - Notification Service: http://localhost:8083
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3000 (admin/admin)

### Test the API

```bash
# Register a user
curl -X POST http://localhost:8080/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "email": "test@example.com", "password": "password123"}'

# Make a prediction
curl -X POST http://localhost:8080/api/ml/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [8.3252, 41.0, 6.984127, 1.023810, 322.0, 2.555556, 37.88, -122.23]}'
```

---

## 📁 Project Structure

```
mlops/
├── services/              # Microservices
│   ├── api-gateway/
│   ├── ml-service/
│   ├── user-service/
│   └── notification-service/
├── training/             # ML training scripts
├── terraform/            # Infrastructure as Code
│   ├── main.tf          # GCP Cloud Run
│   ├── aws/             # AWS ECS
│   └── vm/              # GCP VMs
├── tests/               # Test files
├── docs/                # Documentation
└── artifacts/           # Model artifacts
```

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed structure.

---

## 🔧 Services

### API Gateway (Port 8080)
Routes requests to microservices. Entry point for all client requests.

### ML Service (Port 8081)
Machine learning inference service for housing price predictions.

### User Service (Port 8082)
User management and authentication service.

### Notification Service (Port 8083)
Email, SMS, and push notification service.

---

## 🚢 Deployment

### Automated (GitHub Actions)

1. **Set GitHub Secrets**:
   - `DOCKER_USERNAME` - Docker Hub username
   - `DOCKER_PASSWORD` - Docker Hub password
   - `GCP_PROJECT_ID` - GCP project ID
   - `GCP_SA_KEY` - GCP service account JSON key

2. **Push to main branch**:
   ```bash
   git push origin main
   ```

3. **Monitor deployment** in GitHub Actions tab

### Manual Deployment

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed deployment instructions:
- GCP Cloud Run
- AWS ECS
- GCP VMs
- Terraform

---

## 📚 Documentation

- [DEPLOYMENT.md](docs/DEPLOYMENT.md) - Detailed deployment guide
- [MICROSERVICES_ARCHITECTURE.md](docs/MICROSERVICES_ARCHITECTURE.md) - Architecture overview
- [COMPLETE_STATUS.md](docs/COMPLETE_STATUS.md) - Implementation status
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Project structure

---

## 🛠️ Tech Stack

- **FastAPI** - Web framework
- **Docker** - Containerization
- **GitHub Actions** - CI/CD
- **Terraform** - Infrastructure as Code
- **Prometheus + Grafana** - Monitoring
- **GCP Cloud Run / AWS ECS** - Cloud deployment

---

## 📝 License

This project is provided as-is for educational and demonstration purposes.

---

**Built with ❤️ for MLOps and DevOps best practices**
