"""
Prometheus metrics for monitoring the ML inference service.
"""

from prometheus_client import Counter, Histogram, generate_latest
from prometheus_client.openmetrics.exposition import CONTENT_TYPE_LATEST

# Request counter
request_count = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status"]
)

# Request latency histogram
request_latency = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"]
)

# Prediction counter
prediction_count = Counter(
    "predictions_total",
    "Total number of predictions made"
)

# Prediction errors counter
prediction_errors = Counter(
    "prediction_errors_total",
    "Total number of prediction errors"
)

def get_metrics():
    """Return Prometheus metrics in text format."""
    return generate_latest()

