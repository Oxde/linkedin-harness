# Contributing

- Keep the feed on the Python standard library. A new dependency needs a reason in the PR.
- New producers: one file in `feed/producers/`, a section in `sources.txt`, a fixture and a test
  in `feed/tests/`. A missing key or a failing source must skip with a message, never crash the run.
- Prompts and skills: never add a path where an agent posts, comments, reacts, connects or DMs
  without the user's exact approval.
- Do not commit personal voice files, drafts, archives, tokens, cookies or host-specific job ids.
- Run the tests before opening a PR:

  ```bash
  python3 -m unittest discover -s feed/tests -t .
  (cd dashboard && python3 -m unittest discover -s tests)
  python3 -m unittest discover -s scripts/tests
  ```
