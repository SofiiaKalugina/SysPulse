from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.models.machine import Machine
from app.models.metric import Metric


ALERT_RULES = [
    {
        "metric_name": "cpu_percent",
        "threshold": 80.0,
        "severity": "high",
        "message": "CPU usage is above 80%",
    },
    {
        "metric_name": "ram_percent",
        "threshold": 85.0,
        "severity": "high",
        "message": "RAM usage is above 85%",
    },
    {
        "metric_name": "disk_percent",
        "threshold": 90.0,
        "severity": "critical",
        "message": "Disk usage is above 90%",
    },
]


def active_alert_exists(
    db: Session,
    machine_id: int,
    metric_name: str,
) -> bool:
    alert = (
        db.query(Alert)
        .filter(
            Alert.machine_id == machine_id,
            Alert.metric_name == metric_name,
            Alert.status == "active",
        )
        .first()
    )

    return alert is not None


def check_metric_alerts(
    db: Session,
    machine: Machine,
    metric: Metric,
) -> int:
    alerts_created = 0

    for rule in ALERT_RULES:
        metric_name = rule["metric_name"]
        metric_value = getattr(metric, metric_name)

        if metric_value <= rule["threshold"]:
            continue

        if active_alert_exists(db, machine.id, metric_name):
            continue

        alert = Alert(
            machine_id=machine.id,
            severity=rule["severity"],
            metric_name=metric_name,
            metric_value=metric_value,
            threshold=rule["threshold"],
            message=rule["message"],
            status="active",
        )

        db.add(alert)
        alerts_created += 1

    db.commit()

    return alerts_created