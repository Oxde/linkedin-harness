#!/usr/bin/env python3
"""Clean a draft's invisible characters and flag the tells listed in the anti-ai-writing skill.

Standard library only. Runs locally on a file or stdin; nothing is sent anywhere.

What it changes (only things with no meaning a reader could see):
  - zero-width and other Unicode format characters, byte-order marks, soft hyphens
  - non-breaking and narrow spaces → normal spaces
  - with --plain-punct: curly quotes → straight, the ellipsis character → "...", bullet "•" → "-"

What it flags, with line numbers, and never rewrites (that needs judgement):
  banned words, AI sentence shapes, more than one em dash, a hook with nothing concrete in it,
  a closing question or summary, emoji used as punctuation, a wall of hashtags.

It does not score "how human" a text is. No local script can say that honestly.

Usage:
  python3 clean.py draft.txt                      # report only
  python3 clean.py draft.txt -o clean.txt         # write the cleaned text, then report
  python3 clean.py draft.txt --voice VOICE.md     # also flag the owner's "Words I never use"
  printf 'text' | python3 clean.py -
Exit code: 0 no flags, 1 flags found, 2 bad input.
"""
from __future__ import annotations

import argparse
import re
import statistics
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path

SPACES = {" ", " ", " ", " ", " ", "　"}
PLAIN_PUNCT = {"‘": "'", "’": "'", "“": '"', "”": '"', "…": "...", "•": "-"}

BANNED_WORDS = [
    # corporate filler
    "leverage", "synergy", "ecosystem", "robust", "seamless", "seamlessly", "streamline", "empower",
    "unlock", "elevate", "supercharge", "game-changer", "game changer", "cutting-edge", "best-in-class",
    "holistic", "paradigm", "transformative", "revolutionize", "revolutionise",
    # model favourites
    "delve", "tapestry", "testament", "realm", "crucial", "pivotal", "vibrant", "intricate",
    "multifaceted", "nuanced", "underscore", "underscores", "foster", "in today's fast-paced world",
    "ever-evolving", "navigate the", "embark", "journey",
    # hype
    "insane", "mind-blowing", "mind blowing", "holy shit", "this changes everything", "must-have",
]

SHAPES = [
    ("fake contrast", r"\b(it|this|that)['’]?s? (is )?not (just |only |about )?[^.!?\n]{1,60}[.,;]\s*(it|this|that)['’]?s?\b"),
    ("fake contrast", r"\bthe (weird|real|interesting|important) (part|story|thing) (wasn['’]t|isn['’]t|is)\b"),
    ("fake contrast", r"\bnot only\b[^.!?\n]{1,60}\bbut also\b"),
    ("staged reveal", r"^(the (result|catch|kicker|twist|answer|truth)|here['’]s the thing|plot twist)[?:.!]?\s*$"),
    ("staged reveal", r"^\w+\?\s*$"),
    ("generic moral", r"\b(this matters|let that sink in|the future is|what nobody tells you|read that again)\b"),
    ("summary close", r"^(in short|ultimately|at the end of the day|in conclusion|tl;?dr)\b"),
    ("engagement bait", r"^(thoughts|agree|who else|what do you think|am i wrong)\?\s*$"),
    ("hedge stack", r"\b(might|may|could) (potentially|possibly)\b"),
]
EMOJI_PUNCT = re.compile("[\U0001F680\U0001F525\U0001F4A1✨\U0001F3AF\U0001F6A8\U0001F447✅]")


@dataclass
class Flag:
    line: int
    kind: str
    text: str


def clean(text: str, plain_punct: bool) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {}
    out = []
    for ch in text:
        if ch in SPACES:
            counts["odd spaces"] = counts.get("odd spaces", 0) + 1
            out.append(" ")
        elif unicodedata.category(ch) == "Cf" or ch == "­":
            counts["invisible characters"] = counts.get("invisible characters", 0) + 1
        elif plain_punct and ch in PLAIN_PUNCT:
            counts["curly punctuation"] = counts.get("curly punctuation", 0) + 1
            out.append(PLAIN_PUNCT[ch])
        else:
            out.append(ch)
    return "".join(out), counts


