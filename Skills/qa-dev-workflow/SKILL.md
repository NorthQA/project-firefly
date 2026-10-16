---
name: qa-dev-workflow
description: QA-first way to build and fix software - agree what "done" means before coding, write the failing test first, debug from a reproduction instead of guessing, prove the result with evidence, and review against the acceptance criteria. Use for any feature, bug fix or behavior change, especially when the request is vague ("build this", "fix this bug", "it's broken"), when a fix "should work", or before saying something is done. Not for writing manual test cases from a ticket (use qa-flow) or weekly bug reports (use bug-digest).
license: MIT
compatibility: Portable Agent Skills spec. No harness-specific requirements.
metadata:
  maintainer: northqa
  version: "1.0.0"
  status: active
  updated: "2026-10-16"
  review_after: "2027-01-16"
  portability: portable
  attribution: Process inspired by obra/superpowers (MIT), rewritten with a QA focus.
---

# QA Dev Workflow

Build and fix things the way a QA engineer would check them. Every change
starts with what "done" looks like and ends with proof that it is.

Work in this order: **Agree, Plan, Test first, Build, Prove, Review.** Skip
nothing because the change looks small; small changes are where the
untested edge cases hide.

## 1. Agree on "done" before any code

- Restate the request in one or two sentences. If it can be read more than
  one way, ask which is meant.
- Write the **acceptance criteria** as checks a tester could run: "submitting
  an empty email shows *Email is required* and sends nothing".
- Add the cases people forget: empty and invalid input, permissions (who must
  **not** be able to do it), and what happens on error or timeout.
- Show the criteria and wait for a yes. They are the contract for every step
  below.

## 2. Plan in small, checkable steps

Break the work into steps that each end in something you can verify:
`step → how we check it`. If a step can't be checked, split it until it can.
Keep the plan short enough to read in a minute.

## 3. Test first

For each behavior:

1. **Write the test before the code.** One behavior per test, named after
   what the user sees ("shows an error for an empty email"), using the
   project's existing test style.
2. **Run it and watch it fail.** It must fail because the feature is
   missing, with the failure you expected. A test that passes straight away
   is testing the wrong thing. A test that errors (typo, bad import) hasn't
   failed yet: fix it and rerun.
3. **Write the least code that makes it pass.** No extras the criteria
   don't ask for.
4. **Run the whole suite**, not just your file. Everything passes, with no
   new warnings.
5. Clean up names and duplication, then run the suite again.

End-to-end tests follow the same rules as the project's suites: user-facing
locators (role, label), each test creates and cleans up its own data, and
wait for a visible state, never a fixed sleep. Turning a manual case into an
automated one follows **qa-flow**.

## 4. Debug from a reproduction, not a guess

When something breaks:

1. **Reproduce it.** Exact steps, environment and data. If you can't
   reproduce it, say so and collect more evidence (logs, a recording, the
   failing run's trace) before changing anything.
2. **Turn the reproduction into a failing test.** This is the bug's proof,
   and later its regression test.
3. **Find the cause, not the symptom.** Read the full error. Check what
   changed recently. Compare with a version or path that works. Form one
   explanation at a time and test it with the smallest possible change.
4. **Fix the cause**, then watch the failing test pass and the suite stay
   green.
5. If three attempts haven't fixed it, stop and report what you know. More
   guessing makes it worse.

A bug that should be tracked is filed with its reproduction steps, expected
and actual result, and evidence, so it shows up correctly in **bug-digest**.

## 5. Prove it before you say it

"Done", "fixed" and "works" are claims. Each needs fresh evidence from this
change:

| Claim | Evidence |
| --- | --- |
| Tests pass | The full command you ran and its result (counts, exit code) |
| Bug is fixed | The reproduction test failed before and passes now |
| UI works | A screenshot or recording of the acceptance criteria |
| Build is fine | The build command's output, not a guess |

If you couldn't run something, say exactly what wasn't verified. Never
report success from a partial run, an old run, or a helper's summary you
didn't check.

## 6. Review against the criteria

Before asking for review, check your own diff:

- Every acceptance criterion from step 1 has a test.
- Negative cases and permissions are covered.
- No unrelated changes, debugging leftovers or secrets in the diff.
- The summary lists what changed, file by file, and anything risky.

When feedback comes back, check each point against the code before acting
on it. Fix what's right, explain with evidence what isn't, and rerun the
tests after the changes.

## Never

- Write the code first and the test after, "to save time".
- Change a failing test to make it pass instead of fixing the code.
- Claim something passes, works or is fixed without running it.
- Stack fixes on top of a cause you haven't found.
- Commit, push or post anything without being asked.
