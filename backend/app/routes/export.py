from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.metric import Metric


router = APIRouter(
    prefix="/api/export",
    tags=["export"],
)


def format_prometheus_metric(
    metric_name: str,
    hostname: str,
    value: float,
) -> str:
    safe_hostname = hostname.replace('"', '\\"')

    return f'{metric_name}{{hostname="{safe_hostname}"}} {value}'


@router.get("/prometheus")
def export_prometheus_metrics(
    db: Session = Depends(get_db),
) -> Response:
    latest_metric = (
        db.query(Metric)
        .order_by(Metric.id.desc())
        .first()
    )

    if latest_metric is None:
        content = "# No SysPulse metrics available yet\n"

        return Response(
            content=content,
            media_type="text/plain",
        )

    lines = [
        "# HELP syspulse_cpu_percent Current CPU usage percentage.",
        "# TYPE syspulse_cpu_percent gauge",
        format_prometheus_metric(
            "syspulse_cpu_percent",
            latest_metric.hostname,
            latest_metric.cpu_percent,
        ),
        "",
        "# HELP syspulse_ram_percent Current RAM usage percentage.",
        "# TYPE syspulse_ram_percent gauge",
        format_prometheus_metric(
            "syspulse_ram_percent",
            latest_metric.hostname,
            latest_metric.ram_percent,
        ),
        "",
        "# HELP syspulse_disk_percent Current disk usage percentage.",
        "# TYPE syspulse_disk_percent gauge",
        format_prometheus_metric(
            "syspulse_disk_percent",
            latest_metric.hostname,
            latest_metric.disk_percent,
        ),
        "",
        "# HELP syspulse_process_count Current number of running processes.",
        "# TYPE syspulse_process_count gauge",
        format_prometheus_metric(
            "syspulse_process_count",
            latest_metric.hostname,
            latest_metric.process_count,
        ),
    ]

    content = "\n".join(lines) + "\n"

    return Response(
        content=content,
        media_type="text/plain",
    )