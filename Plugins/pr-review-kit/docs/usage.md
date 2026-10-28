# Usage

## Review one PR

Ask Claude Code in plain words. Any of these work:

```text
Review https://github.com/<owner>/<repo>/pull/123 with the pr-review agent
Use the pr-review agent on PR #123
Review PR 123 (inside the repo's folder; the repo is taken from `gh repo view`)
```

The agent needs a PR URL, or a PR number plus a repo. Without either it stops and says what's missing.

It runs in the background and reports back with:

- the **verdict** (Approve, Request changes, Needs discussion),
- the **merge readiness** (one of four, see [how-it-works.md](how-it-works.md)),
- counts of blocker, important and nit findings,
- whether the Discord post worked,
- the GitHub review event used and the review's URL.

Useful things to add to the request:

- Context the diff doesn't show ("this was written with Claude in this session, don't approve from my account", "the two config tests fail only locally").
- What to look at closely ("check the billing routes for consent bypasses").
- House rules ("no em dashes", "no attribution lines").

## Review several PRs

Ask for each, or all at once:

```text
Review #121, #122 and #123 with the pr-review agent
```

Each PR gets its own GitHub review and Discord post.

## Batch summary

After more than one review in a session, the `pr-review-kit:pr-batch-summary` skill posts one roundup to `DISCORD_PR_SUMMARY_WEBHOOK`:

```text
Post the batch summary for today's reviews
```

It groups PRs into Not ready, After requested changes, After nits and Ready, gives a merge order and what to watch out for, and attaches `pr-review-summary-<YYYY-MM-DD>.md` with box-drawing tables.

## Files it writes

All in a temp or scratch folder, never in your repo:

| File | Goes to |
| --- | --- |
| `pr-review-<N>.md` | Full report, Discord attachment |
| `pr-review-<N>-summary.txt` | Discord message |
| `pr-review-<N>-github.md` | GitHub review body |
| `pr-review-summary-<date>.md` | Batch summary attachment |

## What it never does

- Change code, commit, push or open PRs.
- Post the internal report to GitHub.
- Approve your own PR (it comments instead).
- Retry a failed post a different way: it returns the error and the file paths so you can post by hand.
