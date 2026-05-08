from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(Integer, ForeignKey("machines.id"), nullable=False)

    hostname = Column(String, index=True, nullable=False)
    os_name = Column(String, nullable=False)
    os_version = Column(String, nullable=False)
    timestamp = Column(String, nullable=False)

    cpu_percent = Column(Float, nullable=False)

    ram_total = Column(Integer, nullable=False)
    ram_used = Column(Integer, nullable=False)
    ram_percent = Column(Float, nullable=False)

    disk_total = Column(Integer, nullable=False)
    disk_used = Column(Integer, nullable=False)
    disk_percent = Column(Float, nullable=False)

    process_count = Column(Integer, nullable=False)

    network_sent = Column(Integer, nullable=False)
    network_received = Column(Integer, nullable=False)

    uptime_seconds = Column(Integer, nullable=False)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    machine = relationship("Machine", back_populates="metrics")