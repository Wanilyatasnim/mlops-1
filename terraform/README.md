# Terraform Infrastructure as Code

This directory contains Terraform configurations for provisioning infrastructure on Google Cloud Platform.

## Prerequisites

1. **Install Terraform**: [Download Terraform](https://www.terraform.io/downloads)
2. **GCP Account**: Create a GCP project and enable billing
3. **Service Account**: Create a service account with required permissions:
   - Cloud Run Admin
   - Service Account User
   - Storage Admin (for state backend, if used)

## Setup

1. **Configure variables**:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your values
   ```

2. **Authenticate with GCP**:
   ```bash
   gcloud auth application-default login
   # OR
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account-key.json"
   ```

3. **Initialize Terraform**:
   ```bash
   cd terraform
   terraform init
   ```

4. **Plan deployment**:
   ```bash
   terraform plan
   ```

5. **Apply configuration**:
   ```bash
   terraform apply
   ```

## What Gets Created

- **3 Cloud Run Services**:
  - `api-gateway` - API Gateway service
  - `ml-service` - ML prediction service
  - `user-service` - User management service

- **IAM Policies**: Public access permissions (configurable)

- **Required APIs**: Automatically enabled:
  - Cloud Run API
  - Cloud Build API
  - Container Registry API
  - Compute Engine API

## Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `gcp_project_id` | GCP Project ID | Required |
| `gcp_region` | GCP Region | `us-central1` |
| `gcp_zone` | GCP Zone | `us-central1-a` |
| `docker_registry` | Docker registry URL | `docker.io` |
| `docker_username` | Docker Hub username | Required |

## Outputs

After applying, Terraform will output:
- `api_gateway_url` - API Gateway service URL
- `ml_service_url` - ML Service URL
- `user_service_url` - User Service URL

## Destroying Infrastructure

To tear down all resources:
```bash
terraform destroy
```

## Remote State (Optional)

To use remote state with GCS backend, uncomment and configure the backend block in `main.tf`:

```hcl
backend "gcs" {
  bucket = "your-terraform-state-bucket"
  prefix = "mlops/state"
}
```

Then create the bucket:
```bash
gsutil mb gs://your-terraform-state-bucket
gsutil versioning set on gs://your-terraform-state-bucket
```

