---
name: linkedin-reply
description: Triage the comments under the owner's own LinkedIn post and draft replies in priority order, including critics and possible leads. Use when the user shares the comments on their post, has pushback or a lead in a thread, or at the +30 min / +2 h / +24 h post checks.
license: MIT
metadata:
  version: "1.0.0"
  repository: "https://github.com/Oxde/linkedin-harness"
---

# LinkedIn Reply

The thread under a fresh post is part of the post. Good replies keep the conversation going
and show readers what the owner is like to talk to. Not every comment deserves a reply, and the
early ones matter more than the late ones.

Read first: `VOICE.md`, the post's archive entry in `archive/` (exact text, URL, date), and the
post's draft file in `drafts/` (the evidence ledger, so replies stay consistent with the sources).

## Getting the comments

- Pasted text or screenshots from the user, with names and headlines when available.
- Or the read-only browser bridge from `docs/linkedin-adapters.md`, for the owner's own post
  only, slowly, stopping on any challenge.
- Never reply, react or delete through a browser or API. The owner replies by hand.

## When to run

Queue D in `docs/growth-system.md`: +30 min (answer the first real comments), +2 h (the thread
is forming), +24 h (close it out and write the lesson). Outside those, only when the user asks.

## Triage

Put every comment in one bucket and print the counts before any draft:

- **Lead** — has the problem the owner works on, or hints at hiring or buying.
- **Substance** — new data, a real question, a disagreement, a correction.
- **Peer** — someone in the lane whose attention is worth a real exchange.
- **Thanks** — praise, emoji, a tag. A like, and at most a few words.
- **Noise** — pitches, spam, bad faith. No reply.

Draft in this order: substance and leads first, then peers, then thanks. Stop when the
remaining comments would only get filler.

## How to reply

- **Answer in public.** If someone asks how, the how goes in the reply. Moving it to DMs hides
  the most useful part of the thread from everyone else.
- **Same size as the comment.** A one-line comment gets one or two lines back.
- **Critic:** grant what is correct first, quoting it. Then keep the point the owner
  still believes, with the source or the receipt from the draft's ledger. One reply per critic.
  If they are right, say so plainly and note the correction in the draft file.
- **Lead:** answer the question fully first. Then one sentence that leaves the door open. No
  calendar link, no pitch.
- **A factual question the owner cannot answer from the ledger:** say so, or leave
  `{{answer}}` and flag it. Never make up a figure to sound sure.
- Plain words, the jargon test, then the `anti-ai-writing` pass on every reply.

## Hand-off

One block: the counts, then each reply grouped by bucket, with the commenter's name and their
comment quoted in one line above it. Mark the ones to send first. The user sends them.

## After the +24 h check

Write one lesson into the post's draft file under a `## Lesson` heading: what the comments
show about the hook, the claim or the audience. One sentence, backed by what was said, not by
a guess. If nothing was learned, write that.

## Never

- Reply to a pitch; it only gives it reach.
- Argue twice with the same person, or delete a fair critic.
- Promise anything in public the owner has not confirmed (a call, a template, a price).
