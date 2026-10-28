# pr-review-kit (Claude Code plugin)

A PR review agent for Claude Code. Give it a pull request and it:

1. reviews it with two skills (`pr-reviewer` for process and context, `pr-reviewer-spillwave` for the code),
2. checks every finding against the real diff and drops anything it can't point to a file and line for,
3. posts a short, teammate-style review on GitHub (request changes, comment or approve),
4. posts the full report to Discord, with the report attached as a `.md` file.

After reviewing several PRs, the `pr-batch-summary` skill posts one roundup to Discord, grouped by merge readiness, with merge order.

This folder is a copy of the plugin from [0xLimerence/pr-review-plugin](https://github.com/0xLimerence/pr-review-plugin) (commit `5a7fec3`). That repo is the marketplace (`pr-review-tools`) to install from on any device.

## One-prompt install

Paste this into Claude Code and it installs everything for you:

```text
Install the pr-review-kit plugin from https://github.com/0xLimerence/pr-review-plugin:
1. Run `claude plugin marketplace add 0xLimerence/pr-review-plugin`, then `claude plugin install pr-review-kit@pr-review-tools`.
2. Check that `gh auth status`, `python --version` and `git --version` work. Tell me about anything missing.
3. Ask me for my two Discord webhook URLs, then merge them into the `env` block of ~/.claude/settings.json
   as DISCORD_PR_REVIEW_WEBHOOK and DISCORD_PR_SUMMARY_WEBHOOK, keeping every existing setting.
4. Tell me to restart Claude Code when done.
```

## Quick start

```text
/plugin marketplace add 0xLimerence/pr-review-plugin
/plugin install pr-review-kit@pr-review-tools
```

Add the two Discord webhooks to `~/.claude/settings.json`, restart Claude Code, then ask:

```text
Review https://github.com/<owner>/<repo>/pull/123 with the pr-review agent
```

To try this copy without the marketplace: `claude --plugin-dir ./Plugins/pr-review-kit`.

Full steps: [docs/installation.md](docs/installation.md).

## What's inside

| Component | Name in Claude Code | Purpose |
| --- | --- | --- |
| Agent | `pr-review-kit:pr-review` | Runs the whole review and posts it |
| Skill | `pr-review-kit:pr-reviewer` | Linked issue, pre-PR criteria, related or conflicting PRs, diff review. Also carries the posting scripts |
| Skill | `pr-review-kit:pr-reviewer-spillwave` | Fetches PR data with `gh`, reviews against its criteria |
| Skill | `pr-review-kit:pr-batch-summary` | One Discord roundup after reviewing several PRs |
| Scripts | `discord_post.py`, `box_table.py` | Discord posting and box-drawing tables (Python standard library only) |

## Requirements

- Claude Code with plugin support
- GitHub CLI `gh`, signed in (`gh auth status`)
- Python 3
- git
- Two Discord webhooks (one for single reviews, one for batch summaries)

## Docs

- [Installation](docs/installation.md): install on a device, set the webhooks, update, uninstall
- [Usage](docs/usage.md): how to ask for a review or a batch summary, what you get back
- [How it works](docs/how-it-works.md): the steps, merge readiness, review event rules, output formats
- [Customizing](docs/customizing.md): changing the formats, the reviewer voice, the plugin version
- [Troubleshooting](docs/troubleshooting.md): common errors and fixes

## Layout

```text
Plugins/pr-review-kit/
├── .claude-plugin/plugin.json       plugin "pr-review-kit"
├── README.md                        this file
├── docs/                            guides
├── agents/pr-review.md
└── skills/
    ├── pr-reviewer/                 SKILL.md, references/, scripts/
    ├── pr-reviewer-spillwave/       SKILL.md, references/, scripts/
    └── pr-batch-summary/            SKILL.md, scripts/
```

## Security

- No webhook URLs or tokens are stored in the plugin. Webhooks come from environment variables on each device.
- The agent writes to GitHub only once per review (`gh pr review`), never pushes code, and never posts the internal report to GitHub.
- On your own PR it only comments (GitHub refuses approve or request changes from the author), so it never self-approves.
