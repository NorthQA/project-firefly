# API security controls

Nine layered controls every API should have. Use this file when **designing** an API (pick and plan each control), **building** one (apply them), or **auditing** one (check each, and mark Pass / Fail / N/A / Not checked).

No single control is enough. The gateway and firewall don't replace authorization in the code, and validation doesn't replace parameterized queries. Each layer assumes the others can fail (defense in depth).

```
Client ─HTTPS─► Firewall/WAF ─► API Gateway ─► Service ─► Data
                (network)       (TLS, authN,    (authZ per object,
                                 rate limit,     validation again,
                                 validation,     business rules)
                                 versioning)
Identity: OAuth2/OIDC (delegated access) + WebAuthn/passkeys (phishing-resistant login)
```

Controls that touch infrastructure (gateway, firewall/WAF, identity provider) or auth need **tech lead review**.

## Contents
1. OAuth2 / OpenID Connect
2. HTTPS (TLS)
3. WebAuthn / passkeys
4. API Gateway
5. Firewall / WAF
6. API Versioning
7. Rate Limiting
8. Authorization
9. Input Validation
10. New-endpoint checklist

---

## 1. OAuth2 / OpenID Connect

**What it is:** the resource owner (the user) lets a client get a token from an **authorization server**, and the client uses it at a **resource server** (the API). OAuth2 is for *authorization* (delegated access). For *login*, use **OpenID Connect** on top of it.

**Do:**
- Use the **Authorization Code flow with PKCE** for all clients (web, SPA, mobile). Don't use the Implicit or Resource Owner Password flows (deprecated by the OAuth 2.0 Security BCP / OAuth 2.1).
- Use `client_credentials` for service-to-service calls, with a separate client per service.
- Use `state` (CSRF) and `nonce` (OIDC). The redirect URI must match exactly (no wildcards).
- The API validates every token: signature (pinned algorithm, no `none`), `iss`, `aud` (must be *this* API), `exp`/`nbf`, and scopes.
- Keep access tokens short-lived. Rotate refresh tokens and support revocation.
- Scopes follow least privilege (`tasks:read` separate from `tasks:write`).
- Client secrets stay server-side only. For browser apps, prefer the **BFF pattern**: the server keeps the tokens and the browser gets an `HttpOnly` session cookie. Don't put tokens in localStorage.
- Prefer a proven identity provider or library over a homemade authorization server.

**Check:** WSTG-ATHZ-05, WSTG-SESS-10 · A07, A01 · API2.

## 2. HTTPS (TLS)

**What it is:** a TCP connection plus a TLS handshake (public-key crypto agrees on session keys), so all data is encrypted and the server is authenticated.

**Do:**
- Use TLS 1.2+ (prefer 1.3) with modern cipher suites, and automate certificate renewal.
- Send HSTS (`max-age` ≥ 1 year, `includeSubDomains`, then preload when ready).
- For **APIs, reject plain HTTP**. Don't redirect it: the first request may already have sent a token in clear text. Web pages may redirect HTTP → HTTPS.
- Encrypt internal service-to-service traffic too (TLS or mTLS). Don't assume "inside the network" is safe.
- No secrets, tokens or PII in URLs (they end up in logs and Referer headers).

**Check:** WSTG-CRYP-01/03, WSTG-CONF-07, WSTG-ATHN-01 · A04.

## 3. WebAuthn / passkeys

**What it is:** phishing-resistant, passwordless login using public-key credentials. The authenticator is either **internal/platform** (Touch ID, Windows Hello, a phone) or **external/roaming** (a security key). The browser (client platform) mediates between the authenticator and your server (the relying party).

**Do:**
- Use a maintained WebAuthn server library. Never hand-roll verification.
- Challenges: random, single-use, short TTL, stored server-side, and bound to the session.
- Verify origin and RP ID, the signature, user presence/verification (require UV for sensitive actions), and the signature counter or backup flags per the library's guidance.
- Store only the credential ID, the public key and metadata. Allow multiple passkeys per account.
- **Account recovery must not be weaker** than the passkey. A weak email or SMS fallback defeats it.
- Offer passkeys as a primary login or as MFA. Step-up authentication for sensitive actions.

**Check:** WSTG-ATHN-10/11 · A07.

## 4. API Gateway

**What it is:** a single entry point in front of the services that centralizes cross-cutting concerns.

**Do:**
- Centralize TLS termination, token validation (authN), rate limiting, request size limits, schema validation, CORS, request IDs, access logs and routing.
- Make services reachable **only through the gateway**: private network, security groups, or mTLS.
- **Strip client-supplied identity headers** (`X-User-Id`, `X-Forwarded-*`). Only the gateway sets them, and services trust them only from the gateway.
- The gateway does **coarse** checks. Services still do **object-level authorization** and business validation. A gateway never replaces authz in code.
- Keep the gateway's route list as the API inventory, and remove old or debug routes.

**Check:** WSTG-CONF-05, WSTG-APIT-01, WSTG-INPV-16 · A01, A02 · API8, API9.

## 5. Firewall / WAF

**What it is:** an **outer firewall** that exposes only public ports (443) at the edge, an **inner firewall** that separates tiers (for example, the DB is reachable only from the app subnet), and a **WAF** that filters common layer-7 attacks.

