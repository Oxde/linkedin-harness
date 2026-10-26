# Posting to LinkedIn for free

You don't need a paid scheduler or a data provider to publish. LinkedIn's own API lets any member
post to their own profile through a free developer app. This guide sets that up once, then
publishes approved drafts with `scripts/linkedin_publish.py`.

```text
draft approved by you → hash of the exact text → dry run → --post → live URL → archive
```

## What you get, and what you don't

| | free official API |
|---|---|
| post text to your own profile | yes (`w_member_social`) |
| post as a company page | only with the Community Management API (needs approval) |
| read your feed, other people's posts, your analytics | no; use the browser bridge in `docs/linkedin-adapters.md` |
| comment and react | needs `w_member_social_feed`, not part of the free self-serve products |

## 1. Create the app (once, about 10 minutes)

1. Go to <https://www.linkedin.com/developers/apps> and click **Create app**.
2. App name: anything (for example "my-linkedin-harness"). LinkedIn requires a **company page**
   to attach the app to; if you don't have one, create a small page for yourself first. The app
   does not post as that page.
3. Upload any logo, accept the terms, create.
4. On the **Products** tab, request:
   - **Share on LinkedIn** → gives `w_member_social`
   - **Sign In with LinkedIn using OpenID Connect** → gives `openid`, `profile` (used to find
     your member id)

   Both are self-serve and usually approved instantly.
5. On the **Auth** tab, add `https://www.linkedin.com/developers/tools/oauth/redirect` as an
   authorized redirect URL (the token generator below uses it).

## 2. Get an access token

The simplest path needs no server:

1. Open LinkedIn's OAuth token generator: <https://www.linkedin.com/developers/tools/oauth/token-generator>.
2. Pick your app, tick `openid`, `profile` and `w_member_social`, and generate.
3. Sign in and allow. Copy the access token.

Put it in your `.env` (never in Git, never in a chat):

```bash
LINKEDIN_ACCESS_TOKEN=<token>
```

The token lasts **60 days**. Put a reminder in your calendar and generate a new one before it
expires; a publish with an expired token fails with HTTP 401 and says so.

Optional:

```bash
LINKEDIN_AUTHOR_URN=urn:li:person:<id>   # skips the /v2/userinfo lookup on every post
LINKEDIN_API_VERSION=202609              # YYYYMM; default is last month
```

To find your id once:

```bash
curl -s -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" https://api.linkedin.com/v2/userinfo   # "sub" is <id>
```

## 3. Publish an approved draft

The script never posts text that differs from what you approved.

```bash
set -a; . ./.env; set +a

# put exactly the approved text into a file, then:
python3 scripts/linkedin_publish.py post.txt --hash-only           # → <hash>, approve this exact text
python3 scripts/linkedin_publish.py post.txt --sha256 <hash>        # dry run: shows the payload
python3 scripts/linkedin_publish.py post.txt --sha256 <hash> --post # publishes, prints the live URL
```

What it checks before sending: the text is not empty and under 3,000 characters, the hash matches,
`--post` is present, and the token is set. Any error from LinkedIn is printed with the status code
and the response body.

## 4. How the agent uses it

The `linkedin-writer` skill's approval rule maps onto these flags:

1. The agent shows you the final text and its hash (`--hash-only`).
2. You reply with an explicit "post now" for that text.
3. The agent runs the dry run, then `--post` with the hash you approved.
4. It opens the returned URL to check the post is live, saves the exact text and the URL under
   `archive/`, adds an entry to `archive/POSTS.md`, and sets the feed item to `posted`.

Never give an agent a standing instruction to post. Each post is its own approval.

## Formatting gotchas

- LinkedIn's API treats `\ | { } @ [ ] ( ) < > # * _ ~` as markup. Unescaped, a `(` can silently
  cut the post short. The script escapes all of them, so they show as plain characters.
- Because of that, `#tag` appears as plain text, not a clickable hashtag, and `@name` is not a
  mention. Write tags and mentions in by hand after posting if you need them.
- Line breaks are kept. Bold and italics don't exist on LinkedIn; Unicode "bold letters" hurt
  screen readers and search, so don't use them.
- Images, documents (carousels) and video need an upload step first (the Images, Documents and
  Videos APIs). The script posts text only; post visuals by hand or extend it.

## Rate limits and terms

The member limit is generous for one person (well above a few posts a day). Posting for other
people with your app, or automating engagement, breaks LinkedIn's API terms; the harness doesn't
do either.
