from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.machine import Machine

router = APIRouter(
    prefix="/api/machines",
    tags=["machines"],
)

ONLINE_THRESHOLD_SECONDS = 30


def get_machine_status(last_seen_at: datetime) -> str:
    now = datetime.now(timezone.utc)

    if last_seen_at.tzinfo is None:
        last_seen_at = last_seen_at.replace(tzinfo=timezone.utc)

    seconds_since_last_seen = (now - last_seen_at).total_seconds()

    if seconds_since_last_seen <= ONLINE_THRESHOLD_SECONDS:
        return "online"

    return "offline"


@router.get("")
def get_machines(
    db: Session = Depends(get_db),
) -> List[dict]:
    machines = (
        db.query(Machine)
        .order_by(Machine.last_seen_at.desc())
        .all()
    )

    return [
        {
            "id": machine.id,
            "hostname": machine.hostname,
            "os_name": machine.os_name,
            "os_version": machine.os_version,
            "agent_version": machine.agent_version,
            "created_at": machine.created_at,
            "last_seen_at": machine.last_seen_at,
            "status": get_machine_status(machine.last_seen_at),
        }
        for machine in machines
    ]