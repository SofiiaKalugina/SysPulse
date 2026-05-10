import importlib
import sys
from pathlib import Path

from fastapi.testclient import TestClient


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

app_module = importlib.import_module("main")
client = TestClient(app_module.app)


def sample_metric_payload() -> dict:
    return {
        "hostname": "test-machine",
        "os_name": "Windows",
        "os_version": "10.0",
        "timestamp": "2026-05-09T16:00:00+00:00",
        "cpu_percent": 12.5,
        "ram_total": 16000000000,
        "ram_used": 8000000000,
        "ram_percent": 50.0,
        "disk_total": 500000000000,
        "disk_used": 250000000000,
        "disk_percent": 50.0,
        "process_count": 150,
        "network_sent": 1000,
        "network_received": 2000,
        "uptime_seconds": 3600,
    }


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "syspulse-backend"


def test_receive_metrics():
    response = client.post("/api/metrics", json=sample_metric_payload())

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "received"
    assert data["hostname"] == "test-machine"
    assert "metric_id" in data
    assert "machine_id" in data


def test_latest_metric():
    client.post("/api/metrics", json=sample_metric_payload())

    response = client.get("/api/metrics/latest")

    assert response.status_code == 200

    data = response.json()

    assert data["hostname"] == "test-machine"
    assert data["cpu_percent"] == 12.5
    assert "machine_id" in data


def test_metrics_history():
    client.post("/api/metrics", json=sample_metric_payload())

    response = client.get("/api/metrics/history?limit=5")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1


def test_machines_endpoint():
    client.post("/api/metrics", json=sample_metric_payload())

    response = client.get("/api/machines")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1
    assert "hostname" in data[0]
    assert "status" in data[0]


def test_alerts_endpoint():
    response = client.get("/api/alerts")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_summary_endpoint():
    client.post("/api/metrics", json=sample_metric_payload())

    response = client.get("/api/summary")

    assert response.status_code == 200

    data = response.json()

    assert "total_machines" in data
    assert "online_machines" in data
    assert "active_alerts" in data
    assert "avg_cpu" in data
    assert "avg_ram" in data
    assert "avg_disk" in data