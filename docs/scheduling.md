# Scheduling the jobs

The harness is a set of scripts and prompts. Any scheduler that can run a shell script, and
optionally hand its output to an agent, can drive it: plain cron, a Claude Code routine, Hermes
Agent, n8n, GitHub Actions. This file is the contract; job ids, chat ids and tokens stay on the
host and never go into Git.

## The jobs

| job | suggested schedule | mode | script | prompt | output |
|---|---|---|---|---|---|
| `feed-collect` | `0 7,13 * * *` | no agent | `feed/run_collect.sh` | — | one summary line; failures to chat |
| `feed-menu` | `30 9,16 * * *` | agent | `feed/run_menu.sh` | `feed/prompts/menu.md` | the research menu, or `[SILENT]` |
| `skill-desk` | `0 11 * * 2,4` | agent + `skill-posts` | `feed/run_skill_desk.sh` | `feed/prompts/skill_desk.md` | two or three judged candidates |
| `video-desk` | `0 10 * * 1,4` | agent | `feed/run_video_desk.sh` | `feed/prompts/video_desk.md` | the week's reels, outliers, ideas |
| `feed-stats` | `0 18 * * 0` | no agent | `feed/run_stats.sh` | — | weekly stats |
| own-post metrics | every 30 min, daytime | no agent | `scripts/collect_linkedin_metrics.py` | — | `latest.json` + `snapshots.jsonl` |

An **agent** job runs the script, puts its stdout above the prompt, and sends the agent's reply
to the chat where the owner talks to their main agent, so a reply like "news post about 2" lands
next to the menu. The main agent has the `feed` and `linkedin-writer` skills installed and handles
the pick.

Rules that keep the menu useful:

- `feed-menu` attaches **no skills**. The writer skills add tens of thousands of characters the
  menu never uses.
- Don't run the menu script twice per tick (for example as a "monitor" and again as the job):
  every run marks items `offered`.
- An empty menu prints `Research menu: nothing new.` and the prompt makes the agent reply
  `[SILENT]`; configure the scheduler to drop `[SILENT]` replies.
- Run `feed-collect` in one place only: on the host (cron) or in the container (Railway cron),
  not both.

## Environment for the scripts

Each `run_*.sh` finds the checkout from its own location, so run them from the checkout. If your
scheduler copies scripts into its own directory, set `LINKEDIN_HARNESS` to the checkout path. The
feed URL and token come from the shell, or from `LINKEDIN_HARNESS_ENV` (default
`<checkout>/.env`, see `.env.example`).

## Plain cron + any CLI agent

`no agent` jobs are plain crontab lines:

```cron
0 7,13 * * *  cd /path/to/linkedin-harness && ./feed/run_collect.sh >> collect.log 2>&1
0 18 * * 0    cd /path/to/linkedin-harness && ./feed/run_stats.sh | your-notify-command
```

For an agent job, pipe the script output plus the prompt into a headless agent run and send the
reply on. With Claude Code:

```bash
cd /path/to/linkedin-harness && \
  { ./feed/run_menu.sh; echo; cat feed/prompts/menu.md; } | claude -p \
  | your-notify-command
```

The agent needs permission to run `feed/ctl.sh` and to fetch web pages; grant only those
(for Claude Code, through the project's `.claude/settings.json` allow list).

## Hermes Agent

Hermes runs `--script` output into the prompt and can deliver to Telegram. Copy the scripts
into the profile's scripts directory (Hermes refuses symlinks that point outside it), point
`LINKEDIN_HARNESS` at the checkout, and re-copy after every pull:

```bash
R=/path/to/linkedin-harness; P=~/.hermes/profiles/<profile>
for f in run_menu run_collect run_stats run_skill_desk run_video_desk ctl; do cp $R/feed/$f.sh $P/scripts/feed-$f.sh; done
for s in $(ls $R/skills); do mkdir -p $P/skills/$s && cp -r $R/skills/$s/. $P/skills/$s/; done
```

Put `LINKEDIN_HARNESS`, `FEED_URL` and `FEED_TOKEN` in the profile's `.env` (and set
`LINKEDIN_HARNESS_ENV` to that file). Then:

```bash
hermes -p <profile> cron create "30 9,16 * * *" --name feed-menu \
  --script feed-run_menu.sh --deliver telegram --failure-deliver telegram \
  "$(cat $R/feed/prompts/menu.md)"

hermes -p <profile> cron create "0 11 * * 2,4" --name skill-desk \
  --script feed-run_skill_desk.sh --skill skill-posts \
  --deliver telegram --failure-deliver telegram \
  "$(cat $R/feed/prompts/skill_desk.md)"

hermes -p <profile> cron create "0 10 * * 1,4" --name video-desk \
  --script feed-run_video_desk.sh --deliver telegram --failure-deliver telegram \
  "$(cat $R/feed/prompts/video_desk.md)"

hermes -p <profile> cron create "0 18 * * 0" --name feed-stats --no-agent \
  --script feed-run_stats.sh --deliver telegram

# only if collection does not run in the container:
hermes -p <profile> cron create "0 7,13 * * *" --name feed-collect --no-agent \
  --script feed-run_collect.sh --deliver local --failure-deliver telegram
```

The prompts call `bash "$LINKEDIN_HARNESS/feed/ctl.sh" ...`; make sure the agent's shell has
`LINKEDIN_HARNESS` set, or replace it in the prompt text with the path of your copied
`feed-ctl.sh`.
