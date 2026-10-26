---
name: linkedin-repurpose
description: Turn one long source - a talk, transcript, newsletter, repo README, report or the owner's own long article - into separate LinkedIn posts that each stand alone. Use when the user has a long piece (video, podcast, article, write-up) and wants several LinkedIn posts out of it.
license: MIT
metadata:
  version: "1.0.0"
  repository: "https://github.com/Oxde/linkedin-harness"
---

# LinkedIn Repurpose

A long source is a mine, not a post. The job is to find the parts that stand on their own and
drop the rest. A summary of the source is never one of the posts.

## 1. Read all of it first

Get the full text: the transcript, the article, the README, the call notes. If the user gives a
link and a fetch or transcript tool exists in the session, fetch it once; if not, ask the user to paste the text.
Do not extract from the first third.

The owner's own long articles (see `docs/growth-system.md`, "Long articles") are the best source
there is: the facts are already checked and the opinion is already theirs.

## 2. Build the extraction ledger

Before writing any post, list what the source actually contains, each with where it appears:

| kind | what to pull |
|---|---|
| claim | a sentence someone could disagree with |
| number | a figure, cost, time, count, with its context |
| scene | a moment with a person, an action and a consequence |
| mechanism | how something works, step by step |
| failure | something that broke or was wrong, and what it cost |
| artifact | a table, checklist, command or rule a reader could save |

Facts in a third-party source get checked against their primary source before they go in a
post, the same as any news item.

## 3. Judge the yield

Count the ledger. If it holds fewer than three strong, separate items, say "thin source: <n>
items" and propose one post, or none. Squeezing four posts out of one idea gives four weak posts
in the same voice. A weak pick is not a post.

## 4. Plan the set

Each candidate becomes one post with:

- the single ledger item it is built on,
- the angle only the owner can add (their receipt, disagreement or rule),
- the shape and a hook pattern different from its neighbours,
- a standalone check: does it make sense to someone who never saw the source?

Never write "in my latest video" or "as I said in the newsletter" as the reason to read. The post
is the thing. A link to the source can go in the first comment if the owner wants it.

Lead the set with the strongest claim and the saveable artifact goes later, when
readers of the first post are watching. Add the set to `ACTIVE.md` or the week's `PLAN.md`.

## 5. Draft one at a time

Draft only the post the owner picks, through `linkedin-writer`: evidence, hook pass, draft in
`VOICE.md`, `anti-ai-writing` pass, visual decision. Short by default. Do not hand over the whole
set as finished drafts; they come out sounding alike and none gets edited.

## Output

```
SOURCE   <title>  <length>  <type>
LEDGER   <n> claims, <n> numbers, <n> scenes, <n> mechanisms, <n> failures, <n> artifacts
VERDICT  <n> posts | thin source
SET
1. <shape>  <ledger item>  -> <owner's angle>
...
Say "draft 1" to start.
```
