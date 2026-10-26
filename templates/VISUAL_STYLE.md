---
title: Visual style
status: draft
---

# Visual style (outline, fill in your own)

A self-contained guide any agent can follow to make still images for your posts: feed images,
carousels, covers. Fill every section with exact values. If something is not covered, the agent
should choose the quieter option.

**The world in one line:** <describe the look in one sentence>

## 1. Formats

A table of sizes per use (feed post, square, story/cover, carousel slide), the safe area, and
the margins.

## 2. Colour

Tokens with hex values and the one job each colour has (background, brand, text, secondary
text, "wrong/broken", small accents). Rules: which colour dominates, what is never allowed
(gradients, glow, light theme...).

## 3. Type

Faces, weights and sizes per role (title, the one keyword, body, labels and data, source line),
and the type rules (how many keywords per image, minimum sizes, what never uses mono).

## 4. Material

The recurring parts: background texture, frames and tags, verdict block, buttons, connectors,
rules, props.

## 5. Mascot or recurring character (optional)

If you use one: exact spec (pixel map, sizes, faces, poses), when to use it and when not.

## 6. Composition

Where the header, title, keyword, hero, takeaway and source line sit on the canvas. One idea per
image.

## 7. Picking the picture

Your order of preference, for example: real proof (screen, terminal, number) → the literal thing
→ a typed diagram → the character acting out the claim → a metaphor only when it carries
information.

## 8. Copy on images

Headline rules, source and date lines, your signature.

## 9. Carousels

Slide 1, middle slides, last slide, progress marks.

## 10. Rendering

How images are produced. A common setup is exact-size HTML rendered by headless Chrome:

```bash
chrome --headless=new --hide-scrollbars --window-size=1080,1350 --screenshot=out.png file:///abs/path/post.html
```

## 11. Check before delivering

A checklist the agent runs on every rendered image, at phone scale.
