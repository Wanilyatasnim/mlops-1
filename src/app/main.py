"""
FastAPI inference service for California Housing price predictions.
"""

import pickle
import os
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field
from typing import List
from .metrics import (
    request_count,
    request_latency,
    prediction_count,
    prediction_errors
)
from .logger import setup_logging, get_logger

# Setup logging
setup_logging(os.getenv("LOG_LEVEL", "INFO"))
logger = get_logger(__name__)

app = FastAPI(title="California Housing Price Prediction API")

# Global model and scaler
model_data = None

class PredictionRequest(BaseModel):
    """Request model for prediction endpoint."""
    features: List[float] = Field(
        ...,
        description="List of 8 numeric features for California Housing dataset",
        min_length=8,
        max_length=8
    )

class PredictionResponse(BaseModel):
    """Response model for prediction endpoint."""
    prediction: float

@app.on_event("startup")
async def load_model():
    """Load the trained model and scaler at startup."""
    global model_data
    
    logger.info("Starting model loading process...")
    load_start_time = time.time()
    
    # Option 1: Load from GCS if MODEL_GCS_PATH is set
    model_gcs_path = os.getenv("MODEL_GCS_PATH")
    if model_gcs_path:
        try:
            logger.info(f"Attempting to load model from GCS: {model_gcs_path}")
            from google.cloud import storage
            # Parse GCS path: gs://bucket-name/path/to/model.pkl
            bucket_name = model_gcs_path.split("/")[2]
            blob_path = "/".join(model_gcs_path.split("/")[3:])
            
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_path)
            
            # Download to temporary file
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pkl") as tmp_file:
                blob.download_to_filename(tmp_file.name)
                with open(tmp_file.name, "rb") as f:
                    model_data = pickle.load(f)
                os.unlink(tmp_file.name)
            
            load_time = time.time() - load_start_time
            logger.info(f"Model loaded successfully from GCS in {load_time:.3f}s: {model_gcs_path}")
            return
        except ImportError:
            logger.warning("google-cloud-storage not installed. Falling back to local model.")
        except Exception as e:
            logger.error(f"Error loading from GCS: {e}. Falling back to local model.", exc_info=True)
    
    # Option 2: Load from local artifacts directory (default)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    model_path = os.path.join(project_root, "artifacts", "model.pkl")
    
    if not os.path.exists(model_path):
        logger.error(f"Model file not found at {model_path}")
        raise FileNotFoundError(
            f"Model file not found at {model_path}. "
            "Please run train.py first to generate the model, or set MODEL_GCS_PATH environment variable."
        )
    
    logger.info(f"Loading model from local path: {model_path}")
    with open(model_path, "rb") as f:
        model_data = pickle.load(f)
    
    load_time = time.time() - load_start_time
    logger.info(f"Model loaded successfully from {model_path} in {load_time:.3f}s")

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "California Housing Price Prediction API",
        "endpoints": {
            "predict": "/predict",
            "metrics": "/metrics",
            "health": "/health"
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint."""
    is_healthy = model_data is not None
    if not is_healthy:
        logger.warning("Health check failed: model not loaded")
    return {"status": "healthy", "model_loaded": is_healthy}

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Predict California Housing price from input features.
    
    Expected features (8 total):
    - MedInc: Median income in block group
    - HouseAge: Median house age in block group
    - AveRooms: Average number of rooms per household
    - AveBedrms: Average number of bedrooms per household
    - Population: Block group population
    - AveOccup: Average number of household members
    - Latitude: Block group latitude
    - Longitude: Block group longitude
    """
    start_time = time.time()
    
    try:
        logger.info(f"Received prediction request with {len(request.features)} features")
        
        # Validate features
        if len(request.features) != 8:
            logger.warning(f"Invalid feature count: expected 8, got {len(request.features)}")
            raise HTTPException(
                status_code=400,
                detail="Exactly 8 features are required"
            )
        
        # Prepare features
        import numpy as np
        features_array = np.array([request.features])
        
        # Scale features
        scaler = model_data["scaler"]
        features_scaled = scaler.transform(features_array)
        
        # Make prediction
        model = model_data["model"]
        prediction = model.predict(features_scaled)[0]
        
        # Update metrics
        prediction_count.inc()
        request_count.labels(
            method="POST",
            endpoint="/predict",
            status="200"
        ).inc()
        
        latency = time.time() - start_time
        request_latency.labels(
            method="POST",
            endpoint="/predict"
        ).observe(latency)
        
        # Log latency warning if prediction takes too long
        if latency > 1.0:
            logger.warning(f"Slow prediction detected: {latency:.3f}s (features: {request.features[:3]}...)")
        elif latency > 0.5:
            logger.warning(f"Prediction latency above average: {latency:.3f}s")
        else:
            logger.debug(f"Prediction completed in {latency:.3f}s")
        
        logger.info(f"Prediction successful: {prediction:.4f} (latency: {latency:.3f}s)")
        
        return PredictionResponse(prediction=float(prediction))
    
    except HTTPException:
        # Re-raise HTTP exceptions (validation errors)
        raise
    except Exception as e:
        # Update error metrics
        prediction_errors.inc()
        request_count.labels(
            method="POST",
            endpoint="/predict",
            status="500"
        ).inc()
        
        latency = time.time() - start_time
        request_latency.labels(
            method="POST",
            endpoint="/predict"
        ).observe(latency)
        
        logger.error(
            f"Prediction error: {str(e)} (latency: {latency:.3f}s)",
            exc_info=True
        )
        
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    from .metrics import get_metrics
    return Response(
        content=get_metrics(),
        media_type="text/plain; version=0.0.4; charset=utf-8"
    )

