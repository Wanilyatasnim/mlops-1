"""
User Service - FastAPI service for user management and authentication.
"""

import os
import time
import hashlib
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.responses import Response
from pydantic import BaseModel, EmailStr, Field
from .logger import setup_logging, get_logger
from .metrics import request_count, request_latency

# Setup logging
setup_logging(os.getenv("LOG_LEVEL", "INFO"))
logger = get_logger(__name__)

app = FastAPI(title="User Service")

# In-memory user store (in production, use a database)
users_db = {}
tokens_db = {}

class UserCreate(BaseModel):
    """Request model for user creation."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    """Response model for user."""
    id: str
    username: str
    email: str
    created_at: str

class UserLogin(BaseModel):
    """Request model for user login."""
    username: str
    password: str

class TokenResponse(BaseModel):
    """Response model for authentication token."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int

def hash_password(password: str) -> str:
    """Hash password using SHA256 (for demo purposes)."""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token(user_id: str) -> str:
    """Generate a simple token (in production, use JWT)."""
    import secrets
    token = secrets.token_urlsafe(32)
    tokens_db[token] = {
        "user_id": user_id,
        "expires_at": datetime.now() + timedelta(hours=24)
    }
    return token

@app.on_event("startup")
async def startup():
    """Initialize service on startup."""
    logger.info("User Service starting up...")
    # Create a default admin user for testing
    admin_id = "admin-001"
    users_db[admin_id] = {
        "id": admin_id,
        "username": "admin",
        "email": "admin@example.com",
        "password_hash": hash_password("admin123"),
        "created_at": datetime.now().isoformat()
    }
    logger.info("User Service started successfully")

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "user-service",
        "message": "User Service - User Management and Authentication",
        "endpoints": {
            "register": "/users/register",
            "login": "/users/login",
            "users": "/users",
            "health": "/health",
            "metrics": "/metrics"
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "user-service"}

@app.post("/users/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    """Register a new user."""
    start_time = time.time()
    
    try:
        # Check if username already exists
        for uid, u in users_db.items():
            if u["username"] == user.username:
                raise HTTPException(status_code=400, detail="Username already exists")
            if u["email"] == user.email:
                raise HTTPException(status_code=400, detail="Email already exists")
        
        # Create new user
        user_id = f"user-{len(users_db) + 1:03d}"
        users_db[user_id] = {
            "id": user_id,
            "username": user.username,
            "email": user.email,
            "password_hash": hash_password(user.password),
            "created_at": datetime.now().isoformat()
        }
        
        request_count.labels(method="POST", endpoint="/users/register", status="200").inc()
        latency = time.time() - start_time
        request_latency.labels(method="POST", endpoint="/users/register").observe(latency)
        
        logger.info(f"User registered: {user.username} (ID: {user_id})")
        
        return UserResponse(
            id=user_id,
            username=user.username,
            email=user.email,
            created_at=users_db[user_id]["created_at"]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        request_count.labels(method="POST", endpoint="/users/register", status="500").inc()
        latency = time.time() - start_time
        request_latency.labels(method="POST", endpoint="/users/register").observe(latency)
        logger.error(f"Registration error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/users/login", response_model=TokenResponse)
async def login_user(credentials: UserLogin):
    """Authenticate user and return access token."""
    start_time = time.time()
    
    try:
        # Find user
        user = None
        for uid, u in users_db.items():
            if u["username"] == credentials.username:
                user = u
                break
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        # Verify password
        password_hash = hash_password(credentials.password)
        if user["password_hash"] != password_hash:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        # Generate token
        token = generate_token(user["id"])
        
        request_count.labels(method="POST", endpoint="/users/login", status="200").inc()
        latency = time.time() - start_time
        request_latency.labels(method="POST", endpoint="/users/login").observe(latency)
        
        logger.info(f"User logged in: {credentials.username}")
        
        return TokenResponse(
            access_token=token,
            expires_in=86400  # 24 hours
        )
    
    except HTTPException:
        raise
    except Exception as e:
        request_count.labels(method="POST", endpoint="/users/login", status="500").inc()
        latency = time.time() - start_time
        request_latency.labels(method="POST", endpoint="/users/login").observe(latency)
        logger.error(f"Login error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users", response_model=List[UserResponse])
async def list_users(authorization: Optional[str] = Header(None)):
    """List all users (requires authentication)."""
    start_time = time.time()
    
    try:
        # Simple token validation (in production, use proper JWT validation)
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
        
        token = authorization.replace("Bearer ", "")
        if token not in tokens_db:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        token_data = tokens_db[token]
        if datetime.now() > token_data["expires_at"]:
            raise HTTPException(status_code=401, detail="Token expired")
        
        # Return all users (excluding password hashes)
        users = [
            UserResponse(
                id=u["id"],
                username=u["username"],
                email=u["email"],
                created_at=u["created_at"]
            )
            for u in users_db.values()
        ]
        
        request_count.labels(method="GET", endpoint="/users", status="200").inc()
        latency = time.time() - start_time
        request_latency.labels(method="GET", endpoint="/users").observe(latency)
        
        return users
    
    except HTTPException:
        raise
    except Exception as e:
        request_count.labels(method="GET", endpoint="/users", status="500").inc()
        latency = time.time() - start_time
        request_latency.labels(method="GET", endpoint="/users").observe(latency)
        logger.error(f"List users error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    from .metrics import get_metrics
    return Response(
        content=get_metrics(),
        media_type="text/plain; version=0.0.4; charset=utf-8"
    )

