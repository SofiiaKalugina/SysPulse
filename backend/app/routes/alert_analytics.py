from collections import Counter
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.alert import Alert
from app.models.machine import Machine


router = APIRouter(
    prefix="/api/alerts/analytics",
    tags=["alert analytics"],
)


def get_most_common_alert(alerts: List[Alert]) -> Optional[str]:
    if not alerts:
        return None

    metric_counter = Counter(alert.metric_name for alert in alerts)
    return metric_counter.most_common(1)[0][0]


def get_alerts_by_metric(alerts: List[Alert]) -> Dict[str, int]:
    metric_counter = Counter(alert.metric_name for alert in alerts)
    return dict(metric_counter)


def get_noisy_machine(db: Session, alerts: List[Alert]) -> Optional[str]:
    if not alerts:
        return None

    machine_counter = Counter(alert.machine_id for alert in alerts)
    noisy_machine_id = machine_counter.most_common(1)[0][0]

    machine = (
        db.query(Machine)
        .filter(Machine.id == noisy_machine_id)
        .first()
    )

    if machine is None:
        return None

    return machine.hostname


@router.get("")
def get_alert_analytics(
    db: Session = Depends(get_db),
) -> dict:
    alerts = db.query(Alert).all()

    total_alerts = len(alerts)
    active_alerts = len([alert for alert in alerts if alert.status == "active"])
    resolved_alerts = len([alert for alert in alerts if alert.status == "resolved"])

    alerts_by_metric = get_alerts_by_metric(alerts)
    most_common_alert = get_most_common_alert(alerts)
    noisy_machine = get_noisy_machine(db, alerts)

    return {
        "total_alerts": total_alerts,
        "active_alerts": active_alerts,
        "resolved_alerts": resolved_alerts,
        "alerts_by_metric": alerts_by_metric,
        "most_common_alert": most_common_alert,
        "noisy_machine": noisy_machine,
    }