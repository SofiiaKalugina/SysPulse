from fastapi import FastAPI

app = FastAPI(
    title="SysPulse API",
    description="Backend API for SysPulse monitoring platform",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict:
    return {
        "status": "ok",
        "service": "syspulse-backend",
        "version": "0.1.0",
    }