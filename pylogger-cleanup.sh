#!/usr/bin/env bash
set -euo pipefail

LOG_DIR="{{log_dir}}"
DAYS_KEPT=14

if [[ ! -d "$LOG_DIR" ]]; then
    echo "Log directory not found: $LOG_DIR" >&2
    exit 1
fi

find "$LOG_DIR" \
    -type f \
    -name "*metrics.csv" \
    -mtime +"$DAYS_KEPT" \
    -print \
    -delete
