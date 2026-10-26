#!/usr/bin/env bash
# Scheduler script (no agent) for the weekly feed-stats job.
set -euo pipefail
# Works from the Git checkout and as a copy in an agent's scripts directory (then set LINKEDIN_HARNESS).
ROOT="$(cd "$(dirname "$0")/.." 2>/dev/null && pwd)"
[ -f "$ROOT/feed/feedctl.py" ] || ROOT="${LINKEDIN_HARNESS:?set LINKEDIN_HARNESS to the linkedin-harness checkout}"
if [ -z "${FEED_URL:-}" ] || [ -z "${FEED_TOKEN:-}" ]; then
  ENV_FILE="${LINKEDIN_HARNESS_ENV:-$ROOT/.env}"
  if [ -f "$ENV_FILE" ]; then
    while IFS='=' read -r k v; do case "$k" in FEED_URL|FEED_TOKEN|GH_TOKEN) export "$k=$v";; esac; done < <(grep -E '^(FEED_URL|FEED_TOKEN|GH_TOKEN)=' "$ENV_FILE")
  fi
fi
cd "$ROOT"
exec "${PYTHON:-python3}" -m feed.feedctl stats --days "${FEED_STATS_DAYS:-7}"
