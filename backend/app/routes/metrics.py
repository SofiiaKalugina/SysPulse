from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.metric import Metric
from app.schemas.metric_schema import MetricCreate, MetricResponse

router = APIRouter(
    prefix="/api/metrics",
    tags=["metrics"],
)


@router.post("")
def receive_metrics(
    metric_data: MetricCreate,
    db: Session = Depends(get_db),
) -> dict:
    metric = Metric(**metric_data.model_dump())

    db.add(metric)
    db.commit()
    db.refresh(metric)

    return {
        "status": "received",
        "hostname": metric.hostname,
        "received_at": datetime.utcnow().isoformat(),
        "metric_id": metric.id,
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