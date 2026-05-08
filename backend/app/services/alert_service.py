from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.models.machine import Machine
from app.models.metric import Metric


ALERT_RULES = [
    {
        "metric_name": "cpu_percent",
        "threshold": 80.0,
        "resolve_threshold": 70.0,
        "severity": "high",
        "message": "CPU usage is above 80%",
    },
    {
        "metric_name": "ram_percent",
        "threshold": 85.0,
        "resolve_threshold": 75.0,
        "severity": "high",
        "message": "RAM usage is above 85%",
    },
    {
        "metric_name": "disk_percent",
        "threshold": 90.0,
        "resolve_threshold": 85.0,
        "severity": "critical",
        "message": "Disk usage is above 90%",
    },
]


def get_active_alert(
    db: Session,
    machine_id: int,
    metric_name: str,
) -> Alert | None:
    return (
        db.query(Alert)
        .filter(
            Alert.machine_id == machine_id,
            Alert.metric_name == metric_name,
            Alert.status == "active",
        )
        .first()
    )


def create_alert_if_needed(
    db: Session,
    machine: Machine,
    metric: Metric,
    rule: dict,
) -> int:
    metric_name = rule["metric_name"]
    metric_value = getattr(metric, metric_name)

    if metric_value <= rule["threshold"]:
        return 0

    existing_alert = get_active_alert(db, machine.id, metric_name)

    if existing_alert is not None:
        return 0

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
    return 1


def resolve_alert_if_needed(
    db: Session,
    machine: Machine,
    metric: Metric,
    rule: dict,
) -> int:
    metric_name = rule["metric_name"]
    metric_value = getattr(metric, metric_name)

    active_alert = get_active_alert(db, machine.id, metric_name)

    if active_alert is None:
        return 0

    if metric_value >= rule["resolve_threshold"]:
        return 0

    active_alert.status = "resolved"
    active_alert.resolved_at = datetime.now(timezone.utc)

    return 1


def check_metric_alerts(
    db: Session,
    machine: Machine,
    metric: Metric,
) -> dict:
    alerts_created = 0
    alerts_resolved = 0

    for rule in ALERT_RULES:
        alerts_created += create_alert_if_needed(db, machine, metric, rule)
        alerts_resolved += resolve_alert_if_needed(db, machine, metric, rule)

    db.commit()

    return {
        "alerts_created": alerts_created,
        "alerts_resolved": alerts_resolved,
    }