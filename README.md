# MLOps MVP: California Housing Price Prediction

An end-to-end MLOps pipeline for training and serving a machine learning model using scikit-learn, FastAPI, Prometheus monitoring, Docker containerization, and automated CI/CD with GitHub Actions.

## 📋 Project Overview

This project demonstrates a complete MLOps workflow:

1. **Model Training**: Ridge regression model trained on California Housing dataset
2. **Inference API**: FastAPI service for real-time predictions
3. **Monitoring**: Prometheus metrics for request tracking and performance monitoring
4. **Containerization**: Docker-based deployment
5. **CI/CD**: Automated training, building, and deployment to Google Cloud Run

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Repository                        │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ Push to main
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  GitHub Actions CI/CD                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Install    │→ │    Train     │→ │  Build &     │     │
│  │ Dependencies │  │    Model     │  │   Deploy     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Google Cloud Run (Production)                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │            FastAPI Inference Service                │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │    │
│  │  │   /predict   │  │   /metrics   │  │  /health │ │    │
│  │  └──────────────┘  └──────────────┘  └──────────┘ │    │
│  │                                                    │    │
│  │  ┌──────────────────────────────────────────────┐ │    │
│  │  │      Prometheus Metrics Collection            │ │    │
│  │  │  - Request count                              │ │    │
│  │  │  - Request latency                            │ │    │
│  │  │  - Prediction errors                          │ │    │
│  │  └──────────────────────────────────────────────┘ │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
project/
│── src/
│     ├── train.py              # Model training script
│     ├── app/
│     │      ├── main.py        # FastAPI application
│     │      ├── metrics.py     # Prometheus metrics
│     │      └── __init__.py
│
│── artifacts/                   # Generated after training
│     └── model.pkl             # Trained model artifact
│
│── Dockerfile                   # Docker container definition
│── requirements.txt            # Python dependencies
│── .github/
│       └── workflows/
│             └── ci.yml        # CI/CD workflow
│── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- pip
- Docker (for containerization)
- Google Cloud SDK (for deployment)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mlops
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Train the model**
   ```bash
   python src/train.py
   ```
   This will:
   - Download the California Housing dataset
   - Train a Ridge regression model
   - Save the model to `artifacts/model.pkl`
   - Print the RMSE score

4. **Run the FastAPI service locally**
   ```bash
   uvicorn src.app.main:app --reload --port 8080
   ```

5. **Test the API**
   
   Health check:
   ```bash
   curl http://localhost:8080/health
   ```
   
   Make a prediction:
   ```bash
   curl -X POST http://localhost:8080/predict \
     -H "Content-Type: application/json" \
     -d '{"features": [8.3252, 41.0, 6.984127, 1.023810, 322.0, 2.555556, 37.88, -122.23]}'
   ```
   
   View metrics:
   ```bash
   curl http://localhost:8080/metrics
   ```

### Docker Build and Run

1. **Build the Docker image**
   ```bash
   docker build -t mlops-api:latest .
   ```

2. **Run the container**
   ```bash
   docker run -p 8080:8080 mlops-api:latest
   ```

3. **Test the containerized service**
   ```bash
   curl http://localhost:8080/health
   ```

## 🔄 CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) automates:

1. **Code Checkout**: Retrieves the latest code
2. **Python Setup**: Configures Python 3.10 environment
3. **Dependency Installation**: Installs all required packages
4. **Model Training**: Runs the training script to generate `artifacts/model.pkl`
5. **Docker Build**: Creates a containerized image
6. **Cloud Deployment**: Pushes to Google Container Registry and deploys to Cloud Run

### Required GitHub Secrets

Configure these secrets in your GitHub repository settings:

- `GCP_SA_KEY`: Google Cloud Service Account JSON key
- `GCP_PROJECT_ID`: Your GCP project ID
- `GCP_REGION`: Deployment region (e.g., `us-central1`)

### Workflow Triggers

The pipeline automatically runs on:
- Push to `main` branch

## 📊 API Endpoints

### `GET /`
Root endpoint with API information.

### `GET /health`
Health check endpoint. Returns service status and model loading state.

### `POST /predict`
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
  "prediction": 4.526
}
```

**Feature Description (8 features required):**
1. MedInc: Median income in block group
2. HouseAge: Median house age in block group
3. AveRooms: Average number of rooms per household
4. AveBedrms: Average number of bedrooms per household
5. Population: Block group population
6. AveOccup: Average number of household members
7. Latitude: Block group latitude
8. Longitude: Block group longitude

### `GET /metrics`
Prometheus metrics endpoint. Returns:
- `http_requests_total`: Total HTTP requests by method, endpoint, and status
- `http_request_duration_seconds`: Request latency histogram
- `predictions_total`: Total number of predictions made
- `prediction_errors_total`: Total number of prediction errors

## 🐳 Docker Details

The Dockerfile:
- Uses `python:3.10-slim` base image
- Installs dependencies from `requirements.txt`
- Copies source code and model artifacts
- Exposes port 8080
- Runs FastAPI with uvicorn

## 📦 Dependencies

- **scikit-learn**: Machine learning library for model training
- **numpy**: Numerical computing
- **fastapi**: Modern web framework for API
- **uvicorn**: ASGI server
- **pydantic**: Data validation
- **prometheus-client**: Metrics collection

## 🔍 Monitoring

The service exposes Prometheus metrics at `/metrics` endpoint:

- **Request Metrics**: Track all HTTP requests with method, endpoint, and status code
- **Latency Metrics**: Monitor request processing time
- **Prediction Metrics**: Count successful predictions and errors

You can scrape these metrics with Prometheus or any compatible monitoring tool.

## 📝 Notes

- The model artifact (`artifacts/model.pkl`) must be generated before running the API
- The training script automatically creates the `artifacts/` directory
- For production deployment, ensure the model artifact is included in the Docker image
- The CI/CD pipeline runs training on every push, ensuring the model is always up-to-date

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is provided as-is for educational and demonstration purposes.