**Do:**
- Default-deny security groups and network policies. Allow only what each tier needs (least privilege for networks).
- Keep admin interfaces, databases and internal services off the public internet.
- Filter egress (restrict outbound destinations). This limits the impact of SSRF and data exfiltration.
- WAF with a maintained rule set (e.g. OWASP Core Rule Set). Tune it in detection mode first, then block.
- A WAF is **defense in depth, not a fix**. Still fix the vulnerable code.

**Check:** WSTG-CONF-01, WSTG-CONF-05, WSTG-INPV-19 · A02, A01 (SSRF) · API7, API8.

## 6. API Versioning

**What it is:** clients target a stable contract. `GET /api/v1/users/123` ✅ vs `GET /users/123` ❌ (no version, so any change can break or silently alter clients).

**Do:**
- Version from day one, with **one** scheme used everywhere: URL prefix (`/api/v1/...`, preferred for visibility) or a header. Don't mix them.
- Never make breaking changes within a version: add fields and endpoints, don't change or remove them. Breaking changes go into `v2`.
- Deprecation policy: announce it, send the `Deprecation` and `Sunset` headers, set a retirement date, then **actually retire** old versions.
- Every live version gets the same security controls and patches. Forgotten old versions are a classic breach path.
- Keep an inventory (OpenAPI spec per version) and make sure no unlisted, debug or beta versions are exposed in production.

**Check:** WSTG-APIT-01 · API9 · A02.

## 7. Rate Limiting

**What it is:** caps on how often a client can call, with rules based on **IP, user or API key, and action group**.

**Do:**
- Layered limits: a global per-IP limit at the gateway, plus per-user/API-key limits, plus **stricter per-action limits** (login, OTP, password reset, sign-up, search, export, and anything expensive or paid).
- Use a shared store (Redis) so limits hold across instances. In-memory counters break with more than one instance.
- Algorithm: token bucket or sliding window.
- On limit, return `429 Too Many Requests` with `Retry-After` (and `RateLimit-*` headers if you use them).
- Behind a proxy, derive the client IP only from **trusted** proxy headers. Otherwise attackers spoof `X-Forwarded-For`.
- Pair it with other resource limits: max body size, max page size, query timeouts, and GraphQL depth and complexity limits.
- Log and alert when limits are hit, since that may signal abuse.

**Check:** WSTG-ATHN-03, WSTG-BUSL-05/07 · A07, A06 · API4, API6.

## 8. Authorization

**What it is:** deciding what an authenticated caller may do. For example, a user **can view** a resource but **can't modify** it.

**Do:**
- **Deny by default.** Grant explicit permissions per action: `read`, `create`, `update`, `delete` are separate, and read never implies write.
- Choose a model deliberately: RBAC (roles → permissions) for simple apps, ABAC or relationship-based rules (ownership, team, tenant) when access depends on the data.
- **Centralize the policy** in one module (e.g. `server/auth/policies.ts` → `can(user, "update", task)`) and call it in the **service layer**, server-side, for every request.
- Check all three levels:
  - **Object:** may this user access *this* record? (BOLA/IDOR: scope queries by owner or tenant)
  - **Property:** may they see or change *this field*? (BOPLA: response DTOs hide fields, and input schemas reject privileged fields like `role`)
  - **Function:** may they call *this operation* at all? (BFLA: admin endpoints)
- The UI hiding a button is not authorization. Test the API directly.
- Test a **role × action matrix**: for each role, allowed actions succeed and every other action returns 403 (or 404 to hide existence).

**Check:** WSTG-ATHZ-01..04, WSTG-IDNT-01 · A01 · API1, API3, API5.

## 9. Input Validation

**What it is:** a validator checks every request **before** business logic runs, at the gateway **and** again in the service.

**Do:**
- Schema-validate every input (body, query, path, headers, files): type, required, length, format, range and enum, using an **allowlist**.
- Reject unknown fields (this prevents mass assignment). Enforce `Content-Type` and max body size.
- Validate at the gateway (e.g. against the OpenAPI schema) **and** in the app (zod/pydantic). The app must not rely on the gateway alone.
- Canonicalize before validating (decode, normalize Unicode and paths).
- Business validation (quantity ≥ 1, dates in order, price from the DB) happens server-side in the service.
- Validation **doesn't replace** parameterized queries, output encoding or authorization. Keep all of them.
- Return `400`/`422` with a consistent error shape. Don't echo raw input back unescaped, and don't leak internals.

**Check:** WSTG-INPV-01..20, WSTG-BUSL-01 · A05, A06 · API3, API10.

---

## 10. New-endpoint checklist (copy into the plan or PR)

```
[ ] Versioned, resource-based route (GET/POST/PUT/PATCH/DELETE /api/v1/<resources>[/:id])
[ ] HTTPS only; no secrets in URL
[ ] AuthN: token/session validated (OAuth2/OIDC or session; passkeys/MFA where required)
[ ] AuthZ: permission + object-level + property-level check via central policy
[ ] Input validated by schema (unknown fields rejected, size limits)
[ ] Rate limit rule set (per user/IP; stricter for sensitive actions)
[ ] Exposed only via gateway; behind firewall/WAF; no direct service access
[ ] Idempotent where required (Idempotency-Key for POST that creates/charges)
[ ] Errors: correct status code, generic message, logged with request ID (no secrets/PII)
[ ] Added to API inventory/OpenAPI spec; tests for 401, 403, 404, 422, 429 paths
```
