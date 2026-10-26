---
name: anti-ai-writing
description: Remove the phrases, shapes and habits that make a post read as machine-written. Use on every LinkedIn draft, comment and reply before it goes to the user for approval, and when the user says a draft "sounds like AI".
license: MIT
metadata:
  version: "1.0.0"
  repository: "https://github.com/Oxde/linkedin-harness"
---

# Anti-AI writing

A reader decides in two lines whether a person wrote this. These rules are the checks that
decide it. They are generic: the owner's `VOICE.md` adds their own banned words and wins on any
conflict.

Run this as a separate pass after the draft exists. Do not try to write "anti-AI" from the
start; write the point, then strip the tells.

## 1. Banned words

Corporate filler: leverage, synergy, ecosystem, robust, seamless, optimize, streamline,
empower, unlock, elevate, supercharge, game-changer, cutting-edge, best-in-class, holistic,
paradigm, transformative, revolutionize.

Model favourites: delve, tapestry, testament, landscape (for a market), realm, navigate (for a
problem), journey (for a process), crucial, pivotal, vibrant, intricate, multifaceted, nuanced,
underscore, foster, harness (as a verb), in today's fast-paced world.

Hype on LinkedIn: insane, mind-blowing, holy shit, this changes everything, must-have, 🚨, 🔥 as
punctuation. The number does that job.

## 2. Banned shapes

- **The fake contrast.** "It's not X, it's Y." "The weird part wasn't X, it was Y." "This isn't
  about X. It's about Y." Say Y.
- **The staged reveal.** A one-word line followed by a colon or a line break for drama: "The
  result?" "The catch:" "Here's the thing." Put the result in the sentence.
- **The rule of three by reflex.** Three adjectives, three parallel clauses, three bullets when
  the content has two or four.
- **The generic moral.** "This matters." "The future is X." "What nobody tells you." "Let that
  sink in." End on the strongest fact or the rule, not on a summary of the post.
- **The engagement question.** "What do you think?" "Agree?" A question only when the post
  genuinely does not know the answer and the reader does.
- **The summary close.** "In short," "Ultimately," "At the end of the day," a last paragraph
  that repeats the first.
- **Hedge stacks.** "It might potentially help some teams to possibly..." One hedge, where the
  uncertainty is real.
- **Em-dash chains.** One dash per post at most. Use a full stop.
- **Symmetric lists.** Every bullet the same length and grammar. Real notes are uneven.

## 3. Habits that sound like a model even with clean words

- Explaining the point instead of showing one fact, cost, incident or mechanism.
- Every sentence the same length. Mix short lines with one longer one.
- No named actor, no number, no date anywhere in the post.
- Polishing the user's rough draft into analyst prose. If the user gave a draft, keep its order,
  its rhythm and its roughness; fix facts and mechanics only.
- Praise of the source ("a fascinating paper", "an impressive release"). Say what it did.
- Jargon a smart friend outside the field would not know, left unexplained.

## 4. The check

Read the draft once per question. Fix, then read again.

1. Does line one name a thing and carry a number, a behaviour or a real pain?
2. Is any word from section 1 or the owner's banned list in it?
3. Is any shape from section 2 in it?
4. Could a generic AI-content account have written this exact post? If yes, what fact, receipt or
   opinion only the owner has is missing?
5. Read it aloud. Where would a person never say this sentence out loud?

Report the pass as a short list of what changed. Never claim a draft "passes" without listing
the checks you ran.
