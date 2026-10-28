---
name: pr-batch-summary
description: After reviewing more than one PR in a session (with the pr-review agent or otherwise), group them by merge readiness and post one batch summary with box tables to Discord. Use when several PRs were reviewed, or the user asks for a PR batch summary, merge order across PRs, or a Discord roundup of reviews.
---

# PR review batches

After reviewing more than one PR in a session (with the `pr-review` agent or otherwise), send one batch summary to Discord:

1. Group the PRs by merge readiness: Ready to merge, Merge after nits are fixed, Merge after requested changes are fixed, Not ready to merge. A PR with any important finding is never "Ready to merge", even with an Approve verdict.
2. Write the Discord message as plain markdown, never tables (Discord doesn't render them): a `##` title, one line saying how many PRs were reviewed and whether anything is ready, then each non-empty group as a `###` heading (⛔ Not ready, 🔧 after requested changes, 🧹 after nits, ✅ ready) with one bullet per PR: `- **#<number> <short name>** · <verdict> · <b>/<i>/<n>: <main issue in one or two sentences>`. End with short **Merge order**, **Watch out for** and **Not reviewed yet** sections.
3. Write `pr-review-summary-<YYYY-MM-DD>.md` (add `-2`, `-3` for later batches that day). It holds one box-drawing table per group in ```text blocks, rendered with `python <this skill's base directory>/scripts/box_table.py <table.json>` (columns `PR | Verdict | Blocker / Important / Nit | Main issue`, widths `[22, 10, 9, 42]`), plus merge order, clashes between PRs, attribution or tech-lead-review notes, and PRs not reviewed.
4. Post both once: `python <this skill's base directory>/scripts/discord_post.py --batch <summary.md> <message.txt>`. It sends to `$DISCORD_PR_SUMMARY_WEBHOOK`, splits long messages between table rows, and attaches the .md to the last message.
