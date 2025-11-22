"""
Training script for California Housing dataset using Ridge Regression.
Saves the trained model to artifacts/model.pkl
"""

import pickle
import os
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
import numpy as np

def train_model():
    """Train Ridge regression model on California Housing dataset."""
    
    # Load dataset
    print("Loading California Housing dataset...")
    data = fetch_california_housing()
    X, y = data.data, data.target
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    print("Training Ridge regression model...")
    model = Ridge(alpha=1.0, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_scaled)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f"RMSE: {rmse:.4f}")
    
    # Create artifacts directory if it doesn't exist
    os.makedirs("artifacts", exist_ok=True)
    
    # Save model and scaler
    model_data = {
        "model": model,
        "scaler": scaler
    }
    
    with open("artifacts/model.pkl", "wb") as f:
        pickle.dump(model_data, f)
    
    print("Model saved to artifacts/model.pkl")
    return rmse

if __name__ == "__main__":
    train_model()

