# Security and Privacy

## Trust boundaries

- Household boundary: data from one household cannot be accessed by another.
- Member boundary: sensitive data follows person-specific grants.
- Shared-display boundary: unauthenticated viewing receives screen-safe data only.
- Connector boundary: every connector has least-privilege credentials and an entity allowlist.
- Cloud boundary: local data is not sent to cloud processors without an approved purpose and policy.

## Roles

| Role | Intended access |
|---|---|
| Administrator | Configure household, sources, displays and policies |
| Member | View authorised household and personal information |
| Shared display | Read screen-safe projection only; no administration |

## Controls

- Authenticate setup, household calendar and their APIs with the single local owner account described in [ADR-0005](adr/0005-local-single-owner-authentication.md).
- Store owner passwords as Argon2id hashes; use opaque expiring sessions, HttpOnly/SameSite cookies, same-origin login checks, CSRF validation on writes, and throttled login attempts.
- Keep the pilot HTTP service loopback-only. Do not expose it to the LAN or public internet; this authentication slice does not provide TLS, multi-user authorization or account recovery.
- The single owner account currently authenticates the local installation; it does not implement separate household/member grants. Add those before multiple accounts or households are exposed to different people.
- Authorise every protected read and configuration change according to the current local-owner boundary.
- Redact or aggregate sensitive fields before generating shared-display responses.
- Encrypt the SQLite database at rest. Protect backups and other persisted household files under the same storage/retention design; define key provisioning and lifecycle before implementation.
- Encrypt secrets at rest and transport data over authenticated encrypted channels.
- Avoid logging tokens, private event details, health information or full provider payloads.
- Record configuration and permission changes in an audit log.

## Screen-safe policy

The safe projection may show that a person is busy while hiding event title, location, notes and attendees. Sensitive categories are hidden by default. A privileged reveal requires authenticated, authorised interaction and must not persist on the shared screen.

## Threats to test

- Database, backup or attachment disclosure, including key exposure and restore paths
- Cross-household and cross-member access
- Stale cache revealing revoked information
- Connector over-permissioning
- Prompt or content injection from external calendar text
- Secrets committed to Git or exposed in logs
- Forecast/demo data presented as measured
