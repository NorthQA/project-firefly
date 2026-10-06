---
name: web-security
description: Web application and API security for designing, writing, auditing and testing code against the OWASP Top 10:2025, the OWASP API Security Top 10, the OWASP Web Security Testing Guide (WSTG) checklist, the core API security controls (OAuth2/OIDC, HTTPS/TLS, WebAuthn/passkeys, API gateway, firewall/WAF, API versioning, rate limiting, authorization, input validation), secure coding practices, secure design and least privilege (PoLP). Use this whenever the user writes or reviews auth, login, sessions, permissions, API endpoints, input handling, file uploads, database queries, secrets, CORS, CSP or headers, or asks for a security review, security test plan, threat model, hardening, "is this secure?", WSTG, or OWASP/pentest-style checks, even when security is only implied (e.g. "add a password reset", "expose this as an API").
---

# Web & API Security

Goal: find and prevent real vulnerabilities in the team's own web apps and APIs, and design features so the secure path is the default one.

Scope and ethics: work only on code and systems the user owns or is authorized to test. Explain vulnerabilities and show **fixes and defensive tests**. Don't produce weaponized exploits or attack tooling aimed at third-party systems.

Follow the repo's `CLAUDE.md` rules. Never read `.env`, keys or credentials to "check" them. If a secret shows up, flag it without repeating it and recommend rotation.

## Pick the mode

| User wants | Do |
|---|---|
| Design a feature ("add password reset", "new public API") | **Secure design** (section 1) before any code |
| Write code | Apply the **secure coding rules** (section 2) as you write, then self-check |
| Review or audit code, a diff or a PR | Run the **audit** (section 3) against `references/owasp-checklist.md` |
| Security test plan / test the running app / "WSTG" / pentest-style check | Run the **WSTG test pass** (section 4) with `references/wstg-checklist.md` |
| Design, build or harden an **API** | Apply the nine controls in `references/api-security-controls.md` and copy its new-endpoint checklist into the plan |

The three references work together:

- `owasp-checklist.md` covers **what** the risks are (Top 10:2025 plus the API Top 10).
- `wstg-checklist.md` covers **how to test** for them, test by test (WSTG IDs, with code-review and safe runtime checks, mapped back to the Top 10).
- `api-security-controls.md` covers **which defenses an API needs**, layer by layer: OAuth2/OIDC, HTTPS, WebAuthn/passkeys, API gateway, firewall/WAF, versioning, rate limiting, authorization and input validation, each mapped to WSTG and OWASP IDs.

## 1. Secure design (lightweight threat model)

Answer these briefly before implementing:

1. **Assets:** what data or actions are valuable? (PII, money, admin actions, tokens)
2. **Actors and trust boundaries:** anonymous user, logged-in user, other tenant, admin, internal service, third-party webhook. Where does untrusted data enter?
3. **Threats (STRIDE-lite):** spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege. List the ones that apply, with one line each.
4. **Controls:** for each threat, the specific control (authz check, rate limit, signature, audit log…).
5. **Least privilege:** the minimum role, scope, DB permission and data each part needs.
6. **Abuse cases:** how would someone misuse the *business flow*? (enumeration, brute force, coupon replay, mass sign-up, scraping)
7. **Failure behavior:** what happens on errors, timeouts or partial failure? It must **fail closed** (A10:2025).

Flag anything touching auth, payments, personal data or permissions as **needs tech lead review**.

## 2. Secure coding rules (apply while writing)

