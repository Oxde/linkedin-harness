---
name: linkedin-profile
description: Score a LinkedIn profile against a 100-point rubric and rewrite the weakest parts first - headline, about, featured, experience, banner. Use when the user wants their profile reviewed or rewritten, a better headline or about section, or asks why the profile does not bring the right people.
license: MIT
metadata:
  version: "1.0.0"
  repository: "https://github.com/Oxde/linkedin-harness"
---

# LinkedIn Profile

A post earns one visit to the profile. The profile decides whether that visit turns into a
follow, a message or nothing. This skill judges it the way a stranger arriving from a post would,
then fixes the parts that cost the most.

Read first: `VOICE.md` (positioning, lane, audience, proof the owner can publish) and
`references/rubric.md` in this folder.

## 1. Get the profile as text

Ask the user to paste the headline, the about section, the current role and the two roles
before it, the featured items, and one line describing the banner. A screenshot of the top of
the profile is enough to start. Never log in, never scrape the page.

If `VOICE.md` is empty, stop and fill its Positioning and Lane sections with the user first. A
profile rewritten without knowing the audience is a guess.

## 2. Score it honestly

Score every rubric item, show the table, give the total. Write one plain reason next to each
score: what a visitor sees, not a grade word. A first pass on a real profile usually lands far
below 70; a kind score helps nobody.

```
PROFILE  52/100
  first glance           9/20   headline is a job title; no audience
  proof on the page      6/20   no number anywhere above the fold
  ...
```

## 3. Rewrite in order of points lost

Fix the biggest loss first and stop after three sections in one session; the user has to paste
each change in by hand and will not do eight at once.

- **Headline.** Who the owner helps, with what, plus one piece of proof. Plain words, no
  category jargon a stranger would not know (run the jargon test from `anti-ai-writing`). Give
  three options with different proof.
- **About, opening.** The two lines visible before "see more" carry the section. Say who it is
  for and what changes for them. No self-description adjectives, no third person.
- **About, body.** Write to one reader: the problem, what the owner does about it, one proof
  with a number the owner can source, how to start a conversation. Short beats complete.
- **Featured.** The post that best shows the owner's lane, one proof asset (a repo, a case,
  a result), one way to reach them.
- **Experience.** Each role: one line of scope, then results with numbers, not duties.
- **Banner.** What the owner does, plus how to reach them, in the owner's `VISUAL_STYLE.md`
  if they have one.

## Rules

- Never invent a number, client, title or result. Missing proof becomes `{{number from you}}`
  with a flag saying what would fill it.
- Every rewrite goes through the `anti-ai-writing` pass before the user sees it.
- Keep the owner's register. A blunt writer gets a blunt headline, not a polished one.
- Do not chase keywords at the cost of clarity. A stranger must understand it in one read.

## Output

The score table, then copy-ready blocks for the sections fixed this session, each with its
character count. Score it again afterwards and report the honest change. Name what a rewrite cannot fix
(posting history, recommendations, a real proof asset) instead of hiding it in the score.

This skill never edits the profile itself; the user copies each section in.
