# Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `/agents` doesn't list `pr-review-kit:pr-review` | Plugin not installed or Claude Code not restarted | `/plugin` to check it's enabled, then restart |
| Agent and skills show up twice | Personal copies still in `~/.claude/agents` and `~/.claude/skills` | Delete the personal copies, or ignore the unprefixed ones |
| `DISCORD_PR_REVIEW_WEBHOOK is not set` (or `..._SUMMARY_...`) | Missing `env` entry | Add it to `~/.claude/settings.json` and restart Claude Code |
| `Report name must match ...` | Report file not named `pr-review-<N>.md` (or `pr-review-summary-<YYYY-MM-DD>.md` with `--batch`) | Rename, rerun |
| `Discord rate limit: gave up after 5 tries` | Too many posts at once | Wait a minute, post by hand with the same command |
| HTTP 401/404 from Discord | Webhook deleted or URL wrong | Create a new webhook, update `settings.json` |
| `gh: To get started with GitHub CLI, please run: gh auth login` | `gh` not signed in | `gh auth login` |
| `Can not approve your own pull request` / `Can not request changes on your own pull request` | The `gh` user is the PR author | Expected: the agent should use `--comment`. Ask for a comment review, and get someone else to approve |
| `fetch_pr_data.py` fails | No access to the repo, or `gh` missing from PATH | `gh repo view <owner/repo>` to check access |
| `python` not found (macOS/Linux) | Only `python3` installed | Tell the agent to use `python3`, or alias `python` |
| Review missing a finding you expected | Findings without a file and line are dropped on purpose | Ask the agent to look at that file specifically |
| Agent stops partway | Hit `maxTurns: 60` on a very large PR | Raise `maxTurns` in the agent front matter, or review in parts |

Still stuck: run with `--dry-run` on `discord_post.py` to see exactly what would be sent, and check the temp folder the agent reports for the three output files.
