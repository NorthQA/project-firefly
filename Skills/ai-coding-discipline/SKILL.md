---
name: ai-coding-discipline
description: Working rules for writing and changing code carefully - think before modifying, keep it simple, make surgical changes, define success and verify it, keep diffs reviewable. Use for any coding task, bug fix, refactor, or feature, especially when the request is short or vague ("add validation", "fix this", "code this").
---

# AI Coding Discipline

Rules for changing code without wrong guesses, bloated solutions, or messy diffs. Adapted from the principles in [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills).

Work in this order: **Understand, Plan, Implement, Verify.** Don't jump straight to code.

## 1. Think before modifying

- State your assumptions before acting on them.
- If a request can be read more than one way, list the readings and ask which is meant. Don't pick one silently.
- If something is unclear or a file you expected doesn't exist, stop and say so. Don't guess to keep moving.
- If there's a simpler approach than the one requested, say so and let the user decide.

## 2. Keep it simple

- Write the least code that fully meets the requirement.
- No features, options, configuration, or "future-proofing" nobody asked for.
- No abstractions (helpers, base classes, generic utilities) for code used once.
- Handle errors that can happen; don't add handling for ones that can't.
- If the solution looks large for the problem, shrink it before presenting it.

## 3. Make surgical changes

- Touch only the lines the task needs. Every changed line traces back to the request.
- Match the existing style of the file, even if you'd write it differently.
- Don't refactor, reformat, or rename unrelated code.
- Notice an unrelated problem? Mention it in your summary; don't fix it in this change.
- Remove imports or variables your change made unused. Leave pre-existing dead code alone.

## 4. Define success, then verify it

- Before implementing, turn the request into checkable success criteria, for example: "submitting an empty email shows the error and sends nothing."
- For bugs: reproduce first (ideally a failing test), then fix, then show the reproduction passes.
- For multi-step work, write a short plan where each step has its check: `step -> how we verify it`.
- Nothing is done until the checks have actually run. If something couldn't be run, say exactly what wasn't verified.

## 5. Keep diffs reviewable

- Prefer several small, focused changes over one large one.
- After implementing, summarize the diff file by file in plain language.
- Point out anything risky, surprising, or worth a second look.

## Never

- Claim a test passed without running it.
- Commit, push, or install anything without being asked.
- Read, print, or commit secrets (`.env` files, keys, tokens).
