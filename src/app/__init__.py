"""FastAPI application package."""

# Initialize logging when package is imported
import os
from .logger import setup_logging

# Setup logging with default INFO level
setup_logging(os.getenv("LOG_LEVEL", "INFO"))

