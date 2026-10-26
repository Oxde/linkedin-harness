# The research feed

A small hosted store of research items (news, agent skills, repos, public discussions, reels)
that producers fill on a schedule, plus a menu the owner picks from in chat. The agents do the
research; the owner only chooses.

Python standard library only. Nothing to install.

```
feed/
  producers/  news.py skills.py repos.py posts.py linkedin.py videos.py
              public metadata → JSON lines (no LLM, nothing installed or executed)
  collect.py  runs every producer and posts the items to the service
  store.py    SQLite: dedupe, statuses, menus, stats
  service.py  HTTP API + serves the dashboard
  feedctl.py  CLI client used by the scheduled jobs and by the chat agent
  sources.txt channels, feeds, queries, watchlists (edit this, not the code)
  prompts/    the agent prompts for the menu, skill desk and video desk jobs
  run_*.sh    scheduler entry points; ctl.sh is the feedctl wrapper
```

## Lanes

| lane | producer | sources | needs |
|---|---|---|---|
| `news` | `news.py` | public Telegram channels (`t.me/s/<channel>`), RSS and Atom feeds | — |
| `skill` | `skills.py` | ClawHub, skills.sh | — |
| `repo` | `repos.py` | GitHub search, rising repos (created in the last 14 days with stars), a watchlist | `GH_TOKEN` optional, raises the rate limit |
| `post` | `posts.py`, `linkedin.py` | Hacker News (Algolia), Lobsters, LinkedIn post search | `APIFY_API_KEY` for LinkedIn |
| `video` | `videos.py` | Instagram reels of watched creators | `APIFY_API_KEY` |

A producer without its key, or with an empty section in `sources.txt`, skips itself and says so
on stderr. A failing source never stops the other producers.

## Statuses

`new → offered → shown → picked → drafted → posted`, plus `skipped` and `expired`.

- `menu` returns unseen top items per lane and marks them `offered`, so nothing repeats.
- The menu agent writes back `shown` (listed, with an insight and a why) or `skipped`.
- The chat agent writes `picked` with the owner's words, then `posted` or `skipped`.
- Skip reasons are fed back into the next skill desk as "the owner's bar".

## Run locally

```bash
FEED_ALLOW_NO_TOKEN=1 FEED_DB=./feed.db python3 -m feed.service      # http://127.0.0.1:4872
python3 -m feed.collect                                               # fill it
python3 -m feed.feedctl menu                                          # print a menu
python3 -m feed.feedctl set-status <id> shown --insight "..." --why "..."
python3 -m feed.feedctl pick <id> --note "news post about 2"
python3 -m feed.feedctl list
python3 -m feed.feedctl top --lanes skill,repo --n 6
python3 -m feed.feedctl videos --days 7
python3 -m feed.feedctl stats
```

The dashboard is served at `/` and reads the API with the token you paste into it.

## API

All `/api/*` routes except `/api/health` need `Authorization: Bearer $FEED_TOKEN`.

| route | method | purpose |
|---|---|---|
| `/api/health` | GET | `{"ok": true, "items": n}` |
| `/api/ingest` | POST | `{"items": [...]}` or JSON lines → counts; also expires stale items |
| `/api/menu?quota=news=4,skill=2,repo=2` | GET | unseen top items per lane; marks them `offered` |
| `/api/items?status=&lane=&since=&limit=` | GET | list |
| `/api/items/{id}` | PATCH | `status`, `insight`, `why`, `pick_note`, `kind` |
| `/api/stats?days=7` | GET | per-lane counts, sources by pick rate, last collect per producer |

## Environment

| variable | used by | meaning |
|---|---|---|
| `FEED_TOKEN` | service, clients | shared bearer token; the service refuses to start without it unless `FEED_ALLOW_NO_TOKEN=1` |
| `FEED_URL` | clients | where the service runs |
| `FEED_DB` | service | SQLite path (`/data/feed.db` in the container) |
| `FEED_STATIC` | service | directory served at `/` (default `dashboard/public`) |
| `PORT` | service | listen port |
| `GH_TOKEN` | repos producer | optional GitHub token |
| `APIFY_API_KEY` | linkedin, videos producers | optional; those lanes skip without it |
| `LINKEDIN_HARNESS` | run scripts | path of the checkout, when a script runs from a copy elsewhere |
| `LINKEDIN_HARNESS_ENV` | run scripts | env file with `FEED_URL` / `FEED_TOKEN` (default `<checkout>/.env`) |

## Tests

```bash
python3 -m unittest discover -s feed/tests -t .
```

## Design notes

- **Heuristics first, one small LLM pass.** Producers score items with keyword weights and
  growth; the menu agent sees at most a few dozen items and does one verification fetch each.
- **The menu is short or silent.** If nothing passes, the job replies `[SILENT]`. A long or
  repetitive menu is the failure mode.
- **One owner column from the start.** The store has an `owner` column so a second user is a
  filter, not a migration. There are no accounts or billing.
- **Hostable or local.** The same service runs on a laptop or in a container; nothing depends
  on one machine's filesystem.
- **Leads are not facts.** Telegram and discussion items are leads; the post's facts come from
  the primary source.
