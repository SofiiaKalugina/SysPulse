from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.machine import Machine
from app.schemas.machine_schema import MachineResponse

router = APIRouter(
    prefix="/api/machines",
    tags=["machines"],
)


@router.get("", response_model=List[MachineResponse])
def get_machines(
    db: Session = Depends(get_db),
):
    machines = (
        db.query(Machine)
        .order_by(Machine.last_seen_at.desc())
        .all()
    )

    return machines