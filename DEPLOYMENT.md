# eSim Platform - GCP Deployment Guide

This guide provides step-by-step instructions for deploying the eSim Platform to Google Cloud Platform (GCP) using Cloud Run.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Setup](#local-setup)
3. [GCP Project Setup](#gcp-project-setup)
4. [Docker Deployment](#docker-deployment)
5. [GCP Cloud Run Deployment](#gcp-cloud-run-deployment)
6. [Configuration](#configuration)
7. [Monitoring and Logging](#monitoring-and-logging)
8. [Troubleshooting](#troubleshooting)
9. [Cost Estimation](#cost-estimation)

## Prerequisites

### Required Software
- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher
- **gcloud CLI**: Latest version
- **Git**: For repository management
- **Node.js**: Version 18+ (for local frontend development)
- **Python**: Version 3.9+ (for local backend development)

### GCP Account
- Active GCP account with billing enabled
- Project with appropriate permissions
- Cloud Run API enabled
- Container Registry API enabled
- Cloud Build API enabled

## Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/findbhavin/eSIMPlatfornDesignAndArchitecture.git
cd eSIMPlatfornDesignAndArchitecture
```

### 2. Configure Environment Variables

**Backend Configuration:**
```bash
cd backend
cp .env.example .env
# Edit .env with your configuration
```

**Frontend Configuration:**
```bash
cd frontend
cp .env.example .env
# Edit .env with backend API URL
```

### 3. Local Development with Docker Compose

**Start all services:**
```bash
docker-compose up --build
```

**Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Health Check: http://localhost:8000/api/health

**Stop services:**
```bash
docker-compose down
```

## GCP Project Setup

### 1. Install and Configure gcloud CLI

```bash
# Install gcloud CLI (if not already installed)
# Visit: https://cloud.google.com/sdk/docs/install

# Initialize gcloud
gcloud init

# Set your project
gcloud config set project YOUR_PROJECT_ID
```

### 2. Enable Required APIs

```bash
# Enable Cloud Run API
gcloud services enable run.googleapis.com

# Enable Container Registry API
gcloud services enable containerregistry.googleapis.com

# Enable Cloud Build API
gcloud services enable cloudbuild.googleapis.com
```

### 3. Configure Authentication

```bash
# Authenticate with GCP
gcloud auth login

# Configure Docker to use gcloud as credential helper
gcloud auth configure-docker
```

## Docker Deployment

### Build Docker Images

**Backend:**
```bash
docker build -t esim-backend -f backend/Dockerfile .
```

**Frontend:**
```bash
docker build -t esim-frontend -f frontend/Dockerfile ./frontend
```

### Test Docker Images Locally

**Backend:**
```bash
docker run -p 8000:8000 esim-backend
```

**Frontend:**
```bash
docker run -p 3000:80 esim-frontend
```

## GCP Cloud Run Deployment

### Option 1: Using Cloud Build (Recommended)

**1. Update cloudbuild.yaml:**

Edit `gcp/cloudbuild.yaml` and replace `$PROJECT_ID` with your actual project ID.

**2. Submit build:**

```bash
gcloud builds submit --config=gcp/cloudbuild.yaml .
```

This will:
- Build both backend and frontend images
- Push images to Container Registry
- Deploy services to Cloud Run

### Option 2: Manual Deployment

**1. Build and push backend image:**

```bash
# Build
docker build -t gcr.io/YOUR_PROJECT_ID/esim-backend:latest -f backend/Dockerfile .

# Push to Container Registry
docker push gcr.io/YOUR_PROJECT_ID/esim-backend:latest
```

**2. Deploy backend to Cloud Run:**

```bash
gcloud run deploy esim-backend \
  --image gcr.io/YOUR_PROJECT_ID/esim-backend:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10 \
  --port 8000
```

**3. Get backend URL:**

```bash
BACKEND_URL=$(gcloud run services describe esim-backend \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)')

echo "Backend URL: $BACKEND_URL"
```

**4. Build frontend with backend URL:**

```bash
# Build frontend with backend URL
docker build \
  --build-arg REACT_APP_API_URL=${BACKEND_URL}/api \
  -t gcr.io/YOUR_PROJECT_ID/esim-frontend:latest \
  -f frontend/Dockerfile \
  ./frontend

# Push to Container Registry
docker push gcr.io/YOUR_PROJECT_ID/esim-frontend:latest
```

**5. Deploy frontend to Cloud Run:**

```bash
gcloud run deploy esim-frontend \
  --image gcr.io/YOUR_PROJECT_ID/esim-frontend:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10 \
  --port 80 \
  --set-env-vars REACT_APP_API_URL=${BACKEND_URL}/api
```

**6. Get frontend URL:**

```bash
FRONTEND_URL=$(gcloud run services describe esim-frontend \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)')

echo "Frontend URL: $FRONTEND_URL"
```

### Option 3: Using Service YAML Files

**1. Update service YAML files:**

Edit `gcp/backend-service.yaml` and `gcp/frontend-service.yaml`:
- Replace `PROJECT_ID` with your project ID
- Replace `XXXXXXXXX` in frontend service with backend service ID

**2. Deploy services:**

```bash
# Deploy backend
gcloud run services replace gcp/backend-service.yaml --region us-central1

# Deploy frontend
gcloud run services replace gcp/frontend-service.yaml --region us-central1
```

## Configuration

### Environment Variables

**Backend Environment Variables:**
- `PORT`: API port (default: 8000)
- `PYTHONUNBUFFERED`: Enable Python unbuffered mode (1)
- `ESIM_INSTALLATION_PATH`: Path to eSim installation
- `ESIM_TIMEOUT`: Simulation timeout in seconds
- `ESIM_OUTPUT_DIR`: Directory for simulation outputs

**Frontend Environment Variables:**
- `REACT_APP_API_URL`: Backend API URL (e.g., https://backend-xxx.run.app/api)

### Update Configuration

**For Cloud Run services:**

```bash
# Update backend environment variables
gcloud run services update esim-backend \
  --region us-central1 \
  --set-env-vars "PORT=8000,PYTHONUNBUFFERED=1"

# Update frontend environment variables
gcloud run services update esim-frontend \
  --region us-central1 \
  --set-env-vars "REACT_APP_API_URL=https://backend-xxx.run.app/api"
```

### Configure CORS

The backend API is configured to allow all origins by default. For production:

Edit `backend/api/main.py`:
```python
CORS(app, resources={r"/api/*": {"origins": ["https://your-frontend-domain.com"]}})
```

## Monitoring and Logging

### View Logs

**Backend logs:**
```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=esim-backend" \
  --limit 50 \
  --format json
```

**Frontend logs:**
```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=esim-frontend" \
  --limit 50 \
  --format json
```

### View Metrics

Access Cloud Run console:
```bash
# Open backend service in console
gcloud run services describe esim-backend --region us-central1

# Open frontend service in console
gcloud run services describe esim-frontend --region us-central1
```

Navigate to:
- GCP Console → Cloud Run → Select Service → Metrics

### Set Up Alerts

1. Go to Cloud Monitoring
2. Create alert policies for:
   - High error rate
   - High latency
   - Resource utilization
   - Cost thresholds

### Health Checks

**Backend health check:**
```bash
curl https://YOUR_BACKEND_URL/api/health
```

**Frontend health check:**
```bash
curl https://YOUR_FRONTEND_URL/health
```

## Troubleshooting

### Common Issues

#### 1. Container Fails to Start

**Check logs:**
```bash
gcloud logging read "resource.type=cloud_run_revision" --limit 50
```

**Common causes:**
- Port mismatch (ensure container listens on PORT env variable)
- Missing dependencies
- Configuration errors

#### 2. Backend API Not Accessible

**Check service URL:**
```bash
gcloud run services describe esim-backend --region us-central1 --format 'value(status.url)'
```

**Verify health endpoint:**
```bash
curl https://YOUR_BACKEND_URL/api/health
```

#### 3. Frontend Can't Connect to Backend

**Verify environment variable:**
```bash
gcloud run services describe esim-frontend --region us-central1 --format 'value(spec.template.spec.containers[0].env)'
```

**Update backend URL:**
```bash
gcloud run services update esim-frontend \
  --region us-central1 \
  --set-env-vars "REACT_APP_API_URL=https://correct-backend-url.run.app/api"
```

#### 4. Memory or CPU Issues

**Check resource usage:**
- Go to Cloud Run console
- View metrics for the service
- Adjust resources if needed:

```bash
gcloud run services update esim-backend \
  --region us-central1 \
  --memory 2Gi \
  --cpu 2
```

#### 5. Build Failures

**Check Cloud Build logs:**
```bash
gcloud builds list --limit 10
gcloud builds log BUILD_ID
```

### Debug Mode

**Enable debug logging for backend:**
```bash
gcloud run services update esim-backend \
  --region us-central1 \
  --set-env-vars "FLASK_DEBUG=1"
```

## Cost Estimation

### Cloud Run Pricing (us-central1)

**Compute:**
- CPU: $0.00002400 per vCPU-second
- Memory: $0.00000250 per GiB-second
- Requests: $0.40 per million requests

**Example Monthly Cost (Low Traffic):**

Assumptions:
- 10,000 requests/month
- Average 100ms response time
- Backend: 1 CPU, 1Gi RAM
- Frontend: 1 CPU, 512Mi RAM

| Component | Cost/Month |
|-----------|-----------|
| Backend CPU | ~$5 |
| Backend Memory | ~$2 |
| Frontend CPU | ~$2 |
| Frontend Memory | ~$0.50 |
| Requests | ~$0.01 |
| **Total** | **~$10** |

**Example Monthly Cost (Medium Traffic):**

Assumptions:
- 1,000,000 requests/month
- Average 200ms response time
- Backend: 1 CPU, 1Gi RAM
- Frontend: 1 CPU, 512Mi RAM

| Component | Cost/Month |
|-----------|-----------|
| Backend CPU | ~$100 |
| Backend Memory | ~$40 |
| Frontend CPU | ~$50 |
| Frontend Memory | ~$10 |
| Requests | ~$0.40 |
| **Total** | **~$200** |

**Additional Costs:**
- Container Registry storage: ~$0.026/GB/month
- Cloud Build: First 120 build-minutes/day free
- Networking: Egress charges may apply

### Cost Optimization Tips

1. **Set minimum instances to 0** for development/staging
2. **Use request-based scaling** instead of CPU-based
3. **Optimize Docker images** to reduce storage costs
4. **Set appropriate timeout values** to avoid hanging requests
5. **Enable Cloud CDN** for static frontend assets
6. **Use Cloud Scheduler** to warm up instances before peak hours

### Monitor Costs

```bash
# View current month's costs
gcloud billing accounts list
```

Set up budget alerts in GCP Console:
1. Go to Billing → Budgets & alerts
2. Create budget for your project
3. Set threshold alerts (50%, 90%, 100%)

## Next Steps

After successful deployment:

1. **Custom Domain**: Set up custom domain mapping
2. **SSL/TLS**: Configure HTTPS (automatic with Cloud Run)
3. **Authentication**: Implement user authentication if needed
4. **Database**: Set up Cloud SQL or Firestore if needed
5. **Backups**: Configure automated backups for data
6. **CI/CD**: Set up automated deployments with Cloud Build triggers
7. **Load Testing**: Test performance under load
8. **Security**: Implement security best practices

## Support

For issues or questions:
- Check logs: `gcloud logging read`
- Review Cloud Run documentation: https://cloud.google.com/run/docs
- GitHub Issues: https://github.com/findbhavin/eSIMPlatfornDesignAndArchitecture/issues

---

**Last Updated**: February 2026  
**Version**: 1.0.0
