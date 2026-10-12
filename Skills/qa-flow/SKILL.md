---
name: qa-flow
description: Use for the manual QA workflow from a ticket - generate test cases from the ticket, get them reviewed, keep them as case files in the repo, load them into the team's test management tool, run them there, report the result on the ticket, and optionally turn cases into automated end-to-end tests. Triggers - "qa this ticket", "write test cases for <ticket>", "/qa-flow <ticket>". Not for running a regression of existing automated tests and not for weekly bug reporting (use bug-digest).
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

# QA flow

Ticket → test cases → case file in the repo → test management tool →
manual run → (optional) automated tests → run and report.

Manual cases live as plain text files in the project repo. The repo is the
record; the test management tool is where people run them.

## Project settings

Fill these in per project (project notes or `qa-flow-settings.md` next to
this skill). Ask once if one is missing.

| Setting | Example |
| --- | --- |
| Issue tracker and ticket key | `ABC-1234` |
| How to read a ticket | Tracker API or CLI, and the key's variable name and env file |
| Manual case folder | `<test package>/manual/` |
| Area folders | one folder per product area (`admin/`, `customer/`, ...) |
| Test management tool | Where manual runs happen, and how cases get in (import, API, sync command) |
| Automated test folder and runner projects | folder per area and its project name |
| Test helpers | the project's login, data-seeding and cleanup helpers |
| Report wording | the verdict words the team uses on tickets |

## Step 1: Fetch the ticket

Ask for the ticket ID if it wasn't given. Read the title, description,
acceptance criteria or QA steps, sub-tickets, and comments through the
tracker's API or CLI. Keep the API key in an ignored env file and never
print it. Show a short summary before going on.

## Step 2: Generate test cases

Write cases from the acceptance criteria and QA steps. This is also the file
format:

- indent 0: ticket header, `<TICKET>: <title>` (exactly one line, first)
- indent 1: pre-requisites and case titles, `TC-<ticket number>-01: <name>`
- indent 2: steps and expected results

Two spaces per indent level. Blank lines and lines starting with `#` are
ignored.

```
ABC-1234: Customer can view order details
  Pre-requisites: Customer account exists with one placed order
  TC-1234-01: Customer sees order summary
    Open the orders page
    Click the order row
    Verify item name, total and status are shown
  TC-1234-02: Customer can download the invoice
    Open the order detail page
    Click Download invoice
    Verify a PDF downloads
```

Cover the happy path, each acceptance criterion, the obvious negative
cases, and permissions (who must not see or do it). **Show the cases for
review and wait for approval before writing anything.**

## Step 3: Write the case file and load it

1. Pick the area folder; ask if the ticket doesn't make it obvious.
   Environments are not folders; a run records its environment.
2. Check for an existing file for the ticket:
   `grep -rl "^<TICKET>:" <manual case folder>`. If one exists, add the new
   cases under its header instead of making a second file; keep TC numbers
   unique.
3. Write the reviewed cases verbatim to `<manual case folder>/<area>/<TICKET>.md`.
4. Load them into the test management tool the way the project settings
   say. If the tool supports a dry run or preview, run it first and check
   what will change. Loading the same content twice should change nothing.
5. Commit the case file with the ticket's branch or on its own.

## Step 4: Run the cases

Start a manual run in the test management tool, recording tester,
environment and build. Mark each step pass / fail / blocked, attach evidence
where useful, and complete the run.

Draft the result for the ticket (team's verdict wording, link to the run)
and post it only after the person says yes.

## Step 5: Automate (optional)

Decide per case: worth automating as a pull-request check, as a scheduled
check against a hosted environment, kept manual, or not worth automating.
Don't automate everything by default.

For an automated case, write `<automated test folder>/<area>/<name>.test.ts`
(or the project's equivalent) following its existing tests:

- one group per ticket, one test per case, titles carrying the TC ID
- each test creates its own data with unique IDs and cleans it up through
  the project's fixtures; no shared accounts or rows between tests
- user-facing locators (by role, by label), scoped to the form or dialog;
  exact matching when text repeats
- wait for an observable state, never fixed sleeps or "network idle"
- use the project's own login and seeding helpers rather than inventing new
  ones

## Step 6: Run and report

Run the new test file alone through the project's runner (for Playwright:
`npx playwright test <file> --project=<project>`). Report pass / fail. On a
failure, check the screenshot, video and trace and the locator before
calling it an app bug.

## Summary

1. Fetch ticket → summary
2. Generate cases → review, approval
3. Write the case file → load it into the test tool
4. Run it → draft the ticket comment, post on a yes
5. Automate the cases worth it
6. Run and report
