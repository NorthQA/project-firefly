# How it works

The full rules are in `Plugins/pr-review-kit/agents/pr-review.md`. This is the overview.

## Steps

1. **`pr-reviewer` skill:** linked issue, pre-PR criteria (branch name, base, description), related or conflicting issues and open PRs, and a diff review. Its branch, commit, push and PR-opening parts are skipped.
2. **`pr-reviewer-spillwave` skill:** `scripts/fetch_pr_data.py <url> --no-clone --output-dir <temp>` pulls metadata, diff, comments and commits with `gh`, then the diff is checked against `references/review_criteria.md`. Its file generation, inline comments and `/send` commands are skipped.
3. **Verify:** every finding is checked against the diff or source. No file and line, no finding. Duplicates from the two skills are merged.
4. **Report** to `pr-review-<N>.md`, **summary** to `pr-review-<N>-summary.txt`.
5. **Discord:** `discord_post.py <report> <summary>` posts once to `DISCORD_PR_REVIEW_WEBHOOK`.
6. **GitHub:** the short review to `pr-review-<N>-github.md`, then `gh pr review <N> --repo <owner/repo> <event> --body-file ...`, once.
7. **Return** the result to the caller.

## Severity

- **Blocker:** conflicts, broken behaviour, security holes.
- **Important:** must be fixed before merge but not breaking.
- **Nit:** small, optional or quick fixes.

## Merge readiness

Exactly one, worded the same everywhere:

| Readiness | When |
| --- | --- |
| Ready to merge | No findings above nit, and the nits are optional |
| Merge after nits are fixed | Only nits, but they should be fixed first |
| Merge after requested changes are fixed | Important findings, no blockers |
| Not ready to merge | Any blocker, or a decision is needed first |

A merge-order dependency is added when there is one ("after #123 merges").

## GitHub review event

| Readiness | Event |
| --- | --- |
| Not ready, or after requested changes | `--request-changes` |
| After nits | `--comment` |
| Ready | `--approve` |
| PR author is the `gh` user | always `--comment` |

The body is short: one line on what the PR gets right, then **Needs changes before merge** (numbered, with `path:line`, why and the fix) and **Smaller things** (one-line bullets). No headings, no report scaffolding.

## Discord

- **Message:** title, link, merge readiness, verdict with counts, 1 to 3 deciding findings, "Full review attached." Under 1500 characters.
- **Attachment:** the full report (Summary, Blockers, Important, Nits, Pre-PR checks, Good).
- Discord doesn't render tables, so messages use headings, bold and bullets only.

## Scripts

### `discord_post.py`

```text
python discord_post.py <pr-review-<N>.md> <summary.txt> [--dry-run]
python discord_post.py --batch <pr-review-summary-<YYYY-MM-DD>.md> <summary.txt> [--dry-run]
```

- Single review: posts to `DISCORD_PR_REVIEW_WEBHOOK`. Batch: `DISCORD_PR_SUMMARY_WEBHOOK`.
- The report file name must match the pattern above.
- Messages over Discord's 2000-character limit are split on line boundaries (code blocks are closed and reopened); the file goes on the last message.
- On a 429 it backs off and retries, up to 5 tries.
- `--dry-run` prints what would be sent.

### `box_table.py`

```text
python box_table.py <table.json>
```

JSON: `{"widths": [22, 10, 9, 42], "headers": ["PR", "Verdict", "Blocker / Important / Nit", "Main issue"], "rows": [[...], ...]}`. Cells wrap to their column width. Paste the output inside a fenced `text` block.

Both scripts use only the Python standard library.
