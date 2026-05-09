from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AlertResponse(BaseModel):
    id: int
    machine_id: int
    severity: str
    metric_name: str
    metric_value: float
    threshold: float
    message: str
    status: str
    created_at: datetime
    resolved_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)