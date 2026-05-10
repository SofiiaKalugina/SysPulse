# SysPulse

SysPulse is a system monitoring platform that collects machine metrics through a local Python agent and displays them in a web dashboard.

The project demonstrates backend development, API design, database storage, alert logic, testing, CI, and a simple monitoring dashboard.

## Features

- Python agent for collecting system metrics
- CPU, RAM, disk, process, network, and uptime monitoring
- FastAPI backend
- SQLite database storage
- Machine tracking by hostname
- Online/offline machine status
- Metrics history
- Alert system for high CPU, RAM, and disk usage
- Auto-resolving alerts
- Summary API
- Web dashboard
- Backend API tests with pytest
- GitHub Actions CI

## Architecture

```text
Local Machine
    |
    | Python Agent
    | collects system metrics
    v
FastAPI Backend
    |
    | validates and stores data
    v
SQLite Database
    |
    v
Dashboard / API / Alerts
```

## Tech Stack

### Agent

- Python
- psutil
- requests
- python-dotenv

### Backend

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- pytest
- httpx

### Dashboard

- HTML
- CSS
- JavaScript

### DevOps

- Git
- GitHub
- GitHub Actions

## Project Structure

```text
syspulse/
├── agent/
│   ├── collector.py
│   ├── config.py
│   ├── main.py
│   ├── sender.py
│   └── requirements.txt
│
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── database.py
│   ├── tests/
│   ├── main.py
│   └── requirements.txt
│
├── dashboard/
│   ├── index.html
│   ├── styles.css
│   └── app.js
│
├── .github/
│   └── workflows/
│       └── backend-tests.yml
│
└── README.md
```

## How It Works

1. The agent runs on a machine and collects system metrics.
2. The agent sends metrics to the backend through HTTP.
3. The backend validates the data and stores it in the database.
4. The backend creates or updates the machine record.
5. The alert system checks CPU, RAM, and disk usage.
6. The dashboard fetches data from the backend and displays machine status, metrics, alerts, and history.

## Running the Backend

Open a terminal:

```bash
cd backend
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

The backend runs at:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## Running the Agent

Open a second terminal:

```bash
cd agent
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python main.py
```

The agent collects metrics every few seconds and sends them to the backend.

## Opening the Dashboard

Open this file in a browser:

```text
dashboard/index.html
```

On Windows, the full local URL may look like:

```text
file:///C:/Users/your-user/Desktop/syspulse/dashboard/index.html
```

## API Endpoints

### Health

```text
GET /health
```

### Metrics

```text
POST /api/metrics
GET /api/metrics/latest
GET /api/metrics/history
```

### Machines

```text
GET /api/machines
```

### Alerts

```text
GET /api/alerts
```

### Summary

```text
GET /api/summary
```

## Alert Rules

Current alert rules:

```text
CPU > 80%  -> high alert
RAM > 85%  -> high alert
Disk > 90% -> critical alert
```

Auto-resolve logic:

```text
CPU < 70%  -> resolve CPU alert
RAM < 75%  -> resolve RAM alert
Disk < 85% -> resolve disk alert
```

## Running Tests

From the backend folder:

```bash
cd backend
source venv/Scripts/activate
pytest
```

Expected result:

```text
7 passed
```

## CI

GitHub Actions runs backend tests automatically on every push and pull request to the main branch.

## Current Status

Implemented:

- Agent metrics collection
- Backend API
- Database storage
- Machines tracking
- Online/offline status
- Metrics history
- Alert system
- Auto-resolve alerts
- Dashboard
- Summary API
- Backend tests
- GitHub Actions CI

Planned improvements:

- Better dashboard design
- PostgreSQL support
- Docker setup
- Authentication
- CSV export
- Email notifications
- More detailed charts