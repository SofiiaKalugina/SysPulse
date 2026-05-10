from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.alert import Alert
from app.schemas.alert_schema import AlertResponse

router = APIRouter(
    prefix="/api/alerts",
    tags=["alerts"],
)


@router.get("", response_model=List[AlertResponse])
def get_alerts(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
) -> List[Alert]:
    query = db.query(Alert).order_by(Alert.created_at.desc())

    if status is not None:
        query = query.filter(Alert.status == status)

    return query.all()