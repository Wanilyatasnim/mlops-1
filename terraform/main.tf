terraform {
  required_version = ">= 1.0"
  
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
  
  # Optional: Use remote state backend (uncomment and configure)
  # backend "gcs" {
  #   bucket = "your-terraform-state-bucket"
  #   prefix = "mlops/state"
  # }
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
  zone    = var.gcp_zone
}

# Enable required APIs
resource "google_project_service" "required_apis" {
  for_each = toset([
    "run.googleapis.com",
    "cloudbuild.googleapis.com",
    "containerregistry.googleapis.com",
    "compute.googleapis.com"
  ])
  
  service = each.value
  project = var.gcp_project_id
  
  disable_on_destroy = false
}

# Cloud Run Service - API Gateway
resource "google_cloud_run_service" "api_gateway" {
  name     = "api-gateway"
  location = var.gcp_region
  
  template {
    spec {
      containers {
        image = "${var.docker_registry}/${var.docker_username}/api-gateway:latest"
        
        ports {
          container_port = 8080
        }
        
        env {
          name  = "ML_SERVICE_URL"
          value = "https://ml-service-${replace(var.gcp_project_id, ":", "-")}-${var.gcp_region}.a.run.app"
        }
        
        env {
          name  = "USER_SERVICE_URL"
          value = "https://user-service-${replace(var.gcp_project_id, ":", "-")}-${var.gcp_region}.a.run.app"
        }
        
        env {
          name  = "NOTIFICATION_SERVICE_URL"
          value = "https://notification-service-${replace(var.gcp_project_id, ":", "-")}-${var.gcp_region}.a.run.app"
        }
        
        resources {
          limits = {
            cpu    = "1"
            memory = "512Mi"
          }
        }
      }
      
      container_concurrency = 80
      timeout_seconds       = 300
    }
    
    metadata {
      annotations = {
        "autoscaling.knative.dev/maxScale" = "10"
        "autoscaling.knative.dev/minScale" = "0"
      }
    }
  }
  
  traffic {
    percent         = 100
    latest_revision = true
  }
  
  depends_on = [
    google_project_service.required_apis
  ]
}

# Cloud Run Service - ML Service
resource "google_cloud_run_service" "ml_service" {
  name     = "ml-service"
  location = var.gcp_region
  
  template {
    spec {
      containers {
        image = "${var.docker_registry}/${var.docker_username}/ml-service:latest"
        
        ports {
          container_port = 8081
        }
        
        env {
          name  = "MODEL_PATH"
          value = "/app/artifacts/model.pkl"
        }
        
        resources {
          limits = {
            cpu    = "1"
            memory = "1Gi"
          }
        }
      }
      
      container_concurrency = 80
      timeout_seconds       = 300
    }
    
    metadata {
      annotations = {
        "autoscaling.knative.dev/maxScale" = "10"
        "autoscaling.knative.dev/minScale" = "0"
      }
    }
  }
  
  traffic {
    percent         = 100
    latest_revision = true
  }
  
  depends_on = [google_project_service.required_apis]
}

# Cloud Run Service - User Service
resource "google_cloud_run_service" "user_service" {
  name     = "user-service"
  location = var.gcp_region
  
  template {
    spec {
      containers {
        image = "${var.docker_registry}/${var.docker_username}/user-service:latest"
        
        ports {
          container_port = 8082
        }
        
        resources {
          limits = {
            cpu    = "1"
            memory = "512Mi"
          }
        }
      }
      
      container_concurrency = 80
      timeout_seconds       = 300
    }
    
    metadata {
      annotations = {
        "autoscaling.knative.dev/maxScale" = "10"
        "autoscaling.knative.dev/minScale" = "0"
      }
    }
  }
  
  traffic {
    percent         = 100
    latest_revision = true
  }
  
  depends_on = [google_project_service.required_apis]
}

# Cloud Run Service - Notification Service
resource "google_cloud_run_service" "notification_service" {
  name     = "notification-service"
  location = var.gcp_region
  
  template {
    spec {
      containers {
        image = "${var.docker_registry}/${var.docker_username}/notification-service:latest"
        
        ports {
          container_port = 8083
        }
        
        resources {
          limits = {
            cpu    = "1"
            memory = "512Mi"
          }
        }
      }
      
      container_concurrency = 80
      timeout_seconds       = 300
    }
    
    metadata {
      annotations = {
        "autoscaling.knative.dev/maxScale" = "10"
        "autoscaling.knative.dev/minScale" = "0"
      }
    }
  }
  
  traffic {
    percent         = 100
    latest_revision = true
  }
  
  depends_on = [google_project_service.required_apis]
}

# IAM policy to allow unauthenticated access (optional - remove for production)
resource "google_cloud_run_service_iam_member" "api_gateway_public" {
  service  = google_cloud_run_service.api_gateway.name
  location = google_cloud_run_service.api_gateway.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

resource "google_cloud_run_service_iam_member" "ml_service_public" {
  service  = google_cloud_run_service.ml_service.name
  location = google_cloud_run_service.ml_service.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

resource "google_cloud_run_service_iam_member" "user_service_public" {
  service  = google_cloud_run_service.user_service.name
  location = google_cloud_run_service.user_service.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

resource "google_cloud_run_service_iam_member" "notification_service_public" {
  service  = google_cloud_run_service.notification_service.name
  location = google_cloud_run_service.notification_service.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Outputs
output "api_gateway_url" {
  value       = google_cloud_run_service.api_gateway.status[0].url
  description = "URL of the API Gateway service"
}

output "ml_service_url" {
  value       = google_cloud_run_service.ml_service.status[0].url
  description = "URL of the ML Service"
}

output "user_service_url" {
  value       = google_cloud_run_service.user_service.status[0].url
  description = "URL of the User Service"
}

output "notification_service_url" {
  value       = google_cloud_run_service.notification_service.status[0].url
  description = "URL of the Notification Service"
}

