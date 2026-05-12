from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.alert import Alert
from app.models.machine import Machine
from app.models.metric import Metric
from app.routes.machines import get_machine_status


router = APIRouter(
    prefix="/api/incidents",
    tags=["incidents"],
)


def get_most_common_alert_type(alerts: List[Alert]) -> Optional[str]:
    if not alerts:
        return None

    counts = {}

    for alert in alerts:
        counts[alert.metric_name] = counts.get(alert.metric_name, 0) + 1

    return max(counts, key=counts.get)


def build_incident_summary(
    machines: List[Machine],
    alerts: List[Alert],
    latest_metric: Optional[Metric],
) -> str:
    if not machines:
        return "No machines are currently registered. Start the agent to begin collecting system metrics."

    online_machines = [
        machine for machine in machines
        if get_machine_status(machine.last_seen_at) == "online"
    ]

    active_alerts = [
        alert for alert in alerts
        if alert.status == "active"
    ]

    critical_alerts = [
        alert for alert in active_alerts
        if alert.severity == "critical"
    ]

    most_common_alert = get_most_common_alert_type(alerts)

    summary_parts = []

    if online_machines:
        summary_parts.append(
            f"{len(online_machines)} out of {len(machines)} registered machine(s) are currently online."
        )
    else:
        summary_parts.append("No registered machines are currently online.")

    if active_alerts:
        summary_parts.append(f"There are {len(active_alerts)} active alert(s).")
    else:
        summary_parts.append("There are no active alerts at the moment.")

    if critical_alerts:
        summary_parts.append(
            f"{len(critical_alerts)} critical alert(s) require attention."
        )

    if most_common_alert:
        summary_parts.append(
            f"The most common alert type is {most_common_alert}."
        )

    if latest_metric:
        summary_parts.append(
            f"The latest metric sample shows CPU at {latest_metric.cpu_percent:.1f}%, "
            f"RAM at {latest_metric.ram_percent:.1f}% and disk usage at {latest_metric.disk_percent:.1f}%."
        )

    return " ".join(summary_parts)


@router.get("/summary")
def get_incident_summary(
    db: Session = Depends(get_db),
) -> dict:
    machines = db.query(Machine).all()
    alerts = db.query(Alert).all()

    latest_metric = (
        db.query(Metric)
        .order_by(Metric.id.desc())
        .first()
    )

    summary = build_incident_summary(
        machines=machines,
        alerts=alerts,
        latest_metric=latest_metric,
    )

    return {
        "summary": summary,
    }