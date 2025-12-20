variable "gcp_project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "gcp_region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"
}

variable "gcp_zone" {
  description = "GCP Zone"
  type        = string
  default     = "us-central1-a"
}

variable "docker_registry" {
  description = "Docker registry URL"
  type        = string
  default     = "docker.io"
}

variable "docker_username" {
  description = "Docker Hub username"
  type        = string
}

