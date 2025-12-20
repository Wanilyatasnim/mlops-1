terraform {
  required_version = ">= 1.0"
  
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
  zone    = var.gcp_zone
}

# Compute Instance for API Gateway
resource "google_compute_instance" "api_gateway" {
  name         = "api-gateway-vm"
  machine_type = "e2-medium"
  zone         = var.gcp_zone
  
  boot_disk {
    initialize_params {
      image = "cos-cloud/cos-stable"
    }
  }
  
  network_interface {
    network = "default"
    access_config {
      // Ephemeral public IP
    }
  }
  
  metadata = {
    docker-image = "${var.docker_registry}/${var.docker_username}/api-gateway:latest"
  }
  
  metadata_startup_script = <<-EOF
    #!/bin/bash
    docker pull ${var.docker_registry}/${var.docker_username}/api-gateway:latest
    docker run -d \
      --name api-gateway \
      --restart unless-stopped \
      -p 8080:8080 \
      -e ML_SERVICE_URL=http://${google_compute_instance.ml_service.network_interface[0].network_ip}:8081 \
      -e USER_SERVICE_URL=http://${google_compute_instance.user_service.network_interface[0].network_ip}:8082 \
      -e NOTIFICATION_SERVICE_URL=http://${google_compute_instance.notification_service.network_interface[0].network_ip}:8083 \
      ${var.docker_registry}/${var.docker_username}/api-gateway:latest
  EOF
  
  tags = ["mlops", "api-gateway"]
}

# Compute Instance for ML Service
resource "google_compute_instance" "ml_service" {
  name         = "ml-service-vm"
  machine_type = "e2-standard-2"
  zone         = var.gcp_zone
  
  boot_disk {
    initialize_params {
      image = "cos-cloud/cos-stable"
    }
  }
  
  network_interface {
    network = "default"
    access_config {
      // Ephemeral public IP
    }
  }
  
  metadata = {
    docker-image = "${var.docker_registry}/${var.docker_username}/ml-service:latest"
  }
  
  metadata_startup_script = <<-EOF
    #!/bin/bash
    docker pull ${var.docker_registry}/${var.docker_username}/ml-service:latest
    docker run -d \
      --name ml-service \
      --restart unless-stopped \
      -p 8081:8081 \
      -e MODEL_PATH=/app/artifacts/model.pkl \
      ${var.docker_registry}/${var.docker_username}/ml-service:latest
  EOF
  
  tags = ["mlops", "ml-service"]
}

# Compute Instance for User Service
resource "google_compute_instance" "user_service" {
  name         = "user-service-vm"
  machine_type = "e2-medium"
  zone         = var.gcp_zone
  
  boot_disk {
    initialize_params {
      image = "cos-cloud/cos-stable"
    }
  }
  
  network_interface {
    network = "default"
    access_config {
      // Ephemeral public IP
    }
  }
  
  metadata = {
    docker-image = "${var.docker_registry}/${var.docker_username}/user-service:latest"
  }
  
  metadata_startup_script = <<-EOF
    #!/bin/bash
    docker pull ${var.docker_registry}/${var.docker_username}/user-service:latest
    docker run -d \
      --name user-service \
      --restart unless-stopped \
      -p 8082:8082 \
      ${var.docker_registry}/${var.docker_username}/user-service:latest
  EOF
  
  tags = ["mlops", "user-service"]
}

# Compute Instance for Notification Service
resource "google_compute_instance" "notification_service" {
  name         = "notification-service-vm"
  machine_type = "e2-medium"
  zone         = var.gcp_zone
  
  boot_disk {
    initialize_params {
      image = "cos-cloud/cos-stable"
    }
  }
  
  network_interface {
    network = "default"
    access_config {
      // Ephemeral public IP
    }
  }
  
  metadata = {
    docker-image = "${var.docker_registry}/${var.docker_username}/notification-service:latest"
  }
  
  metadata_startup_script = <<-EOF
    #!/bin/bash
    docker pull ${var.docker_registry}/${var.docker_username}/notification-service:latest
    docker run -d \
      --name notification-service \
      --restart unless-stopped \
      -p 8083:8083 \
      ${var.docker_registry}/${var.docker_username}/notification-service:latest
  EOF
  
  tags = ["mlops", "notification-service"]
}

# Firewall Rules
resource "google_compute_firewall" "allow_http" {
  name    = "mlops-allow-http"
  network = "default"
  
  allow {
    protocol = "tcp"
    ports    = ["8080", "8081", "8082", "8083"]
  }
  
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["mlops"]
}

# Outputs
output "api_gateway_ip" {
  value       = google_compute_instance.api_gateway.network_interface[0].access_config[0].nat_ip
  description = "Public IP of API Gateway VM"
}

output "ml_service_ip" {
  value       = google_compute_instance.ml_service.network_interface[0].access_config[0].nat_ip
  description = "Public IP of ML Service VM"
}

output "user_service_ip" {
  value       = google_compute_instance.user_service.network_interface[0].access_config[0].nat_ip
  description = "Public IP of User Service VM"
}

output "notification_service_ip" {
  value       = google_compute_instance.notification_service.network_interface[0].access_config[0].nat_ip
  description = "Public IP of Notification Service VM"
}

