#!/usr/bin/env bash
# One-shot health check for an always-on Hermes box.
# Exit 0 = healthy, 1 = attention needed. Prints one line per check.
set -uo pipefail
status=0

# 1. Hermes service liveness (systemd)
SERVICE="${HERMES_SERVICE:-hermes}"
if command -v systemctl >/dev/null 2>&1; then
  if systemctl is-active --quiet "$SERVICE"; then
    echo "OK   service $SERVICE active"
  else
    echo "FAIL service $SERVICE not active"; status=1
  fi
fi

# 2. Disk usage on the data volume
DISK_PATH="${HERMES_HOME:-/}"
use="$(df -P "$DISK_PATH" 2>/dev/null | awk 'NR==2 {gsub("%","",$5); print $5}')"
if [ "${use:-100}" -lt 90 ]; then
  echo "OK   disk ${use}% used ($DISK_PATH)"
else
  echo "WARN disk ${use:-?}% used ($DISK_PATH)"; status=1
fi

# 3. Backup freshness
if [ -n "${BACKUP_DIR:-}" ]; then
  latest="$(ls -1t "$BACKUP_DIR"/hermes-*.tar.gz.age 2>/dev/null | head -n1 || true)"
  if [ -n "$latest" ]; then
    age_h=$(( ( $(date +%s) - $(date -r "$latest" +%s) ) / 3600 ))
    max="${MAX_BACKUP_AGE_H:-26}"
    if [ "$age_h" -le "$max" ]; then
      echo "OK   last backup ${age_h}h ago"
    else
      echo "WARN last backup ${age_h}h ago (> ${max}h)"; status=1
    fi
  else
    echo "WARN no backups found in $BACKUP_DIR"; status=1
  fi
fi

exit "$status"
