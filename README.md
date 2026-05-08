# SysPulse

SysPulse is a Linux system monitoring platform.

It includes:

- Python agent for collecting CPU, RAM, disk, process and network metrics
- FastAPI backend for receiving and storing metrics
- PostgreSQL database for historical monitoring data
- Alert system for detecting high CPU/RAM/disk usage
- Web dashboard for viewing machines, metrics and alerts

## Project Structure

```text
syspulse/
├── agent/
├── backend/
├── dashboard/
├── docker-compose.yml
└── README.md
