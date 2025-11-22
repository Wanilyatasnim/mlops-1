# Use Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY artifacts/ ./artifacts/

# Expose port 8080
EXPOSE 8080

# Set environment variable
ENV PYTHONUNBUFFERED=1

# Run FastAPI app with uvicorn
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8080"]

