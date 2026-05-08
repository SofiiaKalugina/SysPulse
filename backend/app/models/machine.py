from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)

    hostname = Column(String, unique=True, index=True, nullable=False)
    os_name = Column(String, nullable=False)
    os_version = Column(String, nullable=False)
    agent_version = Column(String, default="0.1.0", nullable=False)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    last_seen_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    metrics = relationship("Metric", back_populates="machine")