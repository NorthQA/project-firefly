# Skills

NorthQA standard AI skills for Claude Code and compatible agents.

## What is a skill?

A skill is a folder containing a `SKILL.md` file. The file starts with frontmatter (`name` and `description`) followed by instructions the agent loads when the task matches the description. A skill can also ship a `references/` folder with deeper material that is read only when needed.

```
Skills/
  <skill-name>/
    SKILL.md          required: frontmatter + instructions
    references/       optional: supporting checklists and docs
```

## Available skills

| Skill | Purpose |
| --- | --- |
| [ai-coding-discipline](ai-coding-discipline/SKILL.md) | Working rules for careful code changes: think before modifying, keep it simple, make surgical changes, verify, keep diffs reviewable. |
| [ui-design-guidelines](ui-design-guidelines/SKILL.md) | Generates a single canonical `design_guidelines.json` (palette, typography, layout, motion) before any frontend code is written. |
| [web-security](web-security/SKILL.md) | Web and API security against the OWASP Top 10:2025, OWASP API Security Top 10 and WSTG, plus secure design and least privilege. |

### web-security references

- [owasp-checklist.md](web-security/references/owasp-checklist.md)
- [api-security-controls.md](web-security/references/api-security-controls.md)
- [wstg-checklist.md](web-security/references/wstg-checklist.md)

## Plugins

Plugins live in the separate [Plugins](../Plugins/README.md) folder. A plugin can bundle several skills together with commands, agents, hooks and MCP servers.

## Installing a skill

Copy the skill folder into one of these locations:

- Personal (all projects): `~/.claude/skills/<skill-name>/`
- Project (shared with the team): `.claude/skills/<skill-name>/`

The agent picks a skill up automatically when a request matches its `description`. You can also invoke one by name, for example `/web-security`.

## Adding a new skill

1. Create `Skills/<skill-name>/SKILL.md` using a lowercase, hyphenated name.
2. Write a `description` that says what the skill does and when to use it. This is what triggers it.
3. Keep `SKILL.md` focused. Move long checklists into `references/`.
4. Add the skill to the table above and to the root [README](../README.md).
