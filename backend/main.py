from fastapi import FastAPI

from app.database import Base, engine
from app.models.metric import Metric
from app.routes.metrics import router as metrics_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SysPulse API",
    description="Backend API for SysPulse monitoring platform",
    version="0.2.0",
)

app.include_router(metrics_router)


@app.get("/health")
def health_check() -> dict:
    return {
        "status": "ok",
        "service": "syspulse-backend",
        "version": "0.2.0",
    }