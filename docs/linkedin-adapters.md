# Platform adapters

The writing system is platform-neutral. Voice, research, drafts, review passes, approval gates
and the learning loop work the same for LinkedIn, X, Threads, Bluesky, Reddit or a newsletter.
What changes per platform is the adapter: authentication, publishing, reading the feed,
comments, and analytics. The core never depends on browser cookies, one provider or one network's
API.

## Reality check

LinkedIn has an official API, but read access for personal creator accounts is restricted. A
complete creator workflow usually needs more than one adapter.

## 1. Publishing: OAuth through the official API or a managed provider

The user clicks a consent link once in their own browser. The provider stores the access token;
the agent never sees a password.

- `w_member_social`: publish and manage posts for the signed-in member.
- `w_member_social_feed`: comments and reactions for the signed-in member.

Managed OAuth providers (for example Maton, Composio, or your own small OAuth app) save you from
running the token flow yourself. Every post or comment still needs the user's exact approval.

## 2. Own-post metrics and research: a logged-in browser bridge

The free practical option for a personal account.

- The user logs into LinkedIn once in the persistent browser profile the bridge uses (for
  example OpenCLI's browser bridge).
- The bridge reuses that session slowly and read-only: own-post numbers, timeline and search,
  visible comments.
- No password or cookie is pasted into chat or stored by the harness.
- Stop on any CAPTCHA or security challenge.

`scripts/collect_linkedin_metrics.py` is this adapter for own-post numbers. It needs
`LINKEDIN_ACTIVITY_URL` and `LINKEDIN_METRICS_DIR`.

Cons: the UI and the session can change; no high-volume scraping.

## 3. Structured third-party data APIs

Use one when the browser route is too brittle or the system needs dependable JSON for public
posts and comments. The harness uses Apify (`harvestapi/linkedin-post-search`,
`apify/instagram-reel-scraper`) for the `post` and `video` lanes when `APIFY_API_KEY` is set.
Other options people use: LinkedAPI.io, AgntData, ScrapeCreators, Bright Data.

They all need an account and a key. Check privacy, price, rate limits and terms before adopting
one, and run the same small query set through it first to judge coverage and freshness.

## 4. Official member read API

`r_member_social`, `r_member_social_feed` and member post analytics are restricted and
approval-gated. Company pages are easier: the Community Management API covers organization
posts, comments, reactions and analytics for users with a page role. Do not build on the
assumption that every user can get the member scopes.

## Observation rules

- Read-only by default.
- Never automate likes, comments, DMs, connections or follows.
- Read slowly and only the owner's account or a small deliberate list of public posts.
- Stop on CAPTCHA or a security challenge.
- Never claim live LinkedIn scanning works until a real response proves it.

## Recommended onboarding

1. Fill `VOICE.md`.
2. Connect publishing OAuth once.
3. Optionally log into LinkedIn once in a browser bridge for read-only metrics.
4. Decide whether comments are manual paste only or an approval-gated write adapter.
5. Add a structured data API only after the free route proves too weak.

## Other platforms

One adapter per platform: X (primary-source fetcher plus a posting adapter), Bluesky (official
API), Reddit (API with stricter community rules), newsletter or blog (the CMS API).
