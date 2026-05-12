from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models.base import Alert, Machine, Metric
from app.routes.alert_analytics import router as alert_analytics_router
from app.routes.alerts import router as alerts_router
from app.routes.incidents import router as incidents_router
from app.routes.machines import router as machines_router
from app.routes.metrics import router as metrics_router
from app.routes.summary import router as summary_router
from app.routes.export import router as export_router

_ = (Alert, Machine, Metric)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SysPulse API",
    description="Backend API for SysPulse monitoring platform",
    version="0.7.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(metrics_router)
app.include_router(machines_router)
app.include_router(alerts_router)
app.include_router(alert_analytics_router)
app.include_router(incidents_router)
app.include_router(summary_router)
app.include_router(export_router)


@app.get("/health")
def health_check() -> dict:
    return {
        "status": "ok",
        "service": "syspulse-backend",
        "version": "0.7.0",
    }