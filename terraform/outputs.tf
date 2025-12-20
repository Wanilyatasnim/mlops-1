output "api_gateway_url" {
  description = "API Gateway service URL"
  value       = google_cloud_run_service.api_gateway.status[0].url
}

output "ml_service_url" {
  description = "ML Service URL"
  value       = google_cloud_run_service.ml_service.status[0].url
}

output "user_service_url" {
  description = "User Service URL"
  value       = google_cloud_run_service.user_service.status[0].url
}

