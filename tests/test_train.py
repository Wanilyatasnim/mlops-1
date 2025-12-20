"""
Unit tests for the training script.
"""

import pytest
import os
import pickle
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error

# Import the training function
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'training'))
from train import train_model


def test_train_model_creates_artifact():
    """Test that training creates the model artifact file."""
    # Remove existing model if it exists
    model_path = "artifacts/model.pkl"
    if os.path.exists(model_path):
        os.remove(model_path)
    
    # Run training
    rmse = train_model()
    
    # Check that model file was created
    assert os.path.exists(model_path), "Model artifact should be created"
    
    # Check that RMSE is reasonable (should be less than 1.0 for this dataset)
    assert rmse < 1.0, f"RMSE should be reasonable, got {rmse}"
    assert rmse > 0, "RMSE should be positive"
    
    # Verify model can be loaded
    with open(model_path, "rb") as f:
        model_data = pickle.load(f)
    
    assert "model" in model_data, "Model data should contain 'model'"
    assert "scaler" in model_data, "Model data should contain 'scaler'"
    assert isinstance(model_data["model"], Ridge), "Model should be a Ridge regressor"
    assert isinstance(model_data["scaler"], StandardScaler), "Scaler should be StandardScaler"


def test_model_prediction():
    """Test that the trained model can make predictions."""
    # Ensure model exists
    model_path = "artifacts/model.pkl"
    if not os.path.exists(model_path):
        train_model()
    
    # Load model
    with open(model_path, "rb") as f:
        model_data = pickle.load(f)
    
    model = model_data["model"]
    scaler = model_data["scaler"]
    
    # Get sample data
    data = fetch_california_housing()
    X, y = data.data, data.target
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Make prediction
    X_test_scaled = scaler.transform(X_test)
    predictions = model.predict(X_test_scaled)
    
    # Check predictions are reasonable
    assert len(predictions) == len(y_test), "Should have same number of predictions as test samples"
    # Most predictions should be positive (house prices), allow some edge cases
    positive_count = np.sum(predictions > 0)
    assert positive_count > len(predictions) * 0.95, f"At least 95% of predictions should be positive, got {positive_count}/{len(predictions)}"
    # Predictions should be in reasonable range
    assert np.max(predictions) < 15, "Max prediction should be reasonable"
    assert np.min(predictions) > -2, "Min prediction should not be extremely negative"


def test_model_rmse_threshold():
    """Test that model RMSE meets a quality threshold."""
    rmse = train_model()
    
    # RMSE should be below 1.0 for a good model on this dataset
    assert rmse < 1.0, f"Model RMSE {rmse:.4f} should be below 1.0"

