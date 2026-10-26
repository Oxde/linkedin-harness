---
name: linkedin-outreach
description: Write a connection note and a short, honest follow-up sequence to one specific person on LinkedIn, only when there is a real reason to reach out now. Use when the user names a person they want to reach, wants an invite note, a first message, an intro request, or asks whether to follow up.
license: MIT
metadata:
  version: "1.0.0"
  repository: "https://github.com/Oxde/linkedin-harness"
---

# LinkedIn Outreach

Outreach works when the person can tell in one line that the message was written for them,
by someone worth knowing, about something real. Volume is the opposite of that. This skill
writes for one person at a time, and refuses when there is no reason.

Read first: `VOICE.md` (who the owner is, what they can honestly offer, what they never claim).

## The reason test

Get three things from the user before writing anything:

1. **Who:** name, role, company, and where the owner came across them.
2. **Why now:** a specific trigger the owner has actually seen. Something they posted,
   shipped, said in a talk, a shared contact who suggested it. Read that thing; quote one
   detail from it.
3. **What the owner wants:** a conversation, advice, an intro, a role, a sale. Say it plainly to
   the user; the first message can hold it back.

If there is no "why now", output `skip: no reason to write today` and suggest what would
create one (comment on their next post with the `linkedin-comment` skill, ship the thing
first). Never claim a connection, a common background, or familiarity with work the owner has not seen.

## The connection note

LinkedIn caps invite notes at 200 characters; show the count.

- One detail that proves the owner looked at their work.
- One line on who the owner is, in words a stranger understands.
- No ask. The note's only job is an easy "accept".

## After they accept

- **First message:** wait at least a day. Two to four sentences. Pick up the thread from the
  note, give one useful thing (a finding, a link to a primary source, an answer to a question
  they asked publicly), then one small, concrete ask. No meeting link, no deck.
- **One follow-up**, only if the owner has something new to add: a result, a relevant post, a
  fix to the thing they mentioned. "Just checking in" is not new.
- **A closing message**, if still nothing: short, says the owner will not write again, leaves
  the door open. Then stop.

That is the whole sequence. If any step has nothing real to say, skip that step.

## Write it

- Plain words, the jargon test, the owner's register from `VOICE.md`.
- Never claim results, clients or numbers the owner has not given; use `{{placeholder}}` and
  flag it.
- Run the `anti-ai-writing` pass on every message.

## Hand-off

The note with its character count, then each later message with when to send it and the
condition for sending it at all ("only if they reply", "only if X ships"). The user sends
every message and every invite by hand.

## Never

- Send, schedule or automate invites or messages, by API, browser or any tool. Automated
  outreach breaks LinkedIn's terms and puts the account at risk.
- Write a batch of near-identical notes to a list of people. One person, one message.
- Pitch in the connection note, or follow up more than the sequence above.
