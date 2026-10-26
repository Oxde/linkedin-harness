---
name: linkedin-week
description: Plan the coming LinkedIn week from real material - the research feed, active drafts, the last audit's lessons and the owner's lane - with post slots, the reason behind each, and who to engage with. Use at the start of each week, or when the user asks for a posting plan or has run out of ideas.
license: MIT
metadata:
  version: "1.0.0"
  repository: "https://github.com/Oxde/linkedin-harness"
---

# LinkedIn Week

A plan made from topics produces filler. A plan made from what already exists - verified feed
items, drafts in progress, things the owner did this week - produces posts. This skill only
plans; drafting goes through `linkedin-writer`, engagement through `COMMENT_QUEUE.md`.

## 1. Collect the material

Read, in this order, and note what each gave you:

1. `VOICE.md` → Lane and Audience. Every slot must fit it.
2. `ACTIVE.md` and `drafts/`. Unfinished drafts come before new ideas.
3. The feed: `bash "$LINKEDIN_HARNESS/feed/ctl.sh" list` for picked and shown items, and
   `... stats --days 7` for what the owner actually picks and which sources pay off.
4. The latest `linkedin-audit` lesson, if one exists. It overrides any default below.
5. `PLAN.md` from last week, so themes and hook shapes do not repeat.
6. One question to the owner: what happened this week that only they saw? A result, a failure,
   something they shipped, a disagreement they had. Field receipts beat any feed item.

## 2. Fill the slots

The owner's cadence lives in `VOICE.md`; if it is not there, ask once and write it down. Slots
are ceilings, not quotas. A slot without a strong candidate stays empty. A forced post costs
more than a skipped day.

For each slot write:

- the candidate (feed id, draft file, or the owner's own event),
- the angle in one sentence: what only the owner can say about it,
- the shape: news, field note, guide, skill post, opinion, story, carousel,
- the proof it needs and whether that proof exists yet,
- verdict: `ready to draft`, `needs proof`, or `not a post` with the reason.

Rules for the mix:

- Never two slots in a row with the same shape or hook pattern.
- At least one slot built on the owner's own receipt, not on news.
- A weak pick is not a post. If the feed has nothing strong, say so and leave the slot empty.
- Short is the default. Long only for a real story or a guide with a saveable artifact.

## 3. Engagement list

Pick a small list of people for the week from the feed's `post` lane and the owner's lane:
peers, larger accounts the owner can genuinely add to, and people the owner would like to work
with. For each, the reason the owner has something to add. Put candidates in
`COMMENT_QUEUE.md`; drafts come from the `linkedin-comment` skill or the research playbook.

## 4. Timing, last

Posting time is the last lever. Use the owner's own audit data if it shows a real difference;
otherwise pick a consistent time in the audience's timezone and stop thinking about it. If the
owner is tuning times while hooks are weak, say so.

## Output

Write `PLAN.md` in the workspace and show it:

```
WEEK OF <date>
<day>  <shape>  <candidate>  -> <angle>  [ready | needs proof | not a post]
...
EMPTY SLOTS  <why>
ENGAGE       <name> - <what the owner can add>
FROM AUDIT   <the lesson this plan applies>
```

Then: "Say 'draft <day>' to start one." Nothing is scheduled or posted by this skill.
