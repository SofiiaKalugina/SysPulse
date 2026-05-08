from pydantic import BaseModel, Field


class MetricCreate(BaseModel):
    hostname: str = Field(..., min_length=1)
    os_name: str
    os_version: str
    timestamp: str

    cpu_percent: float = Field(..., ge=0, le=100)

    ram_total: int = Field(..., ge=0)
    ram_used: int = Field(..., ge=0)
    ram_percent: float = Field(..., ge=0, le=100)

    disk_total: int = Field(..., ge=0)
    disk_used: int = Field(..., ge=0)
    disk_percent: float = Field(..., ge=0, le=100)

    process_count: int = Field(..., ge=0)

    network_sent: int = Field(..., ge=0)
    network_received: int = Field(..., ge=0)

    uptime_seconds: int = Field(..., ge=0)


class MetricResponse(MetricCreate):
    id: int

    class Config:
        from_attributes = True