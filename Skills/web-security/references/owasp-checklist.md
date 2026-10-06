# OWASP audit checklist

Sources: OWASP Top 10:2025 (https://owasp.org/Top10/2025/) and OWASP API Security Top 10:2023 (https://owasp.org/API-Security/). If OWASP has published a newer edition, use its category names.

For each category, ask the questions that apply to the code in scope. The "look for" hints are grep-able starting points, not proof.

For step-by-step **test cases** (WSTG IDs, with code-review and runtime checks), see `wstg-checklist.md`. It includes a mapping from each Top 10:2025 category to its WSTG sections.

## Contents
- Web: A01–A10 (2025)
- API: API1–API10 (2023)
- Quick grep list

---

## OWASP Top 10:2025

### A01 Broken Access Control
- Is every route, action and handler behind an authn check? Is authz checked on the **server**?
- Object-level: is the query scoped by owner or tenant? Can user B read or change user A's record by changing an ID?
- Function-level: are admin-only operations checked by role or permission on the server?
- CORS allowlist; no `*` with credentials. Directory listing off. JWT/claims not trusted without verification.
- SSRF is folded in here in 2025: outbound URLs built from input are allowlisted.
- Look for: `params.id`, `req.query.id`, `findUnique({ where: { id } })` without an owner filter, `"use server"` functions without an auth call.

### A02 Security Misconfiguration
- Debug mode, verbose errors or stack traces off in production. Default accounts removed.
- Security headers: CSP, HSTS, `X-Content-Type-Options: nosniff`, `Referrer-Policy`, `frame-ancestors`/`X-Frame-Options`.
- Cloud storage is not public. Unused features, ports and endpoints are disabled.
- Look for: `debug: true`, `cors({ origin: '*' })`, missing header middleware, `NODE_ENV` checks.

### A03 Software Supply Chain Failures
- Lockfile committed. Versions pinned. No unreviewed new dependencies. `npm audit` / `pip-audit` / equivalent is clean or triaged.
- CDN scripts use SRI. CI actions pinned to a SHA. Build pipeline access restricted.
- Third-party skills, plugins and MCP servers reviewed before install.

### A04 Cryptographic Failures
- TLS enforced with HSTS. No sensitive data in URLs.
- Passwords use Argon2id/bcrypt/scrypt (never MD5/SHA1/plain SHA-256). Tokens come from a CSPRNG.
- Sensitive data encrypted at rest. Keys are not in code. No homemade crypto. No ECB mode or static IVs.
- Look for: `md5`, `sha1`, `Math.random()` for tokens, hard-coded keys.

### A05 Injection
- SQL/NoSQL: parameterized or ORM-bound only. Raw query helpers use placeholders.
- OS command: none, or an argument array with no shell.
- XSS: no unsafe HTML sinks without sanitization. CSP present.
- Template, LDAP, XPath, header (CRLF) and log injection.
- Look for: template literals in `query(`, `$queryRawUnsafe`, `exec(`, `child_process`, `eval(`, `dangerouslySetInnerHTML`, `innerHTML =`, `v-html`.

### A06 Insecure Design
- Is there a threat model for sensitive flows? Are abuse cases handled (enumeration, brute force, replay, race conditions)?
- Business limits enforced on the server (quantities, prices, one-time use).
- Least privilege designed in, not added later.

### A07 Authentication Failures
- Proven auth library/provider. Rate limiting, lockout or backoff on login, reset, OTP.
- Generic errors ("invalid credentials"). No user enumeration through reset or sign-up responses or timing.
- Session ID rotated on login and invalidated on logout. Cookies `HttpOnly; Secure; SameSite`.
- Reset tokens: single-use, short-lived, hashed at rest. MFA available for sensitive accounts.

### A08 Software or Data Integrity Failures
- Webhooks: signature **and** timestamp verified, with replay protection.
- No insecure deserialization of untrusted data.
- Client round-tripped data (prices, roles, IDs in hidden fields) is not trusted, or is signed.
- Auto-update and CI artifacts verified.

### A09 Security Logging & Alerting Failures
- Auth successes and failures, access denials, admin actions and validation failures are logged with a request ID and actor.
- No secrets, tokens, passwords or full PII in logs.
- Alerts exist for anomalies. Logs are tamper-resistant and retained.

### A10 Mishandling of Exceptional Conditions
- Errors caught at boundaries. Users get generic messages. Details are logged server-side.
- **Fail closed:** an exception in authn/authz/validation denies access. It never falls through to allow.
- Timeouts on all outbound calls. Partial failures rolled back (transactions). Resource cleanup in `finally`.
- Unchecked return values, empty `catch {}`, and `catch` blocks that return a success value.

---

## OWASP API Security Top 10:2023

| ID | Risk | Check |
|---|---|---|
| API1 | Broken Object Level Authorization | Every object access is scoped to the caller (owner/tenant) |
| API2 | Broken Authentication | Token validation (sig, exp, aud, iss), rate-limited auth endpoints, no keys in URLs |
| API3 | Broken Object Property Level Authorization | Response DTOs omit sensitive fields. Input schemas reject unknown or privileged fields (mass assignment) |
| API4 | Unrestricted Resource Consumption | Rate limits, max page size, body size, upload size, timeouts, cost limits on paid third-party calls |
| API5 | Broken Function Level Authorization | Admin and privileged endpoints check role on the server. No reliance on hidden routes |
| API6 | Unrestricted Access to Sensitive Business Flows | Anti-automation on sign-up, checkout, voting, referrals |
| API7 | Server Side Request Forgery | URL fetches allowlisted. Private/metadata IPs blocked after DNS resolution. Redirects re-checked |
| API8 | Security Misconfiguration | Headers, CORS, TLS, verbose errors, unnecessary HTTP methods |
| API9 | Improper Inventory Management | All endpoints and versions documented. Old or debug versions retired. Non-prod not exposed |
| API10 | Unsafe Consumption of APIs | Third-party responses validated. TLS enforced. Timeouts. Redirects not followed blindly |

---

## Quick grep list (starting points)

```
eval( | new Function( | child_process | exec( | spawn(.*shell
$queryRawUnsafe | query(`  | .raw(  | format( .*SELECT
dangerouslySetInnerHTML | innerHTML | v-html | document.write
cors( | Access-Control-Allow-Origin
md5 | sha1 | Math.random
jwt.decode( (without verify) | verify: false | rejectUnauthorized: false
catch {} | catch (e) {}  | console.log(.*(token|password|secret)
"use server" (then confirm each has auth + validation)
```

A grep hit is a lead. Confirm it by reading the code path before you report it.
