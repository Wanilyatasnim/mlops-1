"""
Training script for California Housing dataset using Ridge Regression.
Saves the trained model to artifacts/model.pkl
"""

import pickle
import os
import logging
import time
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
import numpy as np

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def train_model():
    """Train Ridge regression model on California Housing dataset."""
    train_start_time = time.time()
    logger.info("=" * 60)
    logger.info("Starting model training pipeline")
    logger.info("=" * 60)
    
    # Load dataset
    logger.info("Loading California Housing dataset...")
    load_start = time.time()
    data = fetch_california_housing()
    X, y = data.data, data.target
    load_time = time.time() - load_start
    logger.info(f"Dataset loaded: {X.shape[0]} samples, {X.shape[1]} features (took {load_time:.3f}s)")
    
    # Split data
    logger.info("Splitting dataset into train/test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    logger.info(f"Train set: {X_train.shape[0]} samples, Test set: {X_test.shape[0]} samples")
    
    # Scale features
    logger.info("Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    logger.info("Feature scaling completed")
    
    # Train model
    logger.info("Training Ridge regression model (alpha=1.0)...")
    train_start = time.time()
    model = Ridge(alpha=1.0, random_state=42)
    model.fit(X_train_scaled, y_train)
    train_time = time.time() - train_start
    logger.info(f"Model training completed in {train_time:.3f}s")
    
    # Evaluate
    logger.info("Evaluating model on test set...")
    y_pred = model.predict(X_test_scaled)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    logger.info(f"Model RMSE: {rmse:.4f}")
    
    # Create artifacts directory if it doesn't exist
    os.makedirs("artifacts", exist_ok=True)
    
    # Save model and scaler
    logger.info("Saving model artifact...")
    model_data = {
        "model": model,
        "scaler": scaler
    }
    
    save_start = time.time()
    with open("artifacts/model.pkl", "wb") as f:
        pickle.dump(model_data, f)
    save_time = time.time() - save_start
    
    total_time = time.time() - train_start_time
    logger.info(f"Model saved to artifacts/model.pkl (took {save_time:.3f}s)")
    logger.info("=" * 60)
    logger.info(f"Training pipeline completed successfully in {total_time:.3f}s")
    logger.info(f"Final RMSE: {rmse:.4f}")
    logger.info("=" * 60)
    
    return rmse

if __name__ == "__main__":
    train_model()

