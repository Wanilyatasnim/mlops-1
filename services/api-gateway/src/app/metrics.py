"""
Prometheus metrics for monitoring the API Gateway.
"""

from prometheus_client import Counter, Histogram, generate_latest

request_count = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status"]
)

request_latency = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"]
)

def get_metrics():
    """Return Prometheus metrics in text format."""
    return generate_latest()

