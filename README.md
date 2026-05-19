# Monitoring Tool

A lightweight Python-based system monitoring utility that collects basic system metrics and stores them in daily CSV log files. Includes a Bash cleanup script for automatic log retention management.

This project is intended as a simple foundation for infrastructure monitoring, observability experiments, and autoscaling research environments.

---

## Features

- Collects:
  - CPU utilization
  - Memory usage
  - Disk usage
  - Network bytes received
- Writes metrics to daily CSV files
- Automatically creates CSV headers when needed
- Simple log cleanup utility
- Designed to run well with:
  - cron
  - systemd timers
  - containerized environments

---

## Project Structure

```text
project/
├── pylogger.py
├── pylogger-cleanup.sh
├── logs/
│   └── metrics_YYYY-MM-DD.csv
├── examples/
│   ├── monitor.service
│   ├── monitor.timer
│   ├── cleanup.service
│   └── cleanup.timer
└── README.md
```

---

## Requirements

- Python 3.9+
- `psutil`

Install dependencies:

```bash
pip install psutil
```

---

## Monitoring Script

The monitoring script collects metrics and appends them to a CSV file named by date.

Example output file:

```text
logs/metrics_2026-05-19.csv
```

Example CSV contents:

```csv
timestamp,cpu_percent,mem_percent,disk_percent,bytes_recv
2026-05-19T10:15:00,12.5,44.1,61.2,18273645
```

---

## Configuration

The script expects a log directory path:

```python
CSV_FILE = f"{log_path}/metrics_{today}.csv"
```

Replace:

```python
{log_path}
```

with your desired log directory.

Example:

```python
CSV_FILE = f"/var/log/system-monitor/metrics_{today}.csv"
```

---

## Running the Monitor

Run manually:

```bash
python3 monitor.py
```

The script samples CPU usage over a 5-second interval:

```python
psutil.cpu_percent(interval=5)
```

---

## Log Cleanup Script

The cleanup script removes metric CSV files older than 14 days.

Run manually:

```bash
./cleanup_logs.sh
```

Configuration:

```bash
LOG_DIR="/path/to/logs"
DAYS_KEPT=14
```

---

## Systemd Timer Support

The `examples/` directory includes example files for:

- `monitor.service`
- `monitor.timer`
- `cleanup.service`
- `cleanup.timer`

These can be used to:

- schedule periodic metric collection
- automate log retention cleanup
- run monitoring in the background without cron

Example usage:

```bash
sudo cp examples/*.service /etc/systemd/system/
sudo cp examples/*.timer /etc/systemd/system/

sudo systemctl daemon-reload

sudo systemctl enable --now monitor.timer
sudo systemctl enable --now cleanup.timer
```

Check timer status:

```bash
systemctl list-timers
```

---

## Suggested Timer Intervals

Recommended defaults:

| Task | Interval |
|---|---|
| Monitoring | Every 5 minutes |
| Cleanup | Once per day |

---

## Future Improvements

Potential enhancements include:

- Request latency tracking
- Per-core CPU metrics
- Disk I/O statistics
- Network transmit metrics
- PostgreSQL storage backend
- Docker/container metrics
- Threshold-based alerting
- Prometheus/OpenTelemetry integration
- Autoscaling signal generation

---