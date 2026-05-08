from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class MachineResponse(BaseModel):
    id: int
    hostname: str
    os_name: str
    os_version: str
    agent_version: str
    created_at: datetime
    last_seen_at: datetime
    status: Literal["online", "offline"]

    class Config:
        from_attributes = True