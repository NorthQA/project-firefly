# Installation

## 1. Prerequisites

Check each on the device:

```bash
claude --version      # Claude Code with /plugin support
gh auth status        # signed in to GitHub
python --version      # Python 3 (python3 on macOS/Linux)
git --version
```

The `gh` account needs read access to the repos you review and permission to post reviews.

## 2. Get the marketplace onto the device

Pick one:

- **Private GitHub repo (best for several devices).** Push this `pr-review-plugin/` folder as the root of a private repo, for example `<your-github-user>/claude-pr-tools`. Every device then adds it by name and can pull updates.
- **Folder copy.** Copy `pr-review-plugin/` anywhere on the device (or unzip the backup zip).

## 3. Add the marketplace and install

In Claude Code:

```text
/plugin marketplace add <your-github-user>/claude-pr-tools        # GitHub repo
/plugin marketplace add C:\path\to\pr-review-plugin        # or a local folder
/plugin install pr-review-kit@pr-review-tools
```

You can also run `/plugin` and pick it from the menu.

## 4. Set the Discord webhooks

Create two webhooks in Discord (Channel settings, Integrations, Webhooks): one for single PR reviews, one for batch summaries. They can point at the same channel.

Add them to `~/.claude/settings.json` on the device (Windows: `C:\Users\<you>\.claude\settings.json`), merging into any existing `env` block:

```json
{
  "env": {
    "DISCORD_PR_REVIEW_WEBHOOK": "https://discord.com/api/webhooks/<id>/<token>",
    "DISCORD_PR_SUMMARY_WEBHOOK": "https://discord.com/api/webhooks/<id>/<token>"
  }
}
```

Keep these out of git and out of the plugin: anyone with a webhook URL can post to the channel.

## 5. Restart and check

Restart Claude Code, then:

- `/agents` should list `pr-review-kit:pr-review`.
- The skills list should include `pr-review-kit:pr-reviewer`, `pr-review-kit:pr-reviewer-spillwave` and `pr-review-kit:pr-batch-summary`.

Optional dry run of the Discord script (no post is sent):

```bash
python <plugin>/skills/pr-reviewer/scripts/discord_post.py pr-review-1.md summary.txt --dry-run
```

## Try without installing

```bash
claude --plugin-dir <path>/project-firefly/Plugins/pr-review-kit
```

Loads the plugin for that session only.

## Update

- **GitHub marketplace:** push the change (bump `version` in `Plugins/pr-review-kit/.claude-plugin/plugin.json` and in `.claude-plugin/marketplace.json`), then on each device run `/plugin marketplace update pr-review-tools` and update the plugin from `/plugin`.
- **Local folder:** replace the folder, then run the same update commands.

## Uninstall

```text
/plugin uninstall pr-review-kit@pr-review-tools
/plugin marketplace remove pr-review-tools
```

The webhook entries in `settings.json` stay until you delete them.

## Personal copies on the same device

If the original personal files are also in `~/.claude` (`agents/pr-review.md`, `skills/pr-reviewer*`), both versions load. The plugin ones are prefixed `pr-review-kit:`. Delete the personal copies if you only want the plugin.
