# The growth system

The harness turns research into posts in one person's voice, measures what happened, and feeds
the lesson into the next post. It never posts, comments, reacts, connects or DMs on its own.

## Four queues

Each queue runs on its own schedule and writes durable state (the feed service, draft files,
queue files). A chat message is a summary of that state, never the only copy.

### A. News desk

Turn high-signal news in the owner's lane into post candidates.

- Inputs: lead sources (Telegram channels, RSS, newsletters) and primary sources (company
  announcements, papers, changelogs, launch posts).
- Rule: lead sources supply energy and leads; the original source supplies the facts.
- Output per candidate: the event (named actor + exact change), three verified facts with URLs,
  why the audience should care, the owner's angle, the format, and the decision (draft, go
  deeper, skip).

In the harness this is the `feed-menu` job over the `news` and `post` lanes.

### B. Niche feed intelligence

Learn why posts in the lane work. Never copy them.

- Read-only: a small set of searches and a deliberate list of accounts.
- Per post: URL and author, the first lines, visible numbers (only when the page shows them),
  why it worked (tension, proof, format, timing, the reader's fear, status or control stake),
  the owner's different angle, and a comment opportunity only when the owner has a real datum,
  disagreement or receipt to add.

In the harness: the `post` lane (Hacker News, Lobsters, LinkedIn search through Apify).

### C. Skills and workflow desk

Find agent skills, repos and tools worth talking about, then test them before writing.

- Inputs: ClawHub, skills.sh, GitHub search, rising repos, a watchlist.
- Output: a few judged candidates with a verdict against the best-known option; the generic ones
  skipped with the reason so they never return.
- After a pick: inspect → test safely → write only when there is a real artifact.

In the harness: the `skill-desk` job, the `skill-radar` and `skill-posts` skills.

### D. Own-post performance and community

Make every published post improve the next one.

- At +30 min, +2 h and +24 h: impressions, reactions, comments, reposts and saves where visible.
- Diagnose with hook, topic, format, visual, early comments and the reader's stake. Posting time
  is the last explanation, not the first.
- Output: metrics only when real read data exists, up to three approval-gated reply drafts, and
  one concrete lesson written into the draft or a reference file.

In the harness: `scripts/collect_linkedin_metrics.py` and the dashboard.

## Editorial loop

1. Store each promising item as a draft file in `drafts/` (from `templates/draft.md`).
2. Set its status and the next action.
3. Fill the evidence ledger: source, three to six load-bearing facts, the weirdest fact, the
   tension, the conclusion the source supports.
4. Optional niche signal pass: a small live sample of posts on the same topic, to see whether
   the topic or hook shape is saturated. Record the signal; never copy text or treat blank
   counters as data.
5. Choose one angle that only the owner could honestly write.
6. Run a separate hook pass.
7. Draft in the `VOICE.md` style.
8. Fact pass, `anti-ai-writing` pass, visual-fit pass.

## Quality bar for each post

Two posts a day is a ceiling, never a quota. A candidate is publishable only when it clears all:

1. **Primary evidence:** an official source, paper, product artifact, repo or test, or a direct
   field receipt; not a recycled news summary.
2. **An owner-only claim:** an observation, mechanism, disagreement or result a generic
   AI-content account could not honestly write.
3. **Specific load:** a named actor plus a number, mechanism, artifact or compact comparison.
4. **Distinctness:** a second post the same day is not a paraphrase of the first.
5. **Reader value:** a decision rule, a failure mode or a mechanism worth saving.
6. **Human review:** hook pass, anti-AI-writing pass, and a rendered visual check when a visual
   is used.

If a candidate fails, skip the slot.

## Draft statuses

- `researching` — the source is not verified yet.
- `drafting` — angle, hook or body in progress.
- `needs-visual` — copy is ready enough; the visual is missing.
- `waiting-for-user` — needs a decision; scheduled jobs must not repeat the whole draft.
- `approved` — exact copy and visual approved; waiting for the explicit "post now".
- `posted` — live URL and archive verified.
- `parked` — good, not a current priority; no reminders.
- `rejected` — do not revive unless the user asks.

## Quality gates

- A news post cannot rest on a screenshot or summary when the primary source can be opened.
- A guide cannot be all prose when a table or checklist would make it worth saving.
- A launch post cannot read like documentation; lead with the pain it removes.
- A draft the user calls "long and not meaty" is rebuilt around a stronger fact, not trimmed.
- No post is final without the anti-AI-writing pass and a visual decision.

## Long articles

For comparisons, guides, market maps and benchmark explainers, write the long piece first:
scope, sourced fact matrix, separate benchmark matrix, personal receipts if written in first
person, the article with tables and a checked-on date, then the fact, voice and reader-value
passes. Only then derive the feed post or carousel from it.

## Publishing

- Every post has a visual decision: source image, product screenshot, card, carousel, or no
  visual by the user's explicit choice.
- Publishing needs the user's explicit "post now" on the exact text. Hash the approved text
  (SHA-256) and refuse to publish anything whose hash differs, then verify the live post and
  archive the exact payload.

## Definition of working

In one week the system produced: five verified news candidates, six analysed niche posts with
URLs and lessons, two reviewed skills with real test notes, one published post with a 24-hour
review, and zero autonomous social actions.
