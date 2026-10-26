---
name: linkedin-carousel
description: Plan, write and render a LinkedIn carousel (a PDF document post) - decide if the idea needs one, plan the slides, write the copy and caption, and render a PDF from the owner's visual style. Use when the user wants slides, a carousel or a PDF post for LinkedIn, or has a step-by-step idea that would be cramped as text.
license: MIT
metadata:
  version: "1.0.0"
  repository: "https://github.com/Oxde/linkedin-harness"
---

# LinkedIn Carousel

A carousel is for ideas with parts: steps, a sequence, a before and after, a comparison, a
checklist people will save. One claim cut into slides is a text post with extra taps; send that
back to `linkedin-writer` and say why.

Read first: `VOICE.md`, `VISUAL_STYLE.md` (formats, colours, type, carousel rules), and the draft
file if one exists.

## 1. Plan before copy

Write the slide plan as one line per slide and get it approved before any design work:

- **Cover** - the hook in a few words, the named thing and the payoff. It decides everything.
- **Why it matters** - the cost or pain, with a sourced number if there is one.
- **The parts** - one idea per slide, in the order a reader would use them.
- **The saveable slide** - the whole thing compressed into one list or table that works as a
  screenshot on its own.
- **Close** - one next step: the rule, the install line, or what to comment. One.

Use as few slides as the idea needs. If the plan grows, the idea is two carousels or a long
article (`docs/growth-system.md`, "Long articles").

## 2. Copy rules

- A headline per slide that a reader on a phone gets in one glance. Short supporting text; if a
  slide needs a paragraph, split it or cut it.
- Plain words. Run the jargon test from `anti-ai-writing` on every slide.
- Numbers from the evidence ledger only, with the source on the slide or the last slide. Missing
  numbers stay `{{number}}` and are flagged.
- A progress mark on every slide (`03/07`) and the owner's handle where `VISUAL_STYLE.md` puts it.
- Run the `anti-ai-writing` pass on the slide copy and the caption before showing them.

## 3. The caption

The feed shows the caption above the PDF, so it is the real hook. Two or three short lines: the
claim, why to swipe, nothing that repeats slide one word for word.

## 4. Render the PDF

Only after the copy is approved. Write one HTML file with one `<section>` per slide, sized to the
feed format in `VISUAL_STYLE.md` (1080×1350 by default), each section with
`page-break-after: always`, and fonts large enough to read at thumbnail size. Use the owner's
tokens; never invent a palette when `VISUAL_STYLE.md` exists.

```bash
chrome --headless=new --no-pdf-header-footer --print-to-pdf=carousel.pdf file:///abs/path/carousel.html
```

Set `@page { size: 1080px 1350px; margin: 0 }` in the HTML so every slide is one page. Render a
PNG of the cover and one middle slide too, and check them at phone scale against the
`VISUAL_STYLE.md` checklist.

## 5. Hand-off

Save the PDF and the caption next to the draft file and set the draft status to `approved` only
after the user approves both. `$LINKEDIN_HARNESS/scripts/linkedin_publish.py` posts text only: the user uploads
the PDF in LinkedIn's document post flow by hand, with the approved caption. Archive the PDF and
caption with the post's URL afterwards.

## Output

The slide plan, then the slide copy and caption for approval, then the PDF path and the two
preview PNGs.
