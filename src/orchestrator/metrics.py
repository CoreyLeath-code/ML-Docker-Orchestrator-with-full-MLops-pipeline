from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

REQUESTS = Counter("http_requests_total", "Total HTTP requests", ["path", "method", "status"])
LATENCY = Histogram("http_request_latency_seconds", "Request latency", ["path", "method"])


def metrics_response():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}
