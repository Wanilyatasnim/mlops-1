# 🚀 MLOps MVP: California Housing Price Prediction

**An end-to-end MLOps pipeline demonstrating production-ready machine learning deployment with automated training, containerization, monitoring, and CI/CD.**

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Running Locally](#-running-locally)
- [Docker Deployment](#-docker-deployment)
- [Testing](#-testing)
- [Monitoring & Observability](#-monitoring--observability)
- [CI/CD Pipeline](#-cicd-pipeline)
- [API Documentation](#-api-documentation)
- [Model Storage](#-model-storage)
- [Logging](#-logging)
- [Future Work](#-future-work)
- [Contributing](#-contributing)

---

## 🎯 Overview

This project is a complete **MLOps MVP** that demonstrates best practices for deploying machine learning models in production. It includes:

- **Automated model training** using scikit-learn on the California Housing dataset
- **RESTful API** built with FastAPI for real-time predictions
- **Production monitoring** with Prometheus metrics and Grafana dashboards
- **Containerization** with Docker for consistent deployments
- **CI/CD automation** with GitHub Actions
- **Comprehensive logging** for observability
- **Test suite** for quality assurance

---

## ✨ Features

- ✅ **Automated Training Pipeline**: Train Ridge regression models with reproducible results
- ✅ **RESTful API**: FastAPI-based inference service with OpenAPI documentation
- ✅ **Real-time Monitoring**: Prometheus metrics for request tracking, latency, and errors
- ✅ **Containerization**: Docker-based deployment for consistency across environments
- ✅ **CI/CD Integration**: Automated testing, training, and deployment via GitHub Actions
- ✅ **Comprehensive Logging**: Structured logging for debugging and observability
- ✅ **Health Checks**: Built-in health monitoring endpoints
- ✅ **Model Versioning**: Support for local and cloud storage (GCS) model artifacts
- ✅ **Test Coverage**: Unit and integration tests for training and API endpoints
- ✅ **Production-Ready**: Error handling, validation, and performance monitoring

---

## 🛠️ Tech Stack

### Machine Learning
- **scikit-learn** (≥1.4.0) - Model training and evaluation
- **numpy** (≥1.26.0) - Numerical computations

### Web Framework & API
- **FastAPI** (≥0.104.1) - Modern, fast web framework
- **uvicorn** (≥0.24.0) - ASGI server
- **pydantic** (≥2.5.0) - Data validation

### Monitoring & Observability
- **prometheus-client** (≥0.19.0) - Metrics collection
- **Prometheus** - Time-series database for metrics
- **Grafana** - Visualization and dashboards

### Testing
- **pytest** (≥7.4.0) - Testing framework
- **pytest-cov** (≥4.1.0) - Code coverage
- **httpx** (≥0.24.0) - HTTP client for testing

### DevOps
- **Docker** - Containerization
- **GitHub Actions** - CI/CD automation
- **Python 3.10+** - Runtime environment

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    GitHub Repository                             │
│              (Source Code + Model Artifacts)                     │
└─────────────────────────────────────────────────────────────────┘
                            │
                            │ Push to main branch
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              GitHub Actions CI/CD Pipeline                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │   Install    │→ │     Run      │→ │    Train     │        │
│  │ Dependencies │  │    Tests     │  │    Model     │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│                            │                                    │
│                            ▼                                    │
│                  ┌──────────────┐                               │
│                  │    Build     │                               │
│                  │   Docker     │                               │
│                  │    Image     │                               │
│                  └──────────────┘                               │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              Production Environment (Local/Cloud)              │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         FastAPI Inference Service (Port 8080)            │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │  │
│  │  │   /predict   │  │   /metrics   │  │  /health     │ │  │
│  │  │   /docs      │  │              │  │              │ │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘ │  │
│  │                                                          │  │
│  │  ┌────────────────────────────────────────────────────┐ │  │
│  │  │         Prometheus Metrics Collection              │ │  │
│  │  │  • http_requests_total                            │ │  │
│  │  │  • http_request_duration_seconds                    │ │  │
│  │  │  • predictions_total                               │ │  │
│  │  │  • prediction_errors_total                          │ │  │
│  │  └────────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                    │
│                            │ Metrics Scraping                   │
│                            ▼                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         Prometheus + Grafana Stack                       │  │
│  │  ┌──────────────┐          ┌──────────────┐            │  │
│  │  │ Prometheus   │◄─────────┤   Grafana    │            │  │
│  │  │ (Port 9090)  │          │ (Port 3000)   │            │  │
│  │  └──────────────┘          └──────────────┘            │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
mlops-1/
│
├── src/
│   ├── train.py              # Model training script
│   └── app/
│       ├── __init__.py
│       ├── main.py           # FastAPI application
│       ├── metrics.py        # Prometheus metrics
│       └── logger.py         # Logging configuration
│
├── tests/
│   ├── __init__.py
│   ├── test_train.py         # Training script tests
│   └── test_api.py           # API endpoint tests
│
├── artifacts/                # Generated after training
│   └── model.pkl            # Trained model artifact
│
├── .github/
│   └── workflows/
│       └── ci.yml            # CI/CD workflow
│
├── Dockerfile                # Docker container definition
├── docker-compose.yml        # Prometheus + Grafana setup
├── prometheus.yml            # Prometheus configuration
├── pytest.ini                # Pytest configuration
├── requirements.txt         # Python dependencies
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **pip** (Python package manager)
- **Docker** (for containerization)
- **Docker Compose** (for monitoring stack)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Wanilyatasnim/mlops-1.git
   cd mlops-1
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Running Locally

### Step 1: Train the Model

```bash
python src/train.py
```

This will:
- Download the California Housing dataset (20,640 samples)
- Split data into train/test sets (80/20)
- Train a Ridge regression model
- Evaluate and save model to `artifacts/model.pkl`
- Display RMSE score

**Expected Output:**
```
2025-12-06 14:31:35 - __main__ - INFO - Starting model training pipeline
2025-12-06 14:31:35 - __main__ - INFO - Dataset loaded: 20640 samples, 8 features
2025-12-06 14:31:35 - __main__ - INFO - Model RMSE: 0.7456
2025-12-06 14:31:35 - __main__ - INFO - Training pipeline completed successfully
```

### Step 2: Start the API Server

```bash
uvicorn src.app.main:app --reload --port 8080
```

The API will be available at:
- **API**: http://localhost:8080
- **Swagger UI**: http://localhost:8080/docs
- **Health Check**: http://localhost:8080/health
- **Metrics**: http://localhost:8080/metrics

### Step 3: Test the API

**Health Check:**
```bash
curl http://localhost:8080/health
```

**Make a Prediction:**
```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [8.3252, 41.0, 6.984127, 1.023810, 322.0, 2.555556, 37.88, -122.23]}'
```

**View Metrics:**
```bash
curl http://localhost:8080/metrics
```

---

## 🐳 Docker Deployment

### Build the Docker Image

```bash
docker build -t mlops-api:latest .
```

### Run the Container

```bash
docker run -d -p 8080:8080 --name mlops-api mlops-api:latest
```

### Verify Container

```bash
# Check container status
docker ps

# View logs
docker logs mlops-api

# Test the API
curl http://localhost:8080/health
```

### Stop Container

```bash
docker stop mlops-api
docker rm mlops-api
```

---

## 🧪 Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test Suites

```bash
# Training tests only
pytest tests/test_train.py -v

# API tests only
pytest tests/test_api.py -v
```

### Test Coverage

```bash
pytest tests/ --cov=src --cov-report=html
```

### Test Results

The test suite includes:
- ✅ Model training and artifact creation
- ✅ Model prediction functionality
- ✅ API endpoint validation
- ✅ Error handling
- ✅ Metrics collection

**Expected Output:**
```
============================= test session starts =============================
tests/test_api.py::test_root_endpoint PASSED
tests/test_api.py::test_health_endpoint PASSED
tests/test_api.py::test_predict_endpoint_valid PASSED
tests/test_train.py::test_train_model_creates_artifact PASSED
...
======================= 10 passed in 3.61s =======================
```

---

## 📊 Monitoring & Observability

### Prometheus + Grafana Setup

1. **Start Monitoring Stack**
   ```bash
   docker-compose up -d
   ```

2. **Access Services**
   - **Grafana**: http://localhost:3000 (admin/admin)
   - **Prometheus**: http://localhost:9090

3. **Configure Grafana**
   - Go to **Configuration → Data Sources**
   - Add **Prometheus** data source
   - URL: `http://prometheus:9090`
   - Click **Save & Test**

4. **Create Dashboards**
   
   **Key Metrics to Monitor:**
   - `http_requests_total{endpoint="/predict"}` - Request count
   - `http_request_duration_seconds{endpoint="/predict"}` - Latency
   - `predictions_total` - Total predictions
   - `prediction_errors_total` - Error count

   **Sample Queries:**
   ```promql
   # Request rate
   rate(http_requests_total[5m])
   
   # Average latency
   rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])
   
   # Error rate
   rate(prediction_errors_total[5m])
   ```

5. **Stop Monitoring Stack**
   ```bash
   docker-compose down
   ```

### Available Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `http_requests_total` | Counter | Total HTTP requests by method, endpoint, status |
| `http_request_duration_seconds` | Histogram | Request latency distribution |
| `predictions_total` | Counter | Total successful predictions |
| `prediction_errors_total` | Counter | Total prediction errors |

---

## 🔄 CI/CD Pipeline

### Workflow Overview

The GitHub Actions workflow (`.github/workflows/ci.yml`) automates the entire pipeline:

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Checkout  │ →  │   Install   │ →  │    Run      │ →  │    Train    │
│     Code    │    │ Dependencies│    │    Tests    │    │    Model    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                                                    │
                                                                    ▼
                                                          ┌─────────────┐
                                                          │    Build    │
                                                          │   Docker    │
                                                          │   Image     │
                                                          └─────────────┘
```

### Pipeline Steps

1. **Checkout Code**: Retrieves latest code from repository
2. **Setup Python**: Configures Python 3.10 environment
3. **Install Dependencies**: Installs all required packages
4. **Run Tests**: Executes pytest test suite
5. **Train Model**: Runs training script to generate `artifacts/model.pkl`
6. **Build Docker Image**: Creates containerized image

### Workflow Triggers

- **Automatic**: Runs on every push to `main` branch
- **Manual**: Can be triggered manually from GitHub Actions tab

### Optional: Cloud Storage Integration

To enable model upload to Google Cloud Storage, uncomment the GCS steps in `.github/workflows/ci.yml` and configure:

- `GCS_BUCKET_NAME`: Your GCS bucket name
- `GCP_SA_KEY`: Service account JSON key

---

## 📡 API Documentation

### Base URL
```
http://localhost:8080
```

### Endpoints

#### `GET /`
Root endpoint with API information.

**Response:**
```json
{
  "message": "California Housing Price Prediction API",
  "endpoints": {
    "predict": "/predict",
    "metrics": "/metrics",
    "health": "/health"
  }
}
```

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

#### `POST /predict`
Make a price prediction.

**Request:**
```json
{
  "features": [8.3252, 41.0, 6.984127, 1.023810, 322.0, 2.555556, 37.88, -122.23]
}
```

**Response:**
```json
{
  "prediction": 4.1518
}
```

**Feature Description (8 features required):**
1. **MedInc**: Median income in block group
2. **HouseAge**: Median house age in block group
3. **AveRooms**: Average number of rooms per household
4. **AveBedrms**: Average number of bedrooms per household
5. **Population**: Block group population
6. **AveOccup**: Average number of household members
7. **Latitude**: Block group latitude
8. **Longitude**: Block group longitude

#### `GET /metrics`
Prometheus metrics endpoint (text format).

#### `GET /docs`
Interactive API documentation (Swagger UI).

---

## 📦 Model Storage

### Current Setup (Local/Demo)
- Model stored in `artifacts/model.pkl`
- Committed to repository (suitable for small models)
- Automatically included in Docker image

### Production Setup (Cloud Storage)

**Option 1: Google Cloud Storage (GCS)**

1. Set up GCS bucket and configure GitHub secrets
2. Uncomment GCS upload steps in `.github/workflows/ci.yml`
3. Set environment variable:
   ```bash
   export MODEL_GCS_PATH=gs://your-bucket/models/model-latest.pkl
   ```

**Option 2: AWS S3**

Similar approach using `boto3` and S3 bucket.

The FastAPI app automatically:
- Tries to load from cloud storage if `MODEL_GCS_PATH` is set
- Falls back to local `artifacts/model.pkl` if cloud storage is unavailable

---

## 📝 Logging

### Log Levels

- **DEBUG**: Detailed debugging information
- **INFO**: Normal operations (default)
- **WARNING**: Slow predictions, health issues
- **ERROR**: Errors with stack traces

### Configure Logging

Set the `LOG_LEVEL` environment variable:

```bash
export LOG_LEVEL=DEBUG   # Detailed debugging
export LOG_LEVEL=INFO    # Default, production-ready
export LOG_LEVEL=WARNING # Only warnings and errors
```

### What's Logged

**Training Script:**
- Dataset loading progress and timing
- Training pipeline steps
- Model evaluation metrics (RMSE)
- Model saving operations

**API Service:**
- Model loading (startup) with timing
- Prediction requests with feature counts
- Prediction results and latency
- Slow prediction warnings (>0.5s, >1.0s thresholds)
- Error details with full stack traces

### Example Log Output

```
2025-12-06 14:31:35 - app.main - INFO - Starting model loading process...
2025-12-06 14:31:35 - app.main - INFO - Model loaded successfully in 0.023s
2025-12-06 14:31:40 - app.main - INFO - Received prediction request with 8 features
2025-12-06 14:31:40 - app.main - INFO - Prediction successful: 4.1518 (latency: 0.001s)
2025-12-06 14:31:45 - app.main - WARNING - Prediction latency above average: 0.652s
```

---

## 🔮 Future Work

### Short-term Enhancements
- [ ] **Scheduled Retraining**: Weekly/monthly automated model retraining
- [ ] **Model Versioning**: Track model versions and performance over time
- [ ] **A/B Testing**: Compare model versions in production
- [ ] **Data Validation**: Input data quality checks and validation
- [ ] **Feature Store**: Centralized feature management

### Medium-term Improvements
- [ ] **Model Registry**: MLflow or similar for model tracking
- [ ] **Experiment Tracking**: Track hyperparameters and metrics
- [ ] **Automated Alerts**: Grafana alerts for anomalies
- [ ] **Load Testing**: Performance testing with locust/k6
- [ ] **API Rate Limiting**: Protect against abuse

### Long-term Vision
- [ ] **Multi-model Support**: Serve multiple models from same API
- [ ] **Batch Predictions**: Support for bulk prediction requests
- [ ] **Model Explainability**: SHAP/LIME integration
- [ ] **Data Drift Detection**: Monitor input distribution changes
- [ ] **Auto-scaling**: Kubernetes deployment with auto-scaling
- [ ] **Multi-cloud Support**: Deploy to AWS, Azure, GCP

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Run tests** (`pytest tests/ -v`)
5. **Commit your changes** (`git commit -m 'Add amazing feature'`)
6. **Push to the branch** (`git push origin feature/amazing-feature`)
7. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guide
- Write tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

---

## 📄 License

This project is provided as-is for educational and demonstration purposes.

---

## 🙏 Acknowledgments

- **scikit-learn** for the machine learning framework
- **FastAPI** for the modern web framework
- **Prometheus & Grafana** for monitoring capabilities
- **California Housing Dataset** from scikit-learn

---

## 📞 Support

For issues, questions, or contributions, please open an issue on [GitHub](https://github.com/Wanilyatasnim/mlops-1/issues).

---

**Built with ❤️ for MLOps education and best practices**
