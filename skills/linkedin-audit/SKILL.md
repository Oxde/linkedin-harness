---
name: linkedin-audit
description: Post-mortem on the owner's published LinkedIn posts from their own numbers - which posts worked, why, how sure we can be, and the one lesson for next week. Use after the 24-hour check on a post, when the user shares an analytics export or metrics snapshots, or asks which posts performed, why a post underperformed, or what to change.
license: MIT
metadata:
  version: "1.0.0"
  repository: "https://github.com/Oxde/linkedin-harness"
---

# LinkedIn Audit

Every LinkedIn rule, including the ones in this harness, is a prior. The owner's own posts are
the evidence. This skill turns that evidence into one lesson the next plan has to follow.

## 1. Load the data

Use what exists, best first:

1. The metrics collector's output in `$LINKEDIN_METRICS_DIR`: `latest.json` (current numbers per
   `activity_urn`: impressions, reactions, comments) and `snapshots.jsonl` (the same over time,
   which gives the first-hours curve).
2. `archive/POSTS.md` for each post's date, hook, topic and URN; the archived text and draft
   files for shape, length, visual and hook pattern.
3. A LinkedIn analytics export the user pastes or attaches.
4. Numbers the user types in. Enough for a first pass, say so.

Join on the URN. Never fill a missing count with a guess; mark it missing.

## 2. Compute rates, not totals

Impressions mostly reflect follower count. Show the working for:

- **engagement rate** = (reactions + comments + reposts) / impressions
- **comment ratio** = comments / reactions — did it start a conversation
- **reach multiple** = impressions / followers — did it travel past the existing audience
- **saves and sends**, when the source shows them — the strongest sign a post was useful
- **early pace** from `snapshots.jsonl`: share of 24-hour impressions reached by +2 hours

## 3. Compare the top against the bottom

Rank by engagement rate and reach multiple. Put the best and worst few side by side and check,
in this order:

1. topic and lane fit
2. hook: named thing + number or behaviour in line one, or not
3. proof: primary source, own receipt, or summary
4. shape and length
5. visual
6. replies by the owner in the first hours
7. day and time, only if nothing above separates them

## 4. Say how sure you are

State each finding as a claim, the numbers behind it, and the sample size. Under ten posts,
call it a hunch. A difference inside normal noise is not a finding. Do not invent a pattern to
have something to report; "nothing separates them yet" is a valid result.

## 5. Write the lesson back

Pick the one finding with the strongest evidence and write it where it changes behaviour:

- in the draft file's frontmatter or `## Quality check` for a single post,
- in `VOICE.md` or the relevant skill reference when it is a pattern across posts,
- as `FROM AUDIT` input for the next `linkedin-week` run.

One lesson per audit. Five lessons are a report nobody acts on.

## Output

```
AUDIT  <n> posts  <date range>  source: <collector | export | pasted>
TOP     <rate>  <hook first line>  <what it had>
BOTTOM  <rate>  <hook first line>  <what it lacked>
FINDING <claim>  evidence: <numbers>  n=<count>  confidence: <hunch | likely | clear>
LESSON  <the one rule for next week>  written to: <file>
```
