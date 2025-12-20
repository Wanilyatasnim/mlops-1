"""
API Gateway - Routes requests to microservices.
"""

import os
import time
import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from .logger import setup_logging, get_logger
from .metrics import request_count, request_latency

# Setup logging
setup_logging(os.getenv("LOG_LEVEL", "INFO"))
logger = get_logger(__name__)

app = FastAPI(title="API Gateway")

# Service URLs (from environment or defaults)
ML_SERVICE_URL = os.getenv("ML_SERVICE_URL", "http://ml-service:8081")
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:8082")
NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL", "http://notification-service:8083")

# HTTP client for forwarding requests
http_client = httpx.AsyncClient(timeout=30.0)

@app.on_event("startup")
async def startup():
    """Initialize service on startup."""
    logger.info("API Gateway starting up...")
    logger.info(f"ML Service URL: {ML_SERVICE_URL}")
    logger.info(f"User Service URL: {USER_SERVICE_URL}")
    logger.info(f"Notification Service URL: {NOTIFICATION_SERVICE_URL}")

@app.on_event("shutdown")
async def shutdown():
    """Cleanup on shutdown."""
    await http_client.aclose()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "api-gateway",
        "message": "API Gateway - Microservices Router",
        "services": {
            "ml-service": ML_SERVICE_URL,
            "user-service": USER_SERVICE_URL,
            "notification-service": NOTIFICATION_SERVICE_URL
        },
        "endpoints": {
            "ml": {
                "predict": "/api/ml/predict",
                "health": "/api/ml/health"
            },
            "user": {
                "register": "/api/users/register",
                "login": "/api/users/login",
                "users": "/api/users",
                "health": "/api/users/health"
            },
            "notification": {
                "send": "/api/notifications/send",
                "history": "/api/notifications/history",
                "health": "/api/notifications/health"
            },
            "gateway": {
                "health": "/health",
                "metrics": "/metrics"
            }
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint."""
    # Check downstream services
    services_status = {}
    
    try:
        ml_response = await http_client.get(f"{ML_SERVICE_URL}/health", timeout=5.0)
        services_status["ml-service"] = ml_response.status_code == 200
    except Exception as e:
        logger.warning(f"ML Service health check failed: {e}")
        services_status["ml-service"] = False
    
    try:
        user_response = await http_client.get(f"{USER_SERVICE_URL}/health", timeout=5.0)
        services_status["user-service"] = user_response.status_code == 200
    except Exception as e:
        logger.warning(f"User Service health check failed: {e}")
        services_status["user-service"] = False
    
    try:
        notif_response = await http_client.get(f"{NOTIFICATION_SERVICE_URL}/health", timeout=5.0)
        services_status["notification-service"] = notif_response.status_code == 200
    except Exception as e:
        logger.warning(f"Notification Service health check failed: {e}")
        services_status["notification-service"] = False
    
    all_healthy = all(services_status.values())
    
    return {
        "status": "healthy" if all_healthy else "degraded",
        "service": "api-gateway",
        "services": services_status
    }

# ML Service Routes
@app.post("/api/ml/predict")
async def ml_predict(request: Request):
    """Forward prediction request to ML service."""
    start_time = time.time()
    
    try:
        body = await request.json()
        
        response = await http_client.post(
            f"{ML_SERVICE_URL}/predict",
            json=body,
            timeout=10.0
        )
        
        request_count.labels(
            method="POST",
            endpoint="/api/ml/predict",
            status=str(response.status_code)
        ).inc()
        
        latency = time.time() - start_time
        request_latency.labels(
            method="POST",
            endpoint="/api/ml/predict"
        ).observe(latency)
        
        if response.status_code != 200:
            logger.error(f"ML Service error: {response.status_code} - {response.text}")
        
        return JSONResponse(
            content=response.json(),
            status_code=response.status_code
        )
    
    except httpx.TimeoutException:
        request_count.labels(
            method="POST",
            endpoint="/api/ml/predict",
            status="504"
        ).inc()
        latency = time.time() - start_time
        request_latency.labels(
            method="POST",
            endpoint="/api/ml/predict"
        ).observe(latency)
        raise HTTPException(status_code=504, detail="ML Service timeout")
    except Exception as e:
        request_count.labels(
            method="POST",
            endpoint="/api/ml/predict",
            status="500"
        ).inc()
        latency = time.time() - start_time
        request_latency.labels(
            method="POST",
            endpoint="/api/ml/predict"
        ).observe(latency)
        logger.error(f"Gateway error forwarding to ML service: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/ml/health")
async def ml_health():
    """Forward health check to ML service."""
    try:
        response = await http_client.get(f"{ML_SERVICE_URL}/health", timeout=5.0)
        return JSONResponse(
            content=response.json(),
            status_code=response.status_code
        )
    except Exception as e:
        logger.error(f"ML Service health check error: {e}")
        raise HTTPException(status_code=503, detail="ML Service unavailable")

# User Service Routes
@app.post("/api/users/register")
async def user_register(request: Request):
    """Forward user registration to user service."""
    start_time = time.time()
    
    try:
        body = await request.json()
        
        response = await http_client.post(
            f"{USER_SERVICE_URL}/users/register",
            json=body,
            timeout=10.0
        )
        
        request_count.labels(
            method="POST",
            endpoint="/api/users/register",
            status=str(response.status_code)
        ).inc()
        
        latency = time.time() - start_time
        request_latency.labels(
            method="POST",
            endpoint="/api/users/register"
        ).observe(latency)
        
        return JSONResponse(
            content=response.json(),
            status_code=response.status_code
        )
    
    except Exception as e:
        request_count.labels(
            method="POST",
            endpoint="/api/users/register",
            status="500"
        ).inc()
        latency = time.time() - start_time
        request_latency.labels(
            method="POST",
            endpoint="/api/users/register"
        ).observe(latency)
        logger.error(f"Gateway error forwarding to user service: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/users/login")
async def user_login(request: Request):
    """Forward user login to user service."""
    start_time = time.time()
    
    try:
        body = await request.json()
        
        response = await http_client.post(
            f"{USER_SERVICE_URL}/users/login",
            json=body,
            timeout=10.0
        )
        
        request_count.labels(
            method="POST",
            endpoint="/api/users/login",
            status=str(response.status_code)
        ).inc()
        
        latency = time.time() - start_time
        request_latency.labels(
            method="POST",
            endpoint="/api/users/login"
        ).observe(latency)
        
        return JSONResponse(
            content=response.json(),
            status_code=response.status_code
        )
    
    except Exception as e:
        request_count.labels(
            method="POST",
            endpoint="/api/users/login",
            status="500"
        ).inc()
        latency = time.time() - start_time
        request_latency.labels(
            method="POST",
            endpoint="/api/users/login"
        ).observe(latency)
        logger.error(f"Gateway error forwarding to user service: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/users")
async def list_users(request: Request):
    """Forward list users request to user service."""
    start_time = time.time()
    
    try:
        # Forward authorization header
        auth_header = request.headers.get("Authorization")
        headers = {}
        if auth_header:
            headers["Authorization"] = auth_header
        
        response = await http_client.get(
            f"{USER_SERVICE_URL}/users",
            headers=headers,
            timeout=10.0
        )
        
        request_count.labels(
            method="GET",
            endpoint="/api/users",
            status=str(response.status_code)
        ).inc()
        
        latency = time.time() - start_time
        request_latency.labels(
            method="GET",
            endpoint="/api/users"
        ).observe(latency)
        
        return JSONResponse(
            content=response.json(),
            status_code=response.status_code
        )
    
    except Exception as e:
        request_count.labels(
            method="GET",
            endpoint="/api/users",
            status="500"
        ).inc()
        latency = time.time() - start_time
        request_latency.labels(
            method="GET",
            endpoint="/api/users"
        ).observe(latency)
        logger.error(f"Gateway error forwarding to user service: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/users/health")
async def user_health():
    """Forward health check to user service."""
    try:
        response = await http_client.get(f"{USER_SERVICE_URL}/health", timeout=5.0)
        return JSONResponse(
            content=response.json(),
            status_code=response.status_code
        )
    except Exception as e:
        logger.error(f"User Service health check error: {e}")
        raise HTTPException(status_code=503, detail="User Service unavailable")

# Notification Service Routes
@app.post("/api/notifications/send")
async def send_notification(request: Request):
    """Forward notification request to notification service."""
    start_time = time.time()
    
    try:
        body = await request.json()
        
        response = await http_client.post(
            f"{NOTIFICATION_SERVICE_URL}/notifications/send",
            json=body,
            timeout=10.0
        )
        
        request_count.labels(
            method="POST",
            endpoint="/api/notifications/send",
            status=str(response.status_code)
        ).inc()
        
        latency = time.time() - start_time
        request_latency.labels(
            method="POST",
            endpoint="/api/notifications/send"
        ).observe(latency)
        
        return JSONResponse(
            content=response.json(),
            status_code=response.status_code
        )
    
    except Exception as e:
        request_count.labels(
            method="POST",
            endpoint="/api/notifications/send",
            status="500"
        ).inc()
        latency = time.time() - start_time
        request_latency.labels(
            method="POST",
            endpoint="/api/notifications/send"
        ).observe(latency)
        logger.error(f"Gateway error forwarding to notification service: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/notifications/history")
async def notification_history(request: Request):
    """Forward notification history request to notification service."""
    start_time = time.time()
    
    try:
        params = dict(request.query_params)
        
        response = await http_client.get(
            f"{NOTIFICATION_SERVICE_URL}/notifications/history",
            params=params,
            timeout=10.0
        )
        
        request_count.labels(
            method="GET",
            endpoint="/api/notifications/history",
            status=str(response.status_code)
        ).inc()
        
        latency = time.time() - start_time
        request_latency.labels(
            method="GET",
            endpoint="/api/notifications/history"
        ).observe(latency)
        
        return JSONResponse(
            content=response.json(),
            status_code=response.status_code
        )
    
    except Exception as e:
        request_count.labels(
            method="GET",
            endpoint="/api/notifications/history",
            status="500"
        ).inc()
        latency = time.time() - start_time
        request_latency.labels(
            method="GET",
            endpoint="/api/notifications/history"
        ).observe(latency)
        logger.error(f"Gateway error forwarding to notification service: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/notifications/health")
async def notification_health():
    """Forward health check to notification service."""
    try:
        response = await http_client.get(f"{NOTIFICATION_SERVICE_URL}/health", timeout=5.0)
        return JSONResponse(
            content=response.json(),
            status_code=response.status_code
        )
    except Exception as e:
        logger.error(f"Notification Service health check error: {e}")
        raise HTTPException(status_code=503, detail="Notification Service unavailable")

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    from .metrics import get_metrics
    return Response(
        content=get_metrics(),
        media_type="text/plain; version=0.0.4; charset=utf-8"
    )

