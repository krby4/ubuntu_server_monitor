#!/usr/bin/env python3
import argparse
import psutil
import subprocess
import csv
import os
from datetime import datetime

def parse_args():
    parser = argparse.ArgumentParser(description="Basically only gathers the log-path")
    parser.add_argument("-l","--log-path",help="Directory path to where you want the logs",required=True)
    return parser.parse_args()

def collect_baremetal_stats(CSV_FILE):
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
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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

def collect_docker_stats(CSV_FILE):
    FIELDNAMES = [
        "timestamp",
        "container_id",
        "container_name",
        "cpu_percent",
        "mem_usage/limit"
    ]

    file_exists = os.path.isfile(CSV_FILE)
    stats = (subprocess.run(["docker","stats","--no-stream","--format","{{.Container}},{{.Name}},{{.CPUPerc}},{{.MemUsage}}"],capture_output=True,text=True)).stdout
    print(stats)
    lines = stats.strip().splitlines()
    print(lines)
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)

        if not file_exists:
            writer.writeheader()
        for line in lines:
            if not line.strip():
                continue
            parts = line.split(",")
            data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "container_id": parts[0],
                "container_name": parts[1],
                "cpu_percent": parts[2],
                "mem_usage/limit": parts[3]
            }
            writer.writerow(data)

def main():
    args = parse_args()
    log_path = args.log_path
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    today = datetime.now().date().isoformat()
    BAREMETAL_CSV_FILE = f"{log_path}/{today}_baremetal_metrics.csv"
    DOCKER_CSV_FILE = f"{log_path}/{today}_docker_metrics.csv"
    collect_baremetal_stats(BAREMETAL_CSV_FILE)
    collect_docker_stats(DOCKER_CSV_FILE)

if __name__ == "__main__":
    main()
