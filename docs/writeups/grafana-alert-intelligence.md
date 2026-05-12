# SysPulse Alert Intelligence: Observability Prototype

## Overview

SysPulse is a small system monitoring platform built with a local Python agent, FastAPI backend, SQLite database, alert logic and a web dashboard.

This writeup focuses on the Alert Intelligence extension: a prototype feature that explores alert context, alert noise and incident summaries in observability systems.

## Why I Built This

Monitoring tools are most useful when alerts are actionable.

A basic alert can tell an engineer that something is wrong, but it often does not explain enough context:

- how often the issue happens
- whether the alert is active or already resolved
- which machine is the noisiest
- which metric causes the most alerts
- what the current system state looks like

I built this extension to explore how a monitoring system can make alerts easier to understand.

## What Alert Intelligence Does

The Alert Intelligence extension adds:

- alert analytics
- active vs resolved alert counts
- alert grouping by metric
- most common alert type
- noisy machine detection
- incident summary generation
- Prometheus-style metrics export

## API Endpoints

### Alert Analytics

```text
GET /api/alerts/analytics
```

Example response:

```json
{
  "total_alerts": 4,
  "active_alerts": 1,
  "resolved_alerts": 3,
  "alerts_by_metric": {
    "cpu_percent": 2,
    "ram_percent": 1,
    "disk_percent": 1
  },
  "most_common_alert": "cpu_percent",
  "noisy_machine": "local-workstation"
}
```

### Incident Summary

```text
GET /api/incidents/summary
```

Example response:

```json
{
  "summary": "1 out of 1 registered machine(s) are currently online. There are no active alerts at the moment. The latest metric sample shows CPU at 13.5%, RAM at 72.9% and disk usage at 72.4%."
}
```

### Prometheus-style Export

```text
GET /api/export/prometheus
```

Example output:

```text
# HELP syspulse_cpu_percent Current CPU usage percentage.
# TYPE syspulse_cpu_percent gauge
syspulse_cpu_percent{hostname="local-workstation"} 13.5

# HELP syspulse_ram_percent Current RAM usage percentage.
# TYPE syspulse_ram_percent gauge
syspulse_ram_percent{hostname="local-workstation"} 72.9
```

## Dashboard

The dashboard includes an Alert Intelligence section that displays:

- total alerts
- active alerts
- resolved alerts
- most common alert
- noisy machine
- incident summary

This makes the monitoring data easier to understand without opening raw API responses.

## What I Learned

While building this extension, I practiced:

- API design
- backend analytics
- alert lifecycle logic
- metrics formatting
- observability concepts
- dashboard integration
- automated testing

## Future Improvements

Possible next improvements:

- configurable alert rules
- anomaly detection
- alert severity scoring
- CSV export
- PostgreSQL support
- OpenTelemetry-compatible export
- integration with external notification channels
- real Grafana dashboard integration

## Why This Matters

This prototype explores a common observability problem: alerts should not only notify engineers, but also provide useful context.

The goal is not to replace existing observability platforms, but to learn how monitoring systems can reduce noise and make incidents easier to understand.