# OWASP WSTG checklist

Source: OWASP Web Security Testing Guide, test IDs from the official checklist (https://github.com/OWASP/wstg/blob/master/checklists/checklist.md). The latest **stable** release is v4.2, and v5 is in development. A few IDs below (for example CONF-12..14, SESS-10/11, INPV-20, ATHZ-05, APIT) come from the in-development checklist, so they may be numbered differently in the v4.2 PDF. Always cite the ID **and** the title.

**Rules of engagement:** run these tests only against the team's own apps, in a local, dev or staging environment you're authorized to test. Never test production or third-party systems without written permission. Prefer code review and defensive automated tests over live attacks. No destructive payloads, no denial-of-service, no real user data.

Each row has two columns:
- **Code review:** what to look for in the source (always possible).
- **Runtime check:** a safe way to confirm it against a running local or staging app.

Mark each row **Pass / Fail / N/A / Not tested**. A row you didn't test must say *Not tested*, never *Pass*.

## Contents
1. INFO – Information Gathering
2. CONF – Configuration & Deployment Management
3. IDNT – Identity Management
4. ATHN – Authentication
5. ATHZ – Authorization
6. SESS – Session Management
7. INPV – Input Validation
8. ERRH – Error Handling
9. CRYP – Cryptography
10. BUSL – Business Logic
11. CLNT – Client-side
12. APIT – API
13. Mapping to OWASP Top 10:2025
14. Report row format

---

## 1. WSTG-INFO: Information Gathering

| ID | Test | Code review | Runtime check |
|---|---|---|---|
| INFO-01 | Search engine discovery / information leakage | Public docs or repos leaking internal URLs, keys, emails | Search your own domain for exposed staging, docs, backups |
| INFO-02 | Fingerprint web server | Server/version banners configured off | Inspect `Server`, `X-Powered-By` response headers |
| INFO-03 | Webserver metafiles | `robots.txt`, `sitemap.xml`, `security.txt` don't reveal hidden admin paths | Fetch them and review what they disclose |
| INFO-04 | Enumerate applications on webserver | Other apps or vhosts on the same host | List the ports and vhosts in your own infra inventory |
| INFO-05 | Webpage content leakage | HTML comments, source maps, debug data, secrets in client bundles | View source. Check for `.map` files in prod. Grep the built JS for keys |
| INFO-06 | Identify entry points | Every route, action, handler, webhook, form, query param | Produce an endpoint inventory (feeds APIT-01 / API9) |
| INFO-07 | Map execution paths | Multi-step flows (checkout, reset, onboarding) | Walk each flow and note state transitions |
| INFO-08 | Fingerprint framework | Framework and version leaks (headers, cookies, default files) | Check headers, cookie names, default error pages |
| INFO-09 | Fingerprint application | Known third-party apps/CMS and their versions | Match against the dependency inventory |
| INFO-10 | Map architecture | CDN, WAF, load balancer, services, DB, third-party APIs | Draw a trust-boundary diagram (input to threat model) |

## 2. WSTG-CONF: Configuration & Deployment Management

| ID | Test | Code review | Runtime check |
|---|---|---|---|
| CONF-01 | Network infrastructure config | Only required ports exposed. Admin services not public | Review firewall/security group rules |
| CONF-02 | Application platform config | Debug off. Default samples removed. Prod config separate | Trigger a 404/500 and confirm no debug output |
| CONF-03 | File extension handling | Server doesn't serve `.bak`, `.inc`, `.env`, `.git` as text or download | Request known sensitive extensions and expect 403/404 |
| CONF-04 | Old, backup, unreferenced files | No backups, dumps or old builds in the web root | Check the deploy artifact contents |
| CONF-05 | Admin interfaces | Admin routes behind auth + role + ideally network restriction | Try admin URLs as anonymous and as a normal user (expect 401/403) |
| CONF-06 | HTTP methods | Only needed methods routed. `TRACE` disabled | `OPTIONS` / unexpected verbs return 405 |
| CONF-07 | HSTS | `Strict-Transport-Security` with an adequate `max-age` | Check the response header over HTTPS |
| CONF-08 | RIA cross-domain policy | No permissive `crossdomain.xml` / `clientaccesspolicy.xml` | Fetch them. They should be absent or restrictive |
| CONF-09 | File permissions | App files not world-writable. Container runs as non-root | Review the Dockerfile `USER` and file modes |
| CONF-10 | Subdomain takeover | DNS records point only to resources you own | Review DNS for dangling CNAMEs to deleted cloud resources |
| CONF-11 | Cloud storage | Buckets private by default. Signed URLs with expiry | Try unauthenticated listing and reads of your buckets |
| CONF-12 | Content Security Policy | CSP defined. No `unsafe-inline`/`unsafe-eval` without nonce/hash | Inspect the header. Check the console for violations |
| CONF-13 | Path confusion | Caching/CDN rules can't be tricked into caching private pages via path suffixes | Request `/account/x.css` and check whether it's cached |
| CONF-14 | Other security headers | `X-Content-Type-Options`, `Referrer-Policy`, `frame-ancestors`, `Permissions-Policy` | Inspect the response headers |

## 3. WSTG-IDNT: Identity Management

| ID | Test | Code review | Runtime check |
|---|---|---|---|
| IDNT-01 | Role definitions | Roles and permissions are documented and least-privilege | Compare the role matrix with what the code enforces |
| IDNT-02 | User registration | Validation, email verification, no role self-assignment | Register with extra fields (`role=admin`) and expect them ignored |
| IDNT-03 | Account provisioning | Only authorized roles can create or elevate users | Try provisioning as a lower role (expect 403) |
| IDNT-04 | Account enumeration | Login, reset and sign-up give identical responses and timing | Compare responses for existing vs non-existing users |
| IDNT-05 | Username policy | Usernames aren't predictable or sequential. Policy enforced | Review username rules |

## 4. WSTG-ATHN: Authentication

| ID | Test | Code review | Runtime check |
|---|---|---|---|
| ATHN-01 | Credentials over encrypted channel | HTTPS-only. No credentials in URLs | Confirm HTTP redirects to HTTPS and forms post to HTTPS |
| ATHN-02 | Default credentials | No seeded admin/test accounts in prod | Review seed scripts and deployment docs |
| ATHN-03 | Weak lockout | Rate limit, backoff or lockout on login, OTP, reset | Repeated failed logins in staging get throttled |
| ATHN-04 | Bypass authentication | Every protected route/action enforces auth server-side | Call protected endpoints without a session (expect 401) |
| ATHN-05 | Vulnerable remember-me | Remember-me token random, hashed at rest, rotatable, revocable | Review token storage and expiry |
| ATHN-06 | Browser cache weakness | `Cache-Control: no-store` on authenticated sensitive pages | Log out, press Back, and confirm no sensitive data shows |
| ATHN-07 | Weak password policy | Length ≥ 8 (≥ 12 preferred), breached-password check, no forced composition quirks | Try weak or common passwords (expect rejection) |
| ATHN-08 | Weak security questions | Avoid security questions. Prefer MFA/email reset | Review whether they exist |
| ATHN-09 | Password change/reset | Reset tokens single-use, short-lived, hashed. Change requires the current password | Reuse a used or expired token (expect failure) |
| ATHN-10 | Weaker alternative channel | Mobile API, legacy or SSO paths enforce the same controls | Compare auth controls across all login channels |
| ATHN-11 | MFA | MFA can't be skipped by calling the next step directly. Recovery codes protected | Try completing login without the MFA step |

## 5. WSTG-ATHZ: Authorization

| ID | Test | Code review | Runtime check |
|---|---|---|---|
| ATHZ-01 | Directory traversal / file include | File paths never built from raw input. Resolve against a base dir and check the prefix | Automated test: `../` input is rejected |
| ATHZ-02 | Bypass authorization schema | Authz enforced server-side on every route/action, not just hidden in the UI | Call a privileged endpoint as a low-privilege user (expect 403) |
| ATHZ-03 | Privilege escalation | Users can't change their own role, plan or tenant via request fields | Send `role`/`isAdmin` in a profile update and expect them ignored |
| ATHZ-04 | IDOR | Queries scoped by owner/tenant (`WHERE id=? AND owner_id=?`) | As user B, request user A's object ID (expect 403/404) |
| ATHZ-05 | OAuth weaknesses | `state` and PKCE used. Exact redirect URI match. Tokens validated (aud/iss/exp) | Review the OAuth config. Try a mismatched `redirect_uri` in staging |

## 6. WSTG-SESS: Session Management

| ID | Test | Code review | Runtime check |
|---|---|---|---|
| SESS-01 | Session management schema | Session IDs from a CSPRNG, long enough, server-validated | Review session library config |
| SESS-02 | Cookie attributes | `HttpOnly`, `Secure`, `SameSite`, tight `Path`/`Domain`, `__Host-` prefix where possible | Inspect `Set-Cookie` |
| SESS-03 | Session fixation | Session ID rotated on login and on privilege change | Compare the session ID before and after login |
| SESS-04 | Exposed session variables | No tokens in URLs, logs or Referer | Check URLs and logs for tokens |
| SESS-05 | CSRF | Cookie-auth state changes need a CSRF token or strict SameSite + origin check | Cross-origin form POST in staging is rejected |
| SESS-06 | Logout | Logout invalidates the session server-side, not just the cookie | Replay the old cookie after logout (expect 401) |
| SESS-07 | Session timeout | Idle and absolute timeouts configured | Wait past the idle timeout, then try an action |
| SESS-08 | Session puzzling | The same session variable isn't reused across flows with different meanings | Review session keys set in reset vs login flows |
| SESS-09 | Session hijacking | Secure cookies, HSTS, optional binding and anomaly detection | Review the cookie and transport config |
| SESS-10 | JSON Web Tokens | Signature verified. `alg` pinned (no `none`). exp/aud/iss checked. Short-lived. Not stored in localStorage when avoidable | Tampered or unsigned JWT is rejected |
| SESS-11 | Concurrent sessions | Policy defined (limit or visibility). Revoke-all on password change | Change the password and confirm other sessions end |

## 7. WSTG-INPV: Input Validation

| ID | Test | Code review | Runtime check |
|---|---|---|---|
| INPV-01 | Reflected XSS | Auto-escaping. No raw HTML sinks with request data | Test with a harmless marker (`<b>x</b>`) and confirm it renders as text |
| INPV-02 | Stored XSS | Stored user content escaped or sanitized (DOMPurify) on output | Save a marker, view it as another user, confirm it's escaped |
| INPV-03 | HTTP verb tampering | Authz applies to all methods, not only GET/POST | Send the same request with other verbs (expect 405/403) |
| INPV-04 | HTTP parameter pollution | Defined behavior for duplicate params. Schema rejects arrays where scalars are expected | Send `?id=1&id=2` and check the handling |
| INPV-05 | SQL injection | Parameterized queries only. No `$queryRawUnsafe`/string concat | Automated test: quote characters are handled safely |
| INPV-06 | LDAP injection | LDAP filters escaped | Review LDAP query builders (N/A if no LDAP) |
| INPV-07 | XML injection / XXE | XML parsers with external entities and DTDs disabled | Review parser config (N/A if no XML) |
| INPV-08 | SSI injection | SSI disabled on the server | Review server config |
| INPV-09 | XPath injection | Parameterized XPath / escaping | Review (N/A if unused) |
| INPV-10 | IMAP/SMTP injection | Email headers built from validated values. CRLF stripped | Review mail-sending code for header injection |
| INPV-11 | Code injection | No `eval`, `new Function`, dynamic `require`/import on input | Grep for dynamic evaluation |
| INPV-12 | Command injection | No shell. `execFile`/`spawn` with an args array. Allowlisted values | Grep for `exec(`, `shell: true` |
| INPV-13 | Format string injection | User input never used as a format string | Review logging and format calls |
| INPV-14 | Incubated vulnerabilities | Stored input that is later rendered, processed or executed by other components (admin panels, exports, jobs) | Trace stored fields to every consumer |
| INPV-15 | HTTP splitting/smuggling | No CRLF in headers from input. Proxy and app agree on request parsing | Review header-setting code and proxy config |
| INPV-16 | HTTP incoming requests | Inspect what reaches the app behind proxies (trusted `X-Forwarded-*` only) | Confirm `trust proxy` is set correctly |
| INPV-17 | Host header injection | Absolute URLs (reset links) built from config, not the `Host` header | Send a reset with a spoofed Host and check the link domain |
| INPV-18 | Server-side template injection | User input is template **data**, never template **source** | Review template rendering calls |
| INPV-19 | SSRF | Outbound URLs allowlisted. Private/metadata IPs blocked after DNS resolution. Redirects re-checked | Automated test: internal IPs are rejected |
| INPV-20 | Mass assignment | Schemas pick allowed fields. No `update(req.body)` | Send extra privileged fields and expect them ignored |

## 8. WSTG-ERRH: Error Handling

| ID | Test | Code review | Runtime check |
|---|---|---|---|
| ERRH-01 | Improper error handling | Central error handler. Generic messages. Fail closed | Send malformed input and get a clean 4xx with no internals |
| ERRH-02 | Stack traces | Stack traces only in server logs, never in responses | Force an error in staging and confirm no stack trace |

## 9. WSTG-CRYP: Cryptography

| ID | Test | Code review | Runtime check |
|---|---|---|---|
| CRYP-01 | Weak TLS | TLS 1.2+ only, strong ciphers, valid certs | Run an SSL scanner against your own staging host |
| CRYP-02 | Padding oracle | Authenticated encryption (AES-GCM / ChaCha20-Poly1305). Uniform decrypt errors | Review crypto usage |
| CRYP-03 | Sensitive data over unencrypted channels | No HTTP endpoints, mixed content or plaintext internal hops for secrets | Check for mixed content and non-TLS calls |
| CRYP-04 | Weak crypto primitives | No MD5/SHA1 for security. Argon2id/bcrypt for passwords. CSPRNG for tokens | Grep for `md5`, `sha1`, `Math.random` |

## 10. WSTG-BUSL: Business Logic

| ID | Test | Code review | Runtime check |
|---|---|---|---|
| BUSL-01 | Business data validation | Server enforces business rules (quantities ≥ 1, dates valid, prices from DB) | Submit negative or zero quantities (expect rejection) |
| BUSL-02 | Forge requests | Hidden or disabled fields aren't trusted. Price and discount computed server-side | Modify the price in a request and confirm the server ignores it |
| BUSL-03 | Integrity checks | Client-round-tripped data is signed or re-derived | Tamper with signed data (expect rejection) |
| BUSL-04 | Process timing | Race conditions handled (transactions, unique constraints, idempotency keys) | Parallel requests for one-time actions produce a single effect |
| BUSL-05 | Function use limits | Coupons, votes and invites enforce limits server-side | Reuse a single-use coupon (expect failure) |
| BUSL-06 | Workflow circumvention | Each step verifies the previous steps completed (server-side state) | Call the final step directly (expect rejection) |
| BUSL-07 | Application misuse defenses | Rate limiting, anomaly detection, alerting on abuse | Automated burst gets throttled and logged |
| BUSL-08 | Unexpected file types | Allowlist by content (magic bytes), not just extension | Upload a renamed file of the wrong type (expect rejection) |
| BUSL-09 | Malicious files | Size limits, AV scan if relevant, stored outside web root, random names, safe `Content-Type`/`Content-Disposition` | Upload an HTML/SVG file and confirm it isn't served inline as active content |
| BUSL-10 | Payment functionality | Amounts and currency server-side. Provider webhooks verified. Idempotent order creation | Tamper with the amount and replay the webhook (expect rejection or no double-apply) |

## 11. WSTG-CLNT: Client-side

| ID | Test | Code review | Runtime check |
|---|---|---|---|
| CLNT-01 | DOM-based XSS | No `innerHTML`/`document.write`/`eval` fed from `location`, `postMessage`, storage | Grep for DOM sinks. Test with a harmless marker in the hash |
| CLNT-02 | JavaScript execution | No `javascript:` URLs from user data. `href` values validated | User-supplied links restricted to `https:` |
| CLNT-03 | HTML injection | Markup from users escaped or sanitized | Marker renders as text |
| CLNT-04 | Client-side URL redirect | Redirect targets allowlisted or relative-only | `?next=https://evil.example` is rejected |
| CLNT-05 | CSS injection | User input never placed in `style` or CSS without validation | Review dynamic styles |
| CLNT-06 | Client-side resource manipulation | Script, iframe and fetch URLs not controlled by input | Review dynamic `src`/`href` |
| CLNT-07 | CORS | Explicit origin allowlist. No reflected Origin with credentials | Send a foreign `Origin` and confirm it isn't echoed |
| CLNT-08 | Cross-site flashing | N/A unless legacy Flash content exists | Confirm no `.swf` |
| CLNT-09 | Clickjacking | `frame-ancestors 'none'/'self'` or `X-Frame-Options` | Try to frame the page from another origin |
| CLNT-10 | WebSockets | Origin checked. Auth on connect **and** per message. Input validated. `wss://` only | Connect from a foreign origin or without auth (expect rejection) |
| CLNT-11 | Web messaging | `postMessage` handlers verify `event.origin`. Specific target origin, never `*` for sensitive data | Grep `addEventListener('message'` |
| CLNT-12 | Browser storage | No tokens, secrets or PII in localStorage/sessionStorage/IndexedDB | Inspect storage after login |
| CLNT-13 | Cross-site script inclusion (XSSI) | Sensitive JSON not served as executable JS. Correct `Content-Type` + `nosniff` | Review JSON endpoints' headers |
| CLNT-14 | Reverse tabnabbing | `target="_blank"` links to external sites use `rel="noopener noreferrer"` | Grep `target="_blank"` |

## 12. WSTG-APIT: API

| ID | Test | Code review | Runtime check |
|---|---|---|---|
| APIT-01 | API reconnaissance | Complete endpoint inventory (OpenAPI). Old versions and debug endpoints retired. Introspection off in prod | Compare the routes in code with the published spec (API9) |
| APIT-02 | Broken object level authorization | Every object access is owner/tenant scoped | As user B, access user A's resources (expect 403/404) (API1) |
| APIT-99 | GraphQL | Introspection off in prod. Depth, complexity and batch limits. Field-level authz | Send a deep nested query (expect rejection) (API4) |

Cover the rest of the API surface with the API Security Top 10 table in `owasp-checklist.md`.

---

## 13. Mapping to OWASP Top 10:2025 (for reporting)

| Top 10:2025 | Main WSTG sections |
|---|---|
| A01 Broken Access Control | ATHZ-01..05, CONF-05, INPV-19 (SSRF), CLNT-07, APIT-02 |
| A02 Security Misconfiguration | CONF-01..14, INFO-02/03/05/08, ERRH-02 |
| A03 Software Supply Chain Failures | INFO-08/09 (versions), plus dependency audit (not covered by WSTG) |
| A04 Cryptographic Failures | CRYP-01..04, ATHN-01, SESS-02 |
| A05 Injection | INPV-01..18, CLNT-01..06 |
| A06 Insecure Design | BUSL-01..10, INFO-07/10 |
| A07 Authentication Failures | ATHN-01..11, IDNT-04/05, SESS-01..11 |
| A08 Software or Data Integrity Failures | BUSL-03, SESS-10, INPV-20 |
| A09 Security Logging & Alerting Failures | BUSL-07 (plus log review) |
| A10 Mishandling of Exceptional Conditions | ERRH-01/02, BUSL-04 |

## 14. Report row format

```
WSTG-<ID> <title> - Pass | Fail | N/A | Not tested
  Evidence: <file:line, or the safe request/response observed in staging>
  Top 10: <A0x:2025>   Severity (if Fail): <Critical/High/Medium/Low>
  Fix + defensive test: <...>
```
