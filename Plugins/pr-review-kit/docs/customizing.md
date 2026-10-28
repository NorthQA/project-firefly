# Customizing

All behaviour is plain Markdown and Python, so edit the files and reinstall or update.

| To change | Edit |
| --- | --- |
| Review steps, merge readiness, event rules, GitHub/Discord/report formats | `Plugins/pr-review-kit/agents/pr-review.md` |
| Reviewer voice (the "senior teammate" model; you can point it at a real review your team likes) | "GitHub review" section of the agent |
| Process checks (linked issue, branch rules, pre-PR criteria) | `skills/pr-reviewer/SKILL.md` |
| Code review criteria | `skills/pr-reviewer-spillwave/references/review_criteria.md` |
| Batch summary groups, emoji, table columns | `skills/pr-batch-summary/SKILL.md` |
| Discord limits, retry, splitting | `scripts/discord_post.py` (two copies: in `pr-reviewer/` and `pr-batch-summary/`; keep them identical) |
| Agent turn limit or model | Front matter of the agent (`maxTurns`, `model: inherit`) |

## Releasing a change

1. Bump `version` in `Plugins/pr-review-kit/.claude-plugin/plugin.json` and the matching entry in `.claude-plugin/marketplace.json`.
2. Validate:
   ```bash
   claude plugin validate pr-review-plugin
   claude plugin validate project-firefly/Plugins/pr-review-kit
   ```
3. Push (GitHub marketplace) or copy the folder, then `/plugin marketplace update pr-review-tools` on each device.

## Using it for another team

- Change the reviewer example in the agent's "GitHub review" section.
- Point the webhooks at that team's channel.
- Rename the marketplace (`name` in `.claude-plugin/marketplace.json`) if it should not be "pr-review-tools"; the install command changes to `pr-review-kit@<new name>`.
