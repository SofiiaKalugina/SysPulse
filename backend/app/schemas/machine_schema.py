from datetime import datetime

from pydantic import BaseModel


class MachineResponse(BaseModel):
    id: int
    hostname: str
    os_name: str
    os_version: str
    agent_version: str
    created_at: datetime
    last_seen_at: datetime

    class Config:
        from_attributes = True