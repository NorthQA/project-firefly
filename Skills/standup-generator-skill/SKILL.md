---
name: standup-generator-skill
description: Daily standup built from the issue tracker - yesterday and today, counting tickets you moved (Done, sent back, Blocked) on anyone's board, tickets you filed, and your own open work. Use when preparing a daily standup, status update or end-of-day summary - "write my standup", "what did I do yesterday", "what's on my plate today". Drafts only. Never posts without a yes.
license: Apache-2.0
compatibility: Portable Agent Skills spec. Needs a project tracker connector for automatic mode; works from pasted notes otherwise.
metadata:
  maintainer: northqa
  version: "1.0.0"
  status: active
  updated: "2026-10-15"
  review_after: "2027-01-15"
  portability: portable
  attribution: Adapted from the "standup" skill in Anthropic's knowledge-work-plugins (Apache-2.0).
---

# Standup Generator

Write a standup from the work the user actually did: tickets they moved,
tickets they filed, and their own open tickets. Always draft first. Post
nowhere unless the user says so.

This matters most for people whose work lives on other people's tickets,
such as QA, reviewers and leads. Their day is the statuses they changed, not
the tickets assigned to them. A standup built only from assigned tickets
makes that work invisible.

## Settings

Use a `standup.config.yaml` in the project if one exists. Otherwise use these
defaults. What the user says in the conversation overrides both for that run.

```yaml
timezone: auto                 # or an IANA name, e.g. "Europe/Berlin"
working_days: [Mon, Tue, Wed, Thu, Fri]
window: yesterday_and_today    # or: since_last_standup, since <date>

count_moves_into:              # statuses that count as "your" moves
  done: [Done]
  sent_back: [Changes Requested]  # returned for changes
  blocked: [Blocked]
moves_from: any                # or a list, e.g. [In Testing, In Review]

filed:
  include: true
  types: [bug]                 # match on label or issue type; [] = all filed

own_tickets:
  in_progress: [In Progress]
  waiting: [In Review]         # flagged as a blocker when stale
  next_up: [Todo, unstarted]
  stale_after_days: 1
  today_limit: 4

exclude_statuses: [Canceled, Duplicate]
highlight: [Changes Requested, Blocked, In Review]   # shown in bold
```

## 1. Check the tools

A project tracker connector is required for automatic mode. Source control
is optional, and only used to check review status on linked pull requests.
If no tracker is connected, say which connector would help in one line and
offer manual mode: "Tell me what you did and I'll structure it." If a
connected tool errors, name it in the notes line. Never skip it silently.

## 2. Identify the user

Resolve the current user in each tool ("me"). If you can't, stop and ask.
Never pull someone else's work by mistake.

## 3. Set the window

Default: from the start of the previous working day to now, in the user's
timezone, split into **Yesterday** and **Today**. After a weekend or day off,
"yesterday" is the last working day. Convert the window to UTC before
querying, and keep every timestamp you report in the user's timezone.

Report only changes inside the window. Older history on the same ticket is
context, not a move.

## 4. Find the moves the user made

1. List every issue in the user's teams updated inside the window, not just
   the issues assigned to the user.
2. For each one, read its status history. Keep the changes that landed in a
   `count_moves_into` status inside the window.
3. Decide who made each change:
   - **Best:** the tracker's history gives the actor. Use it.
   - **Fallback:** the user posted a comment on the issue shortly before the
     change. Seconds to a few minutes is the usual pattern when a verdict is
     posted and the status is changed together. Count it as the user's move
     and say in the notes line that you matched it this way.
   - Neither: leave it out. Don't count a move because it happened during
     the user's working hours.
4. A ticket can count more than once. One sent back for changes yesterday and
   moved to Done today appears in both days.

With many issues, split the comment checks across helpers and ask each for a
compact table only (issue, move, comment found, first words). Comment bodies
carry screenshots and long text that would flood the conversation.

## 5. Find what the user filed

If `filed.include` is on, list issues the user created inside the window,
filtered by `filed.types`. Issues created by an integration or automation may
show a different creator. Say in the notes that those aren't counted, rather
than guessing.

## 6. Pull the user's own open work

Issues assigned to the user in `in_progress`, `waiting` or `next_up`, plus
any status changes they had inside the window.

Blockers are:

- the user's tickets in a blocked status;
- tickets waiting on another unfinished ticket owned by someone else;
- tickets in `waiting` longer than `stale_after_days`, and linked pull
  requests with no reviewer or no review in that time.

Say what's stuck, why, and who can unblock it. Never invent a blocker.

## 7. Write it

- Lead each day with counts, e.g. "5 moved to Done, 1 sent back for changes".
- **Leave out any category with nothing in it.** No "Blocked: 0" lines and
  no empty headings. Mention it once in the totals line instead.
- One line per ticket: `ID Title (short reason)`. Shorten titles to about
  60 characters.
- For tickets sent back or Blocked, add the reason and who it went back
  to, taken from the user's own comment.
- Use the tracker's exact status names.

```markdown
## Standup: Thursday, Jan 9

**Yesterday (Wed, Jan 8)**: 3 moved to Done, 1 sent back for changes

Done (In Review → Done):
- PROJ-101 Fix token expiry check
- PROJ-104 Export report to CSV
- PROJ-107 Align table header styles

Sent back (In Review → **Changes Requested**):
- PROJ-110 Rate limit dashboard (two acceptance criteria not met, back to the developer)

**Today (Thu, Jan 9)**: 2 moved to Done

Done (In Review → Done):
- PROJ-110 Rate limit dashboard (retested, passes)
- PROJ-112 Session timeout warning

**Bugs filed**: 1
- PROJ-120 Required field shows no error message on the create form

**Total:** 5 moved to Done, 1 sent back for changes, 1 bug filed. Nothing moved to Blocked.

**Up next**
- PROJ-098 Refactor settings page: **In Review** since Tue, Jan 7
- PROJ-115 Update onboarding copy: Todo

**Blockers**
- PROJ-098: its pull requests have no reviewer assigned.

_Window: Wed, Jan 8 to Thu, Jan 9, local time. Moves matched to the
user's comments posted seconds before each change._
```

End with one short notes line. It should cover the window, any tool that
failed, how moves were attributed, and anything the tracker couldn't show
(for example, tickets reassigned away from the user).

## 8. Confirm

Show the draft and ask if anything should change. Offer a read-aloud
version: full sentences, no ticket IDs, 30 to 60 seconds. If the update
leaves the team, take out customer names and confidential details. Post
only the approved text, and only after the user says to.
