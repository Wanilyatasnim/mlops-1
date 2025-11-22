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
    
    # Get the project root directory (parent of src/)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    model_path = os.path.join(project_root, "artifacts", "model.pkl")
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model file not found at {model_path}. "
            "Please run train.py first to generate the model."
        )
    
    with open(model_path, "rb") as f:
        model_data = pickle.load(f)
    
    print(f"Model loaded successfully from {model_path}!")

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
    return {"status": "healthy", "model_loaded": model_data is not None}

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
        # Validate features
        if len(request.features) != 8:
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
        
        return PredictionResponse(prediction=float(prediction))
    
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
        
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    from .metrics import get_metrics
    return Response(
        content=get_metrics(),
        media_type="text/plain; version=0.0.4; charset=utf-8"
    )

