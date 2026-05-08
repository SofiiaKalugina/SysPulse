from datetime import datetime
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(
    title="SysPulse API",
    description="Backend API for SysPulse monitoring platform",
    version="0.1.0",
)


class MetricCreate(BaseModel):
    hostname: str = Field(..., min_length=1)
    os_name: str
    os_version: str
    timestamp: str

    cpu_percent: float = Field(..., ge=0, le=100)
    ram_total: int = Field(..., ge=0)
    ram_used: int = Field(..., ge=0)
    ram_percent: float = Field(..., ge=0, le=100)

    disk_total: int = Field(..., ge=0)
    disk_used: int = Field(..., ge=0)
    disk_percent: float = Field(..., ge=0, le=100)

    process_count: int = Field(..., ge=0)

    network_sent: int = Field(..., ge=0)
    network_received: int = Field(..., ge=0)

    uptime_seconds: int = Field(..., ge=0)


metrics_storage: List[MetricCreate] = []


@app.get("/health")
def health_check() -> dict:
    return {
        "status": "ok",
        "service": "syspulse-backend",
        "version": "0.1.0",
    }


@app.post("/api/metrics")
def receive_metrics(metric: MetricCreate) -> dict:
    metrics_storage.append(metric)

    return {
        "status": "received",
        "hostname": metric.hostname,
        "received_at": datetime.utcnow().isoformat(),
        "stored_metrics_count": len(metrics_storage),
    }


@app.get("/api/metrics/latest")
def get_latest_metric() -> dict:
    if not metrics_storage:
        return {
            "status": "empty",
            "message": "No metrics received yet.",
        }

    latest_metric = metrics_storage[-1]

    return {
        "status": "ok",
        "metric": latest_metric,
    }