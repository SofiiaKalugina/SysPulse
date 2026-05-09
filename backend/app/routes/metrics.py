from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.machine import Machine
from app.models.metric import Metric
from app.schemas.metric_schema import MetricCreate, MetricResponse
from app.services.alert_service import check_metric_alerts

router = APIRouter(
    prefix="/api/metrics",
    tags=["metrics"],
)


@router.post("")
def receive_metrics(
    metric_data: MetricCreate,
    db: Session = Depends(get_db),
) -> dict:
    machine = (
        db.query(Machine)
        .filter(Machine.hostname == metric_data.hostname)
        .first()
    )

    if machine is None:
        machine = Machine(
            hostname=metric_data.hostname,
            os_name=metric_data.os_name,
            os_version=metric_data.os_version,
            last_seen_at=datetime.now(timezone.utc),
        )
        db.add(machine)
        db.commit()
        db.refresh(machine)
    else:
        machine.os_name = metric_data.os_name
        machine.os_version = metric_data.os_version
        machine.last_seen_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(machine)

    metric = Metric(
        machine_id=machine.id,
        **metric_data.model_dump(),
    )

    db.add(metric)
    db.commit()
    db.refresh(metric)

    alert_result = check_metric_alerts(db, machine, metric)

    return {
     "status": "received",
     "hostname": metric.hostname,
     "machine_id": machine.id,
    "received_at": datetime.now(timezone.utc).isoformat(),     "metric_id": metric.id,
     "alerts_created": alert_result["alerts_created"],
     "alerts_resolved": alert_result["alerts_resolved"],
}
    


@router.get("/latest", response_model=MetricResponse | dict)
def get_latest_metric(
    db: Session = Depends(get_db),
):
    latest_metric = (
        db.query(Metric)
        .order_by(Metric.id.desc())
        .first()
    )

    if latest_metric is None:
        return {
            "status": "empty",
            "message": "No metrics received yet.",
        }

    return latest_metric


@router.get("/history", response_model=List[MetricResponse])
def get_metrics_history(
    limit: int = 20,
    db: Session = Depends(get_db),
):
    metrics = (
        db.query(Metric)
        .order_by(Metric.id.desc())
        .limit(limit)
        .all()
    )

    return metrics