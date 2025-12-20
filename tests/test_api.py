"""
Unit and integration tests for the FastAPI application.
"""

import pytest
from fastapi.testclient import TestClient
import os
import sys

# Ensure model exists before importing app
model_path = os.path.join(os.path.dirname(__file__), '..', 'artifacts', 'model.pkl')
if not os.path.exists(model_path):
    # Run training if model doesn't exist
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'training'))
    from train import train_model
    train_model()

# Add services to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'services', 'ml-service', 'src'))

# Import app and manually trigger startup to ensure model loads
from app.main import app, load_model
import asyncio

# Manually trigger startup event to load model
asyncio.run(load_model())

# Create test client
client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "endpoints" in data


def test_health_endpoint():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "model_loaded" in data


def test_predict_endpoint_valid():
    """Test prediction endpoint with valid input."""
    # Ensure model exists first
    import os
    model_path = os.path.join(os.path.dirname(__file__), '..', 'artifacts', 'model.pkl')
    if not os.path.exists(model_path):
        # Run training if model doesn't exist
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from src.train import train_model
        train_model()
    
    # Valid California Housing features
    valid_features = [8.3252, 41.0, 6.984127, 1.023810, 322.0, 2.555556, 37.88, -122.23]
    
    response = client.post(
        "/predict",
        json={"features": valid_features}
    )
    
    # If 500, check the error message
    if response.status_code != 200:
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    data = response.json()
    assert "prediction" in data
    assert isinstance(data["prediction"], (int, float))
    assert data["prediction"] > 0  # House prices should be positive


def test_predict_endpoint_invalid_length():
    """Test prediction endpoint with wrong number of features."""
    # Too few features
    response = client.post(
        "/predict",
        json={"features": [1.0, 2.0, 3.0]}
    )
    assert response.status_code == 422  # Validation error
    
    # Too many features
    response = client.post(
        "/predict",
        json={"features": [1.0] * 10}
    )
    assert response.status_code == 422  # Validation error


def test_predict_endpoint_invalid_type():
    """Test prediction endpoint with invalid data types."""
    # Non-numeric features
    response = client.post(
        "/predict",
        json={"features": ["invalid"] * 8}
    )
    assert response.status_code == 422  # Validation error


def test_metrics_endpoint():
    """Test the metrics endpoint."""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    
    # Check that metrics content is present
    content = response.text
    assert "http_requests_total" in content or "prometheus" in content.lower()


def test_metrics_after_prediction():
    """Test that metrics are updated after making predictions."""
    # Make a prediction
    valid_features = [8.3252, 41.0, 6.984127, 1.023810, 322.0, 2.555556, 37.88, -122.23]
    client.post("/predict", json={"features": valid_features})
    
    # Check metrics
    response = client.get("/metrics")
    assert response.status_code == 200
    content = response.text
    
    # Should have prediction metrics
    assert "predictions_total" in content or "http_requests_total" in content

