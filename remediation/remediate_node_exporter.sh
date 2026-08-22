#!/bin/bash

SERVICE="node_exporter"
LOG="/var/log/sre-remediation.log"

echo "$(date '+%Y-%m-%d %H:%M:%S') - Checking $SERVICE" >> "$LOG"

if ! systemctl is-active --quiet "$SERVICE"; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $SERVICE is DOWN. Restarting..." >> "$LOG"

    systemctl restart "$SERVICE"

    if systemctl is-active --quiet "$SERVICE"; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') - $SERVICE successfully recovered." >> "$LOG"
    else
        echo "$(date '+%Y-%m-%d %H:%M:%S') - ERROR: $SERVICE failed to recover." >> "$LOG"
    fi
fi
