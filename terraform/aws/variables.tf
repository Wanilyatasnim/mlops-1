variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "us-east-1"
}

variable "docker_registry" {
  description = "Docker registry URL (e.g., docker.io, ECR URL)"
  type        = string
  default     = "docker.io"
}

variable "docker_username" {
  description = "Docker Hub username or ECR repository prefix"
  type        = string
}

