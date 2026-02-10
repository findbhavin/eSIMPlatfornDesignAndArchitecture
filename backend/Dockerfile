# Backend Dockerfile for eSim Platform API
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ngspice \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY backend/requirements-api.txt /app/backend/requirements-api.txt
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/backend/requirements-api.txt

# Copy application code
COPY src/ /app/src/
COPY backend/ /app/backend/
COPY circuits/ /app/circuits/
COPY config.yaml /app/config.yaml

# Create necessary directories
RUN mkdir -p /tmp/uploads

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Run with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120", "backend.api.main:create_app()"]
