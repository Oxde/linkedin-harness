#!/usr/bin/env bash
# feedctl for agents: loads FEED_URL/FEED_TOKEN from $LINKEDIN_HARNESS_ENV (default <checkout>/.env) if the
# shell lacks them, finds the checkout, and runs `python3 -m feed.feedctl "$@"`.
#   bash "$LINKEDIN_HARNESS/feed/ctl.sh" set-status <id> shown --insight "..." --why "..."
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." 2>/dev/null && pwd)"
[ -f "$ROOT/feed/feedctl.py" ] || ROOT="${LINKEDIN_HARNESS:?set LINKEDIN_HARNESS to the linkedin-harness checkout}"
if [ -z "${FEED_URL:-}" ] || [ -z "${FEED_TOKEN:-}" ]; then
  ENV_FILE="${LINKEDIN_HARNESS_ENV:-$ROOT/.env}"
  if [ -f "$ENV_FILE" ]; then
    # Only these two keys; env files often hold unquoted values that break plain sourcing.
    while IFS='=' read -r k v; do
      case "$k" in FEED_URL|FEED_TOKEN) export "$k=$v";; esac
    done < <(grep -E '^(FEED_URL|FEED_TOKEN)=' "$ENV_FILE")
  fi
fi
cd "$ROOT"
exec "${PYTHON:-python3}" -m feed.feedctl "$@"
