from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.alert import Alert
from app.models.machine import Machine
from app.models.metric import Metric
from app.routes.machines import get_machine_status

router = APIRouter(
    prefix="/api/summary",
    tags=["summary"],
)


def average(values: list[float]) -> Optional[float]:
    if not values:
        return None

    return round(sum(values) / len(values), 1)


@router.get("")
def get_summary(
    db: Session = Depends(get_db),
) -> dict:
    machines = db.query(Machine).all()

    latest_metrics = (
        db.query(Metric)
        .order_by(Metric.id.desc())
        .limit(10)
        .all()
    )

    active_alerts_count = (
        db.query(Alert)
        .filter(Alert.status == "active")
        .count()
    )

    total_machines = len(machines)

    online_machines = sum(
        1 for machine in machines
        if get_machine_status(machine.last_seen_at) == "online"
    )

    avg_cpu = average([metric.cpu_percent for metric in latest_metrics])
    avg_ram = average([metric.ram_percent for metric in latest_metrics])
    avg_disk = average([metric.disk_percent for metric in latest_metrics])

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_machines": total_machines,
        "online_machines": online_machines,
        "offline_machines": total_machines - online_machines,
        "active_alerts": active_alerts_count,
        "avg_cpu": avg_cpu,
        "avg_ram": avg_ram,
        "avg_disk": avg_disk,
    }