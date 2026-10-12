---
name: bug-digest
description: Use when asked for the weekly QA bug report or bug digest - "do the bug digest", "weekly bug report", "routine bug feedback for the channel", "what bugs did I file this week". Builds the report by querying the issue tracker directly, drafts it, and posts to the team channel only after a yes. Not for release triage of a single build and not for writing test cases (use qa-flow).
license: MIT
compatibility: Portable Agent Skills spec. No harness-specific requirements.
metadata:
  maintainer: northqa
  version: "1.0.0"
  status: active
  updated: "2026-10-12"
  review_after: "2027-01-12"
  portability: portable
---

# Bug digest

A weekly report of the QA owner's bugs, the QA verification queue, bugs that
came from product feedback, and fixed bugs that still need automated tests.
Built by querying the issue tracker directly; there is no bot or script to
run.

## Project settings

| Setting | Example |
| --- | --- |
| QA owner | Name and tracker user ID of the person the report is for. |
| Team | Tracker team to search. |
| Bug label | The label that marks a bug. Confirm the name in the tracker before querying. |
| QA queue state | The status that means "waiting for QA" (for example "In QA"). |
| Feedback channel | Chat channel ID where product feedback is reported. |
| Report channel | Where the digest is posted, and how (bot or webhook variable). |
| Automated test folder | Where to look for existing automated tests by ticket ID. |
| Week | Default: Monday to Friday of the current week. |

## Build it

Fetch, then filter in code. Tracker searches often can't filter by creator,
and one big page ordered by "updated" misses old open bugs, so query open
states directly.

1. **The owner's bugs**: bug label × each open state type (triage,
   unstarted, started), filtered to the owner as creator. Plus bugs whose
   state is Done with a completed date inside the week. Skip ones already
   reported Done last week.
2. **QA queue**: every bug currently in the QA queue state, whoever filed
   it. These are the owner's to verify. Drop archived ones. Flag items that
   look like features rather than bugs (large scope, part of a bigger piece of planned work).
3. **From product feedback**: bugs linked to a message in the feedback
   channel (a chat-message attachment on the ticket; links to pull requests
   don't count). Bugs only, no features.
4. **Needs automated tests**: this week's Done bugs from the owner or from
   product feedback with no automated test mentioning the ticket ID:
   `grep -rli <TICKET> <automated test folder>`.

Large result sets: save to a file and parse rather than reading them inline.

## Report shape

```
Weekly Bug Report · <date range>
Filed by <owner> · <N> bugs

<Status> (<n>)
• <TICKET> <title>

In QA (<n>)
• <TICKET> <title>

From Product Feedback (<n>) · bugs only
• <TICKET> <title> (<reporter>)

For Automation & Test Cases (<n>) · Done bugs with no automated test
• <TICKET> <title> (<owner> or product feedback) → /qa-flow <TICKET>
```

- Group the owner's bugs by current status with a count per group. It's a
  snapshot of where things stand, not "filed this week". Missing open bugs
  filed in earlier weeks is the usual mistake.
- Leave out the backlog section unless the owner asks for it; the header
  count is Done this week plus non-backlog open bugs.
- Link each ticket. Name people by name (the channel is the whole team),
  never "you".

## Post it

Show the full draft first. Post only after an explicit "post it". Then send
it to the report channel the way the project settings say. Record the week
and the Done tickets reported, so next week skips them.
