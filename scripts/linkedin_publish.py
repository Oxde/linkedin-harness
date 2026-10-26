#!/usr/bin/env python3
"""Publish one approved text post to LinkedIn through the free official API.

Standard library only. The post goes out only when all of these hold:

- the text file's SHA-256 equals --sha256 (the hash of the exact text the user approved);
- --post is given (without it the script prints the payload and exits: a dry run);
- LINKEDIN_ACCESS_TOKEN is set (a member token with the w_member_social scope).

The author is LINKEDIN_AUTHOR_URN (urn:li:person:<id>) or, when unset, read from /v2/userinfo
(needs the openid and profile scopes on the same token). See docs/publishing.md.

Usage:
  python3 scripts/linkedin_publish.py drafts/post.txt --hash-only
  python3 scripts/linkedin_publish.py drafts/post.txt --sha256 <hash>            # dry run
  python3 scripts/linkedin_publish.py drafts/post.txt --sha256 <hash> --post     # publish
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

POSTS_URL = "https://api.linkedin.com/rest/posts"
USERINFO_URL = "https://api.linkedin.com/v2/userinfo"
MAX_CHARS = 3000
# LinkedIn's "little text" format treats these as markup; unescaped, they can cut the post short.
RESERVED = re.compile(r"([\\|{}@\[\]()<>#*_~])")


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def escape_commentary(text: str) -> str:
    return RESERVED.sub(r"\\\1", text)


def default_version(today: dt.date | None = None) -> str:
    """The previous month as YYYYMM: LinkedIn releases a version monthly and keeps each for about a year."""
    today = today or dt.date.today()
    first = today.replace(day=1)
    prev = first - dt.timedelta(days=1)
    return f"{prev.year}{prev.month:02d}"


def build_payload(author: str, text: str) -> dict:
    return {
        "author": author,
        "commentary": escape_commentary(text),
        "visibility": "PUBLIC",
        "distribution": {"feedDistribution": "MAIN_FEED", "targetEntities": [], "thirdPartyDistributionChannels": []},
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }


def request(url: str, token: str, version: str, body: dict | None = None) -> tuple[int, dict, str]:
    headers = {"Authorization": f"Bearer {token}", "X-Restli-Protocol-Version": "2.0.0", "LinkedIn-Version": version}
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST" if body is not None else "GET")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, dict(resp.headers), resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        raise RuntimeError(f"LinkedIn {req.get_method()} {url} failed: HTTP {exc.code}: {detail}") from exc


def author_urn(token: str, version: str) -> str:
    urn = os.environ.get("LINKEDIN_AUTHOR_URN", "").strip()
    if urn:
        if not urn.startswith(("urn:li:person:", "urn:li:organization:")):
            raise SystemExit(f"LINKEDIN_AUTHOR_URN must be urn:li:person:<id> or urn:li:organization:<id>, got {urn!r}")
        return urn
    _, _, body = request(USERINFO_URL, token, version)
    sub = json.loads(body).get("sub")
    if not sub:
        raise RuntimeError(f"/v2/userinfo returned no 'sub' (token needs openid + profile scopes): {body}")
    return f"urn:li:person:{sub}"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("text_file", type=Path, help="file holding exactly the approved post text")
    p.add_argument("--sha256", help="SHA-256 of the approved text; publishing refuses any other text")
    p.add_argument("--hash-only", action="store_true", help="print the text's SHA-256 and exit")
    p.add_argument("--post", action="store_true", help="actually publish (default is a dry run)")
    args = p.parse_args(argv)

    text = args.text_file.read_text(encoding="utf-8").strip()
    digest = sha256(text)
    if args.hash_only:
        print(digest)
        return 0
    if not text:
        raise SystemExit(f"{args.text_file} is empty")
    if len(text) > MAX_CHARS:
        raise SystemExit(f"post is {len(text)} characters; LinkedIn allows {MAX_CHARS}")
    if not args.sha256:
        raise SystemExit(f"--sha256 is required (this text hashes to {digest}; get it approved first)")
    if args.sha256 != digest:
        raise SystemExit(f"text changed since approval: expected {args.sha256}, file hashes to {digest}")

    token = os.environ.get("LINKEDIN_ACCESS_TOKEN", "").strip()
    version = os.environ.get("LINKEDIN_API_VERSION", "").strip() or default_version()
    if not args.post:
        author = os.environ.get("LINKEDIN_AUTHOR_URN", "").strip() or "urn:li:person:<from /v2/userinfo>"
        print(json.dumps({"dry_run": True, "linkedin_version": version, "payload": build_payload(author, text)}, indent=2, ensure_ascii=False))
        return 0
    if not token:
        raise SystemExit("LINKEDIN_ACCESS_TOKEN is not set (see docs/publishing.md)")

    author = author_urn(token, version)
    status, headers, body = request(POSTS_URL, token, version, build_payload(author, text))
    post_id = headers.get("x-restli-id") or headers.get("X-RestLi-Id") or ""
    if status != 201 or not post_id:
        raise RuntimeError(f"unexpected response: HTTP {status}, id={post_id!r}, body={body!r}")
    print(json.dumps({"posted": True, "id": post_id, "url": f"https://www.linkedin.com/feed/update/{post_id}/", "sha256": digest}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