- **Access control (A01, API1/3/5):** deny by default. Check authorization on the server for every request **and every object** (ownership or tenant scoped in the query). Don't rely on hidden fields, client-side checks or unguessable IDs. Server Actions and route handlers are public endpoints.
- **Input:** validate with a schema at the boundary (type, length, format, allowlist). Reject unknown fields to prevent mass assignment (API3).
- **Injection (A05):** parameterized queries or ORM bindings only. No string-built SQL, shell, LDAP or NoSQL queries. Never `eval` or `new Function` on input. Avoid shell calls. If unavoidable, pass an argument array, never a string.
- **Output / XSS:** rely on framework auto-escaping. Treat `dangerouslySetInnerHTML`, `v-html` and `innerHTML` as red flags; sanitize with a vetted library (DOMPurify) if truly needed. Set a CSP.
- **Authentication (A07, API2):** use a proven library or provider. Hash passwords with Argon2id (or bcrypt/scrypt). Add rate limiting and lockout/backoff on login, reset and OTP. Use generic error messages. Support MFA. Rotate the session ID on login.
- **Sessions and cookies:** `HttpOnly; Secure; SameSite=Lax` (or `Strict`), short expiry, server-side invalidation on logout. Use CSRF protection for cookie-authenticated state changes.
- **Crypto (A04):** TLS everywhere with HSTS. Use platform crypto libraries only, and never roll your own. Use a CSPRNG for tokens. Encrypt sensitive data at rest. Keys go in a secret manager, never in code.
- **Configuration (A02):** secure headers (CSP, HSTS, `X-Content-Type-Options`, `Referrer-Policy`, `frame-ancestors`). CORS uses an explicit origin allowlist, never `*` with credentials. No debug mode or stack traces in production. Default credentials removed.
- **Supply chain (A03):** pin versions and commit lockfiles. Add no new dependency without review. Run `npm audit` or the equivalent. Prefer maintained packages. Verify integrity (SRI for CDN scripts). Treat third-party skills, plugins and MCP servers the same way.
- **Integrity (A08):** verify webhook signatures and timestamps. Don't deserialize untrusted data into objects. Sign and verify anything the client round-trips. Protect the CI/CD pipeline.
- **Logging (A09):** log auth events, access denials and admin actions with a request ID. Never log secrets, tokens, passwords or full PII. Alert on anomalies.
- **Exceptional conditions (A10):** catch errors at boundaries, return generic messages, and log details server-side. On an error in an auth or authz path, **deny**. Put timeouts on everything. Handle partial failures with transactions or rollback.
- **SSRF (API7):** allowlist outbound hosts, block internal/metadata IP ranges after DNS resolution, and disable redirects or re-check them.
- **Resource consumption (API4):** rate limits, max body size, max page size, upload limits, query timeouts.
- **Business flows (API6):** protect sensitive flows (sign-up, checkout, voting) from automation with rate limits, captcha or device checks as appropriate.
- **Inventory and third-party APIs (API9/10):** document every endpoint and version, retire old ones, and validate data from third-party APIs as untrusted.
- **File uploads:** allowlist type by content (magic bytes), size limit, random stored names, store outside the web root or in object storage, and serve with `Content-Disposition` and the correct content type.
- **API controls:** every API gets the layered controls in `references/api-security-controls.md`: OAuth2/OIDC done right (Auth Code + PKCE), HTTPS only, passkeys where login matters, gateway plus firewall/WAF in front, versioned routes (`/api/v1/...`), rate limits by IP, user and action, central authorization (read ≠ write), and schema validation at both the gateway and the service.
- **Least privilege everywhere:** minimal DB grants, scoped tokens, non-root containers, narrow IAM, and DTOs that expose only needed fields.

## 3. Audit procedure

1. Get the scope: the diff (`git diff main...HEAD`, `gh pr diff <n>`) or the listed files. Read the related requirement.
2. Map the entry points (routes, actions, handlers, webhooks, jobs) and trust boundaries.
3. Walk `references/owasp-checklist.md` category by category. Mark only categories that apply, and skip the rest explicitly.
4. Where tooling exists in the project, run it (dependency audit, SAST, linters with security rules). Never guess commands. Ask.
5. For any API in scope, walk the nine controls in `references/api-security-controls.md` and mark each Pass / Fail / N/A / Not checked.
6. For the areas the change touches, also run the matching WSTG sections from `references/wstg-checklist.md` (for example, login code → ATHN + SESS, file upload → BUSL-08/09, new endpoint → ATHZ + APIT).
7. Suggest a **defensive test** for each confirmed finding (e.g. "user B requesting user A's order returns 403").

## 4. WSTG test pass

Use this for a full security test plan, or before a release.

1. **Confirm authorization and target:** only the team's own app, in a local, dev or staging environment. Never production or third-party systems without written permission. No destructive or denial-of-service tests, and no real user data.
2. **Scope the sections:** start with INFO-06 (entry points) and INFO-10 (architecture), then pick the WSTG sections that apply. Mark the rest N/A with a one-line reason, for example "INPV-06 LDAP: N/A, no LDAP in stack".
3. **For each in-scope test ID:** do the *code review* check first, then the *runtime check* if a running environment is available. Record Pass / Fail / N/A / Not tested with evidence. Never mark a test Pass unless it was actually checked.
4. **Automate the important ones:** turn Fail and high-risk checks (IDOR, authz bypass, CSRF, mass assignment, SSRF, rate limits) into automated regression tests in the project's existing test framework. Follow the `qa-testing` skill if the repo has it.
5. **Report:** use the WSTG row format in the checklist. Group findings by Top 10:2025 category using its mapping table, and summarize coverage (tested / N/A / not tested counts).

## Report format

```
Scope: <files / PR / feature>
Summary: <1–2 sentences, overall risk>

Findings (most severe first):
[Critical|High|Medium|Low] <OWASP id, e.g. A01:2025 / API1:2023 / WSTG-ATHZ-04> - <file:line>
  Issue: <what is wrong>
  Impact: <what an attacker could do>
  Fix: <specific change, with a snippet if short>
  Test: <how to prove it's fixed>

API controls (if API in scope): <OAuth2 · HTTPS · WebAuthn · Gateway · Firewall/WAF · Versioning · Rate limit · AuthZ · Validation - Pass/Fail/N/A each>
WSTG coverage (if run): <n tested / n N/A / n not tested>
Good practices observed: <brief>
Not checked / out of scope: <honest list>
Needs tech lead review: yes/no - <why>
```

Severity guide: **Critical** means remote unauthenticated compromise or mass data exposure. **High** means authz bypass, injection or account takeover. **Medium** means it needs specific conditions or has limited impact. **Low** means hardening or defense in depth. Don't inflate severity, and don't pad the report with generic advice that doesn't apply to this code.

Don't modify files during an audit unless the user asks you to apply fixes. Then fix one finding at a time, most severe first.

## No attribution

No "generated by Claude/AI" comments, credits or `Co-Authored-By` trailers in code, commits, reports or PRs.
