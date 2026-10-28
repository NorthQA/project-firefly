# project-firefly

NorthQA Standard AI Skills, Plugins, Connectors/Integrations

## Contents

| Path | Description |
| --- | --- |
| [Skills](Skills/README.md) | Standard AI skills, with installation and contribution notes. |
| [Plugins](Plugins/README.md) | Claude Code plugins (skills, commands, agents, hooks, MCP), with layout and install notes. |

## Skills

- **ai-coding-discipline**: rules for careful, reviewable code changes.
- **qa-dev-workflow**: QA-first way to build and fix software: agreed "done", tests first, debugging from a reproduction, proof before claims.
- **ui-design-guidelines**: produces a canonical design system file before frontend work.
- **web-security**: OWASP and WSTG based security guidance for web apps and APIs.
- **qa-flow**: manual QA from a ticket: test cases, review, case files, test runs, optional automation.
- **bug-digest**: weekly QA bug report built straight from the issue tracker, posted after approval.
- **standup-generator-skill**: daily standup built from the issue tracker, counting the tickets you moved, filed and own.
- **security-audit-skill**: source-first security audit with adversarial validation and verified reports, by Cloudflare (MIT).

See the [Skills README](Skills/README.md) for details.

## Plugins

- **pr-review-kit**: PR review agent that posts a short GitHub review and the full report to Discord, plus multi-PR batch summaries.

See the [Plugins README](Plugins/README.md).

## Connectors and Integrations

None yet.

## License

[MIT](LICENSE), except where a skill folder has its own `LICENSE` (standup-generator-skill is Apache-2.0; security-audit-skill is MIT, Copyright (c) 2025-2026 Cloudflare, Inc.).
