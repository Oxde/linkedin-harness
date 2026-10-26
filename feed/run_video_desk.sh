#!/usr/bin/env bash
# Scheduler script for the video-desk job: the week's competitor reels with outliers, plus post lane.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." 2>/dev/null && pwd)"
[ -f "$ROOT/feed/feedctl.py" ] || ROOT="${LINKEDIN_HARNESS:?set LINKEDIN_HARNESS to the linkedin-harness checkout}"
if [ -z "${FEED_URL:-}" ] || [ -z "${FEED_TOKEN:-}" ]; then
  ENV_FILE="${LINKEDIN_HARNESS_ENV:-$ROOT/.env}"
  if [ -f "$ENV_FILE" ]; then
    while IFS='=' read -r k v; do case "$k" in FEED_URL|FEED_TOKEN) export "$k=$v";; esac; done < <(grep -E '^(FEED_URL|FEED_TOKEN)=' "$ENV_FILE")
  fi
fi
cd "$ROOT"
exec "${PYTHON:-python3}" -m feed.feedctl videos --days "${VIDEO_DESK_DAYS:-7}" --n "${VIDEO_DESK_N:-30}"
