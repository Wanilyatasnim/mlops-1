"""
Notification Service - FastAPI service for sending notifications.
"""

import os
import time
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, EmailStr, Field
from .logger import setup_logging, get_logger
from .metrics import request_count, request_latency

# Setup logging
setup_logging(os.getenv("LOG_LEVEL", "INFO"))
logger = get_logger(__name__)

app = FastAPI(title="Notification Service")

# In-memory notification store (in production, use a database)
notifications_db = []

class NotificationRequest(BaseModel):
    """Request model for sending notification."""
    user_id: str
    email: EmailStr
    subject: str = Field(..., min_length=1, max_length=200)
    message: str = Field(..., min_length=1)
    notification_type: str = Field(default="email", pattern="^(email|sms|push)$")

class NotificationResponse(BaseModel):
    """Response model for notification."""
    id: str
    user_id: str
    status: str
    sent_at: str

@app.on_event("startup")
async def startup():
    """Initialize service on startup."""
    logger.info("Notification Service starting up...")
    logger.info("Notification Service started successfully")

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "notification-service",
        "message": "Notification Service - Email, SMS, and Push Notifications",
        "endpoints": {
            "send": "/notifications/send",
            "history": "/notifications/history",
            "health": "/health",
            "metrics": "/metrics"
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "notification-service"}

@app.post("/notifications/send", response_model=NotificationResponse)
async def send_notification(notification: NotificationRequest):
    """Send a notification (email, SMS, or push)."""
    start_time = time.time()
    
    try:
        # Simulate sending notification
        # In production, integrate with email service (SendGrid, SES, etc.)
        # or SMS service (Twilio, etc.)
        
        notification_id = f"notif-{len(notifications_db) + 1:06d}"
        
        # Simulate async processing
        import asyncio
        await asyncio.sleep(0.1)  # Simulate network delay
        
        notification_record = {
            "id": notification_id,
            "user_id": notification.user_id,
            "email": notification.email,
            "subject": notification.subject,
            "message": notification.message,
            "type": notification.notification_type,
            "status": "sent",
            "sent_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        notifications_db.append(notification_record)
        
        request_count.labels(
            method="POST",
            endpoint="/notifications/send",
            status="200"
        ).inc()
        
        latency = time.time() - start_time
        request_latency.labels(
            method="POST",
            endpoint="/notifications/send"
        ).observe(latency)
        
        logger.info(f"Notification sent: {notification_id} to {notification.email} ({notification.notification_type})")
        
        return NotificationResponse(
            id=notification_id,
            user_id=notification.user_id,
            status="sent",
            sent_at=notification_record["sent_at"]
        )
    
    except Exception as e:
        request_count.labels(
            method="POST",
            endpoint="/notifications/send",
            status="500"
        ).inc()
        latency = time.time() - start_time
        request_latency.labels(
            method="POST",
            endpoint="/notifications/send"
        ).observe(latency)
        logger.error(f"Notification error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/notifications/history", response_model=List[dict])
async def get_notification_history(user_id: Optional[str] = None, limit: int = 50):
    """Get notification history."""
    start_time = time.time()
    
    try:
        filtered_notifications = notifications_db
        
        if user_id:
            filtered_notifications = [n for n in notifications_db if n["user_id"] == user_id]
        
        # Return most recent first
        result = sorted(filtered_notifications, key=lambda x: x["sent_at"], reverse=True)[:limit]
        
        request_count.labels(
            method="GET",
            endpoint="/notifications/history",
            status="200"
        ).inc()
        
        latency = time.time() - start_time
        request_latency.labels(
            method="GET",
            endpoint="/notifications/history"
        ).observe(latency)
        
        return result
    
    except Exception as e:
        request_count.labels(
            method="GET",
            endpoint="/notifications/history",
            status="500"
        ).inc()
        latency = time.time() - start_time
        request_latency.labels(
            method="GET",
            endpoint="/notifications/history"
        ).observe(latency)
        logger.error(f"Get history error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    from .metrics import get_metrics
    return Response(
        content=get_metrics(),
        media_type="text/plain; version=0.0.4; charset=utf-8"
    )

