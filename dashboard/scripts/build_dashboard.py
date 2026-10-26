#!/usr/bin/env python3
"""Build JSON for the local LinkedIn intelligence dashboard."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


SOURCES_FILE = Path(__file__).resolve().parents[2] / "feed" / "sources.txt"
SOURCE_SECTIONS = {"telegram": "Telegram lead", "rss": "RSS"}


def read_sources(path: Path) -> list[dict]:
    """Telegram channels and RSS feeds from the feed's sources.txt, for the dashboard's source card."""
    if not path.exists():
        raise FileNotFoundError(f"sources file not found: {path}")
    out: list[dict] = []
    section = None
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].strip()
            continue
        if section == "telegram":
            out.append({"name": f"@{line}", "type": SOURCE_SECTIONS[section], "status": "active", "url": f"https://t.me/s/{line}"})
        elif section == "rss":
            out.append({"name": urlparse(line).netloc, "type": SOURCE_SECTIONS[section], "status": "active", "url": line})
    return out


def parse_archive(index: Path) -> list[dict]:
    if not index.exists():
        return []
    posts: list[dict] = []
    current: dict | None = None
    for line in index.read_text(errors="ignore").splitlines():
        if line.startswith("## "):
            if current:
                posts.append(current)
            current = {"published_at": line[3:].strip(), "hook": "", "urn": "", "topic": ""}
        elif current and line.startswith("- Hook:"):
            current["hook"] = line.split(":", 1)[1].strip()
        elif current and "LinkedIn URN:" in line:
            match = re.search(r"`([^`]+)`", line)
            current["urn"] = match.group(1) if match else ""
        elif current and line.startswith("- Topic:"):
            current["topic"] = line.split(":", 1)[1].strip()
    if current:
        posts.append(current)
    return posts[:12]


def parse_active(active: Path) -> list[dict]:
    if not active.exists():
        return []
    items = []
    for line in active.read_text(errors="ignore").splitlines():
        match = re.match(r"\d+\. \[\[([^\]]+)\]\] — `([^`]+)`;?\s*(.*)", line)
        if match:
            items.append({"title": match.group(1), "status": match.group(2), "note": match.group(3)})
    return items


def build_data(archive: Path, active: Path, sources: Path = SOURCES_FILE) -> dict:
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "analytics": {
            "status": "not_connected",
            "message": "Connect LinkedIn browser read access or a paid data provider to populate followers, impressions, comments, and replies.",
            "followers": None,
            "impressions_30d": None,
            "comments_to_reply": None,
        },
        "latest_posts": parse_archive(archive / "POSTS.md"),
        "active_items": parse_active(active),
        "sources": read_sources(sources),
        "queues": [
            {"name": "Research menu", "schedule": "twice daily", "status": "active", "purpose": "Verified candidates from the feed, one line of why each matters; you pick."},
            {"name": "Skill desk", "schedule": "twice weekly", "status": "active", "purpose": "Judges top skill and repo candidates against the known option; skips the generic ones."},
            {"name": "Video desk", "schedule": "twice weekly", "status": "optional", "purpose": "Competitor reels of the week: outliers, formats, gaps, recordable ideas."},
            {"name": "Feed collect", "schedule": "twice daily", "status": "active", "purpose": "Runs every producer and posts new items to the feed service. No LLM."},
            {"name": "Post performance", "schedule": "daily", "status": "needs read adapter", "purpose": "Metrics, comments, reply drafts, and one lesson after a recent post."},
        ],
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--archive", required=True, type=Path)
    p.add_argument("--active", required=True, type=Path)
    p.add_argument("--out", required=True, type=Path)
    args = p.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(build_data(args.archive, args.active), indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
