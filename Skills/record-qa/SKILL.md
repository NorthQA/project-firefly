---
name: record-qa
description: Record a browser QA check with agent-browser, collect page errors, console errors, failed requests and a video, and report what broke. Use when the user asks to record, film, or capture errors ("record the signup flow on staging and tell me what broke", "film the checkout and capture console errors"), to re-run a saved flow file, or to record a test dashboard while an automated run happens. The user describes it in plain words; you run every command. Not for writing automated tests.
license: MIT
compatibility: Portable Agent Skills spec. Requires the agent-browser CLI and ffmpeg.
metadata:
  maintainer: northqa
  version: "1.0.0"
  status: active
  updated: "2026-10-12"
  review_after: "2027-01-12"
  portability: portable
---

# Record QA

The user says what to check in plain words. You turn that into a recorded,
headless browser run and hand back the captured errors and the video. The
user should never have to type an agent-browser command.

Run `agent-browser skills get core` once if you need the command reference.

## Prerequisites

- [agent-browser](https://github.com/vercel-labs/agent-browser) (`npm install -g agent-browser`, then `agent-browser install` for the browser)
- [ffmpeg](https://ffmpeg.org/) for shrinking the video

See [`references/example-login.flow`](references/example-login.flow) for a complete flow file.

## Project settings

| Setting | What it is |
| --- | --- |
| Test environments | Hosts you may record against. |
| Production hosts | Hosts you must never record against. |
| Access gate | Header names and variables if test hosts sit behind SSO or an access proxy. |
| Test accounts | Which seeded accounts recordings may log in as. |
| Share target | Where recordings go: a chat channel, a hosted page, or a folder. |

## 1. Pin the target

URL, environment, and what "working" looks like. Ask only if the
environment is unclear. Refuse production hosts.

## 2. Explore in your own session

Learn the real steps before recording:

```bash
export AGENT_BROWSER_SESSION=record-qa-explore
agent-browser open <url>
agent-browser snapshot -i
```

Click through the flow the user described, snapshotting after each change.
Close it when done: `agent-browser close`.

## 3. Write a flow

One agent-browser command per line, `#` for comments, saved as
`flows/<short-name>.flow` so it can be re-run.

- Never use `@eN` refs from your exploration session; they don't exist in
  a fresh browser. Use stable locators: `find text "..." click`,
  `find role button click --name "Save"`, `find label "Email" fill "..."`.
- Add `wait 1500` (or `wait --text "..."`) after navigation and loading so
  the video shows the result.
- Secrets come from the environment as `${NAME}`. Never write a password or
  token into the file.

## 4. Record it

Use a fresh session per recording:

```bash
S=record-qa-$$
agent-browser --session $S open about:blank
# Only if the host sits behind an access gate; values from the environment:
agent-browser --session $S set headers "{\"<Header-Name>\": \"$GATE_VALUE\"}"
agent-browser --session $S record start recording.mp4
# ...run each line of the flow with: agent-browser --session $S <line>
# stop at the first step that exits non-zero
agent-browser --session $S --json errors      > page-errors.json
agent-browser --session $S --json console     > console.json
agent-browser --session $S --json network requests > requests.json
agent-browser --session $S screenshot final.png
agent-browser --session $S record stop
agent-browser --session $S close
```

Wrap this in a small script for the team if they record often: it should
expand `${NAME}` from the environment, stop at the first failed step,
collect the evidence even when a step fails, and write a short `report.md`.

Make the video small before sharing:

```bash
ffmpeg -y -loglevel error -i recording.mp4 -an -vf "scale=min(1280\,iw):-2" \
  -r 5 -c:v libx264 -preset slow -tune stillimage -crf 36 -pix_fmt yuv420p \
  -movflags +faststart recording-small.mp4
```

Keep the original if the re-encode isn't smaller.

## 5. Read the evidence and report

- Failed requests: responses with status 0 or 400 and up. Requests with no
  response at all were usually cut off by the next navigation (fonts,
  analytics, captcha); list them separately, they're not failures.
- Reply with: a one-line verdict (clean run, or found an issue), the failed
  step and what the screen showed (`final.png`), and the page errors,
  console errors and failed requests sorted into app bug / environment /
  noise. Then the video path.

## Recording a test dashboard during an automated run

To film a dashboard while its runner works: open the dashboard in its own
session, wait until it has loaded (`agent-browser wait --text "<a heading
it shows>"`) before clicking anything, select the run's area and results
view, then `record start`. Stop when the run's process exits. Collect the
runner's own failure screenshots and videos from its report folder
afterwards; they show the app, while your recording shows the dashboard.

Save recordings outside any folder the dashboard watches or serves.

## Sharing

- Chat: post the verdict and failures as the message and put the video,
  screenshots and report in the thread. A post is an external write: confirm
  the channel with the user first; a direct message to the user is the safe
  test.
- Hosted page: publish an `index.html` with the evidence next to it. If the
  team keeps one shared report page, add the run to it instead of making a
  new link.

## Reading the report honestly

- A failed step can be a wrong locator in your flow. If `final.png` shows
  the element under another name, fix the flow and re-run before calling it
  an app bug.
- Known noise: `404 /favicon.ico`.
- Check that any visible cursor overlay doesn't interfere with pages that
  render on load before turning it on; overlays can cause false page errors.

## Safety

- Never record against production hosts.
- Never print access-gate credentials; strip token parameters from any URL
  you quote.
- Use seeded test accounts only. No real third-party accounts (calendars,
  email, payments); use each provider's test mode, such as the payment
  provider's test card numbers.
- Recordings can show customer data. Check the video before sharing it
  outside the team.
