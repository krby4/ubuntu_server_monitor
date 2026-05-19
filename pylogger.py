import psutil
import csv
import os
from datetime import datetime

today = datetime.now().date().isoformat()

CSV_FILE = f"{{log_path}}/metrics_{today}.csv"

FIELDNAMES = [
    "timestamp",
    "cpu_percent",
    "mem_percent",
    "disk_percent",
    "bytes_recv"
]

# --- collect metrics ---

cpu = psutil.cpu_percent(interval=5)
mem = psutil.virtual_memory()
mem_percent = mem.percent
disk = psutil.disk_usage('/')
disk_percent = disk.percent
net = psutil.net_io_counters()
net_recv = net.bytes_recv

data = {
    "timestamp": datetime.now().isoformat(),
    "cpu_percent": cpu,
    "mem_percent": mem_percent,
    "disk_percent": disk_percent,
    "bytes_recv": net_recv
}

# --- write to CSV ---
file_exists = os.path.isfile(CSV_FILE)

with open(CSV_FILE, "a", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDNAMES)

    if not file_exists:
        writer.writeheader()

    writer.writerow(data)
