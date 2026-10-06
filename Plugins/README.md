# Plugins

NorthQA Claude Code plugins. A plugin bundles skills, commands, agents, hooks and MCP servers into one installable package that can be shared across the team.

## Available plugins

None yet.

| Plugin | Purpose |
| --- | --- |
| | |

## Plugin layout

Each plugin lives in its own folder:

```
Plugins/
  <plugin-name>/
    .claude-plugin/
      plugin.json     required: name, description, version, author
    skills/           optional: <skill-name>/SKILL.md
    commands/         optional: slash commands as markdown files
    agents/           optional: subagent definitions
    hooks/            optional: hooks.json
    .mcp.json         optional: MCP server config
    README.md         what it does, how to use it
```

Only `.claude-plugin/plugin.json` sits inside `.claude-plugin/`. All other folders go at the plugin root.

Example `plugin.json`:

```json
{
  "name": "example-plugin",
  "description": "What the plugin does",
  "version": "0.1.0",
  "author": { "name": "NorthQA" }
}
```

## Skills vs plugins

- A **skill** is a single `SKILL.md` instruction set. See [Skills](../Skills/README.md).
- A **plugin** is a package that can contain several skills plus commands, agents, hooks and MCP servers, with a version and a manifest.

Standalone skills that are mature and reused together can be promoted into a plugin by moving them into the plugin's `skills/` folder.

## Installing a plugin

Test locally:

```
claude --plugin-dir ./Plugins/<plugin-name>
```

To distribute to the team, publish the plugins through a marketplace (a repository with `.claude-plugin/marketplace.json`), then:

```
/plugin marketplace add <repo>
/plugin install <plugin-name>@<marketplace-name>
```

## Adding a new plugin

1. Create `Plugins/<plugin-name>/` with a lowercase, hyphenated name.
2. Add `.claude-plugin/plugin.json`.
3. Add the components it needs (skills, commands, agents, hooks, MCP).
4. Write a `README.md` inside the plugin folder.
5. Add the plugin to the table above and to the root [README](../README.md).
