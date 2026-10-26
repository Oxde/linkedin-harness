---
name: linkedin-comment
description: Draft comments on other people's LinkedIn posts that add something only the owner can add, or say "skip". Use when the user shares someone's post and asks what to say under it, wants an engagement round, or picks a POSTS item from the research menu.
license: MIT
metadata:
  version: "1.0.0"
  repository: "https://github.com/Oxde/linkedin-harness"
---

# LinkedIn Comment

A comment is a tiny post under someone else's name. It earns attention only when it carries
something the post did not: a fact, a case, a cost, a disagreement. Most posts do not need the
owner's comment. "Skip" is the most common correct answer.

Read first: `VOICE.md` (positioning, proof the owner may use, words they never use) and the
comment rules in `docs/research-playbook.md`.

## Where the post comes from

- Pasted text or a screenshot from the user. Read the whole post, not just the hook.
- A `post` lane item from the research menu: open the URL once, read-only.
- Never scrape the feed, never log in on the user's behalf, never click anything on LinkedIn.
  If the post cannot be read, ask the user to paste it. Do not guess what it said.

## Decide before drafting

Answer three questions, one line each:

1. **What does the post actually claim?** In plain words, one sentence.
2. **What can the owner add that is true and theirs?** A number they measured, a thing they
   built or broke, a case where the claim fails, a source the author missed. Check `VOICE.md`
   → "Proof I can use". If the only thing to add is agreement, stop.
3. **Is the author or audience worth it?** In the owner's lane, a reader the owner wants, a
   thread still young enough to be read.

If 2 or 3 is "no", output `skip: <reason>` and move on. Do not pad a weak comment into a
paragraph.

## Pick one move

- **Datum** — a figure or result from the owner's own work, with the unit and the context.
- **Missing case** — where the advice stops being true, and what happens there.
- **Pushback** — say the part that is right first, in the author's terms, then the part that
  is wrong and why. Never sarcasm.
- **Receipt** — the owner did this exact thing; two lines on what happened.
- **Sharp question** — the one question the post avoided. It must be answerable.
- **Correction** — only with a primary source link in hand. Short and kind.
- **Short and true** — a single line, only when it is genuinely funny or exactly right.

Name the move you chose. One move per comment.

## Write it

- 1–4 sentences. Plain words. Run the jargon test from the writer skill: any term the author's
  audience might not know gets replaced or explained in the same sentence.
- Open with the substance. No praise opener, no restating the post, no tagging strangers.
- Never invent a number, a client or an experience. If the comment needs a figure the owner has
  not given, write `{{number}}` and flag it.
- Run the `anti-ai-writing` pass. Comments are read closely; one stock phrase sinks them.

## Engagement round

When the user hands over several posts at once, or asks for a round from the feed:

1. Run "Decide before drafting" on each. Skips are listed with their reason, not drafted.
2. Draft at most five. A round is a ceiling, not a quota.
3. Spread across authors; do not land on the same person twice in a week. Check the queue.
4. Add each draft as a row in `queues/COMMENT_QUEUE.md`: Status `drafted`, Author, URL,
   Why engage, Comment type, Exact draft, Approved? empty, Sent? empty.

## Hand-off

Show per post: the move, the comment as a copy-ready block, and one line on why this one.
The user posts it by hand. When they confirm, set `Approved?` and `Sent?` in the queue.

## Never

- Post, react, follow or connect, by API or browser. This skill only writes text.
- Drop a link to the owner's own post or product into someone else's thread.
- Comment on a topic the owner cannot speak to from their own work, just to be visible.
