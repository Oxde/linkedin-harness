---
name: linkedin-inbox
description: Sort LinkedIn DMs and connection requests into what deserves a reply and what does not, spot automated outreach sequences, and draft only the replies worth sending. Use when the user shares a batch of messages or invites, asks whether a message deserves an answer or is automated, or has a backlog of LinkedIn messages.
license: MIT
metadata:
  version: "1.0.0"
  repository: "https://github.com/Oxde/linkedin-harness"
---

# LinkedIn Inbox

The point of triage is to find the few messages that matter fast, and to stop the rest from
costing attention. Reading is cheap; replying is the expensive part, so draft only what earns it.

Read first: `VOICE.md` (what the owner does, who they help, what they are open to right now).

## Input

Pasted messages or screenshots, newest last, with the sender's name and headline where
visible. Never open the inbox in a browser or through any tool on the user's behalf.

## Buckets

Print the counts first, then work the list:

- **Opportunity** — a real problem the owner solves, a collaboration, a paid ask.
- **Role** — a recruiter or hiring manager with an actual position.
- **Peer** — someone in the lane writing to the owner personally.
- **Favor** — advice, an intro, feedback, "a quick call".
- **Automated** — a sequence or a template. No reply.

## Spotting a sequence

Call it automated only with evidence. Look for a combination, not one sign:

- no detail about the owner beyond job title or industry;
- a message that lands minutes after the invite is accepted;
- a meeting link or a deck in the first message;
- "following up" with nothing new, on a fixed rhythm;
- merge-field slips: wrong name, wrong company, odd capitalization.

Name the signs you saw next to each one, so the user can trust the call.

## Replies

- **Opportunity:** answer the question they asked, concretely, as if the answer alone were the
  reply. If it fits, one sentence on how to continue. If it does not, say so and point
  somewhere useful.
- **Role:** if it might fit, ask only what the message left out (scope, level, location,
  compensation range). If not, one polite line.
- **Peer:** a real reply in the owner's voice. Short is fine.
- **Favor:** if it is specific and small, just help in the reply. If it is vague ("pick your
  brain"), give the one useful answer in two lines and decline the call kindly.
- **Declines** are short and final. No fake "later".
- Never invent availability, prices, or facts about the owner's work; use `{{placeholder}}` and
  flag it.
- Plain words, then the `anti-ai-writing` pass on every draft.

## Connection requests

Accept-worthy: in the lane, a real person, a note or a shared context that makes sense. Decline
or ignore: empty profiles, obvious sequences, sellers with no context. Give one line of reason
per request. The user clicks accept or ignore themselves.

## Hand-off

Counts, then drafts grouped by bucket, each with the sender and their message summarized in
one line above it. Automated and declined items get one line each, no draft. The user sends
every reply by hand.

## Never

- Send, accept, archive or report anything through a browser or API.
- Copy private message content into the repo, the feed or any shared file.
- Reply to an automated sequence, even to say no.
