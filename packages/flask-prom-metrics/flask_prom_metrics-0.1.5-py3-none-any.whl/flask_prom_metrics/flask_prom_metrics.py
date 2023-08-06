from flask import request

from prometheus_client import (
    Counter,
    Histogram,
)

import time
import os

APP = "server" if os.getenv("APP") is None else os.getenv("APP")

service_request_amount = Counter(
    "service_request_amount",
    "Amount of received requests",
    ["app"],
)
service_response_amount = Counter(
    "service_response_amount",
    "Amount of request responses",
    ["app", "status"],
)
service_request_latency_seconds = Histogram(
    "service_request_latency_seconds",
    "Oberseve request latency in seconds",
    ["app", "status"],
    buckets=[0.01, 0.05, 0.1, 0.2, 0.4, 1, 3, 5, 8],
)
service_failed_request_latency_seconds = Histogram(
    "service_failed_request_latency_seconds",
    "Oberseve failed request latency in seconds",
    ["app", "status"],
    buckets=[0.01, 0.05, 0.1, 0.2, 0.4, 1, 3, 5, 8],
)


def start_request():
    service_request_amount.labels(app=APP).inc()
    request._prometheus_metrics_request_start_time = time.time()


def end_request(response):
    latency = time.time() - request._prometheus_metrics_request_start_time

    if response.status_code > 302:
        service_failed_request_latency_seconds.labels(
            app=APP, status=response.status_code
        ).observe(latency)
    else:
        service_request_latency_seconds.labels(
            app=APP, status=response.status_code
        ).observe(latency)

    service_response_amount.labels(app=APP, status=response.status_code).inc()
    return response
