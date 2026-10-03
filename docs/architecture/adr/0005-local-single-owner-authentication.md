# ADR-0005: Use a single local owner account for the pilot

- Status: Accepted
- Date: 2026-10-01

## Context

Chit currently runs as a household-controlled loopback service and has no account system. Household member records describe people and their schedules; they are not login identities. The pilot needs a basic sign-in boundary for setup and household calendar data without adding an external identity dependency.

## Decision

- Start with exactly one local owner login for the local Chit installation. The login is not hardcoded in source; bootstrap it once through `server/bootstrap_owner.py`.
- Store an Argon2id password hash in the encrypted SQLite database. Never store plaintext passwords or commit credentials.
- Issue opaque, database-backed sessions with a 12-hour expiry. Store only the session-token hash; set the browser cookie `HttpOnly`, `SameSite=Strict`, and `Path=/`.
- Require a session for all pages and APIs, including the TV dashboard, setup, and calendar pages. Require a session-bound CSRF token on state-changing requests. Check same-origin on login and throttle repeated login failures in the local server process.
- Bind the pilot server to `127.0.0.1` only. This decision does not authorize LAN or public exposure.
- Household adult/child/helper profiles remain data records, not accounts. Multi-user membership, role authorization, invitations, password recovery and external identity providers are deferred.
- Before public deployment or LAN exposure, replace or supersede this decision with a reviewed identity, TLS, authorization, recovery and operational-security design. Google/OIDC may be evaluated then.

## Consequences

The pilot has a small local sign-in flow with no required network identity provider. The owner must retain the password; account recovery is not implemented. The local loopback boundary remains part of the security model. This provides owner authentication, not complete member-level authorization or a secure public deployment.

## Supersession

If this decision changes, add a new ADR that identifies this record as superseded. Do not rewrite the accepted decision history.