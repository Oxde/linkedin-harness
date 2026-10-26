---
name: feed
description: Resolve the user's pick from the latest research menu, mark it in the feed service, and hand it to the LinkedIn writer.
license: MIT
metadata:
  version: "1.0.0"
  repository: "https://github.com/Oxde/linkedin-harness"
---

# feed — picking from the research menu

The `feed-menu` job sends a numbered research menu into this chat once or twice a day. Each item
in that message maps to a feed `id` (the menu job received them as `id: <hex>` lines). The user
replies in their own words, often by voice: "news post about 2", "let's do the skill one",
"video 3", "skip all".

`$LINKEDIN_HARNESS` is the path of the linkedin-harness checkout. `feed/ctl.sh` finds the feed
URL and token itself (from the shell or from `$LINKEDIN_HARNESS_ENV`, default `<checkout>/.env`).

## When the user refers to a menu item

1. Find the most recent research menu in this chat and resolve the item they mean: by number,
   by lane ("the skill one"), by topic words, or by the company name. If two items could match,
   ask one short question naming both; otherwise do not ask.
2. Record the pick, quoting their words:

   bash "$LINKEDIN_HARNESS/feed/ctl.sh" pick <id> --note "<the user's words>"

3. Start the `linkedin-writer` flow with this brief: the item's title, url, the `Insight` and
   `Audience` lines from the menu, and the user's note. The writer's own rules apply unchanged
   (voice, anti-AI-writing pass, visual decision, exact approval before any publish).
4. When the post is published through the writer's publish step, run
   `bash "$LINKEDIN_HARNESS/feed/ctl.sh" set-status <id> posted`. When the user says skip, drop,
   or no, run `bash "$LINKEDIN_HARNESS/feed/ctl.sh" set-status <id> skipped`. If they ask for a
   video from it, record `--note "video: ..."` on the pick and leave the status `picked`; a video
   tool can read picked items from the API.

## When the user answers the skill desk

The `skill-desk` job posts judged candidates ("Verdict: strong / watch") instead of a draft.
"draft 2" means: record the pick as above, then write the post (with the `skill-posts` skill if
the owner has one) and go through the writer's approval flow. "test 2" means: run it in a scratch
directory with no secrets first (see the `skill-radar` safety gates), then draft with the run as
the receipt. "skip 2" or "skip all": `set-status <id> skipped --why "<the user's reason, verbatim>"`
so the feed remembers their bar.

## Never

- Publish, comment, react, connect, or DM. The writer's approval flow is the only path.
- Invent an id. If the menu is gone from context, run `bash "$LINKEDIN_HARNESS/feed/ctl.sh" list`
  to see offered, shown and picked items with their ids, or ask the user which one they meant.
  Never run `menu` for this.
- Reply with the whole menu again. One line confirming the pick is enough.
