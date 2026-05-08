import platform
import socket
import time
from datetime import datetime, timezone

import psutil


def collect_system_metrics() -> dict:
    """
    Collect basic system metrics from the current machine.
    Returns data as a dictionary ready to be converted to JSON.
    """

    disk = psutil.disk_usage("/")
    memory = psutil.virtual_memory()
    network = psutil.net_io_counters()

    boot_time = psutil.boot_time()
    uptime_seconds = int(time.time() - boot_time)

    metrics = {
        "hostname": socket.gethostname(),
        "os_name": platform.system(),
        "os_version": platform.version(),
        "timestamp": datetime.now(timezone.utc).isoformat(),

        "cpu_percent": psutil.cpu_percent(interval=1),
        "ram_total": memory.total,
        "ram_used": memory.used,
        "ram_percent": memory.percent,

        "disk_total": disk.total,
        "disk_used": disk.used,
        "disk_percent": disk.percent,

        "process_count": len(psutil.pids()),

        "network_sent": network.bytes_sent,
        "network_received": network.bytes_recv,

        "uptime_seconds": uptime_seconds,
    }

    return metrics