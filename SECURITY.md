# Security

Report a vulnerability privately through GitHub's "Report a vulnerability" on this repository.
Please do not open a public issue for it.

Things that are in scope: the feed service's auth (`FEED_TOKEN`), the dashboard's handling of
URLs from feed items, the producers' parsing of untrusted pages, and any place an agent prompt
could be steered into an external action without the user's approval.