def voice_words(path: Path) -> list[str]:
    """The comma-separated list after '**Words I never use:**' in the owner's VOICE.md."""
    match = re.search(r"\*\*Words I never use:\*\*\s*(.+)", path.read_text(encoding="utf-8"))
    if not match:
        raise SystemExit(f"{path}: no '**Words I never use:**' line found")
    return [w.strip().lower() for w in match.group(1).split(",") if w.strip()]


def check(text: str, extra_words: list[str]) -> list[Flag]:
    flags: list[Flag] = []
    lines = text.splitlines()
    words = [w.lower() for w in BANNED_WORDS + extra_words]
    for n, line in enumerate(lines, 1):
        low = line.lower()
        for w in words:
            if re.search(rf"(?<![\w-]){re.escape(w)}(s|es|d|ed|ing)?(?![\w-])", low):
                flags.append(Flag(n, "banned word", w))
        for kind, pattern in SHAPES:
            if re.search(pattern, line.strip(), re.IGNORECASE):
                flags.append(Flag(n, kind, line.strip()[:80]))
        if EMOJI_PUNCT.search(line):
            flags.append(Flag(n, "emoji as punctuation", line.strip()[:80]))
    dashes = [n for n, line in enumerate(lines, 1) for _ in range(line.count("—"))]
    if len(dashes) > 1:
        flags.append(Flag(dashes[0], "em dashes", f"{len(dashes)} in the post (lines {sorted(set(dashes))}); keep one at most"))
    hashtags = re.findall(r"(?<!\w)#\w+", text)
    if len(hashtags) > 3:
        flags.append(Flag(len(lines), "hashtag wall", f"{len(hashtags)} hashtags"))
    first = next((l.strip() for l in lines if l.strip()), "")
    named = any(w[:1].isupper() and w.lower() not in {"i", "i'm", "i've"} for w in first.split()[1:])
    if first and not (re.search(r"\d|\$", first) or named):
        flags.append(Flag(1, "weak hook", "line 1 has no number and no named thing"))
    last = next((l.strip() for l in reversed(lines) if l.strip()), "")
    if last.endswith("?") and len(last) < 60:
        flags.append(Flag(len(lines), "closing question", last))
    bait = {f.line for f in flags if f.kind == "engagement bait"}
    return [f for f in flags if not (f.line in bait and f.kind in ("staged reveal", "closing question"))]


def stats(text: str) -> str:
    sentences = [s for s in re.split(r"(?<=[.!?])\s+|\n+", text) if re.search(r"\w", s)]
    lengths = [len(re.findall(r"\w+", s)) for s in sentences]
    words = sum(lengths)
    spread = statistics.pstdev(lengths) if len(lengths) > 1 else 0.0
    numbers = len(re.findall(r"\d[\d,.]*%?", text))
    return (f"{len(text)} characters · {words} words · {len(sentences)} sentences · "
            f"sentence length {min(lengths, default=0)}-{max(lengths, default=0)} words (spread {spread:.1f}) · {numbers} numbers")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("input", help="draft file, or - for stdin")
    p.add_argument("-o", "--output", type=Path, help="write the cleaned text here")
    p.add_argument("--plain-punct", action="store_true", help="also straighten quotes and replace … and •")
    p.add_argument("--voice", type=Path, help="the owner's VOICE.md; adds its 'Words I never use' list")
    args = p.parse_args(argv)

    raw = sys.stdin.read() if args.input == "-" else Path(args.input).read_text(encoding="utf-8")
    if not raw.strip():
        print("empty draft", file=sys.stderr)
        return 2
    text, changes = clean(raw, args.plain_punct)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    flags = check(text, voice_words(args.voice) if args.voice else [])

    print(stats(text))
    if changes:
        print("cleaned: " + ", ".join(f"{v} {k}" for k, v in changes.items()) + ("" if args.output else " (use -o to save)"))
    if not flags:
        print("no flags. Still read it aloud once; the script cannot judge voice or truth.")
        return 0
    print(f"{len(flags)} flags, rewrite these by hand:")
    for f in sorted(flags, key=lambda f: f.line):
        print(f"  line {f.line:>3}  {f.kind:<20} {f.text}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
