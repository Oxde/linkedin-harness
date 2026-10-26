# Deploy the feed to Railway

The feed service and the dashboard run in one small container. Collection runs as a second
service from the same image on a cron schedule. Any container host works the same way; this is
the Railway path the scripts support.

## What gets deployed

`feed/deploy.sh` stages a small directory and runs `railway up` from it:

```
Dockerfile           python:3.12-alpine, runs `python -m feed.service`
railway.toml         healthcheck /api/health (or railway.collect.toml for the cron service)
feed/                the package, without tests or databases
public/              dashboard/public/
```

The service stores SQLite at `/data/feed.db`, so it needs a volume mounted at `/data`.

## Steps

1. Create a Railway project with two services, for example `linkedin-harness` (the API and
   dashboard) and `feed-collect` (the cron). Add a volume at `/data` to `linkedin-harness`.
2. Create a **project token** for the project. Keep it in your shell or a local env file, never in
   Git.
3. Set the service variables:

   ```bash
   export RAILWAY_TOKEN=<project token>
   railway variables --service linkedin-harness --set "FEED_TOKEN=$(openssl rand -hex 24)" --set FEED_DB=/data/feed.db
   ```

   On `feed-collect`: `FEED_URL=http://linkedin-harness.railway.internal:8080`,
   `FEED_TOKEN=${{linkedin-harness.FEED_TOKEN}}`, and optionally `GH_TOKEN`, `APIFY_API_KEY`.
4. Deploy both:

   ```bash
   bash feed/deploy.sh             # API + dashboard
   bash feed/deploy.sh --collect   # collection cron, same image
   ```

   `RAILWAY_SERVICE` overrides the service name.
5. Generate a public domain for `linkedin-harness` and check it:

   ```bash
   curl -s "https://<your domain>/api/health"
   ```

6. Put that URL and the token into your local `.env` as `FEED_URL` / `FEED_TOKEN` for the
   scheduled jobs.

## Cron service settings

The cron service needs start command `python -m feed.collect`, cron schedule `0 7,13 * * *`
(UTC) and restart policy `NEVER`. `railway up` does not always apply `startCommand` and
`cronSchedule` from the staged `railway.toml`; if the service ignores them, set them on the
service in the Railway dashboard, or through the GraphQL API with `serviceInstanceUpdate`.

Some RSS hosts rate-limit cloud IP ranges. The news producer logs the failure and carries on.

## Run it without Railway

```bash
FEED_TOKEN=... FEED_DB=/persistent/feed.db PORT=8080 python3 -m feed.service
```

Any host that runs a Python 3.12 process with a persistent disk is enough. The Dockerfile expects
the staged layout (`public/` at the top); build from the directory `feed/deploy.sh` stages, or
change its `COPY public` line to `COPY dashboard/public /app/public` to build from the checkout.
