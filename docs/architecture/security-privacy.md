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

- Authenticate administrative and sensitive routes.
- Authorise every protected read and configuration change.
- Redact or aggregate sensitive fields before generating shared-display responses.
- Encrypt secrets at rest and transport data over authenticated encrypted channels.
- Avoid logging tokens, private event details, health information or full provider payloads.
- Record configuration and permission changes in an audit log.

## Screen-safe policy

The safe projection may show that a person is busy while hiding event title, location, notes and attendees. Sensitive categories are hidden by default. A privileged reveal requires authenticated, authorised interaction and must not persist on the shared screen.

## Threats to test

- Cross-household and cross-member access
- Stale cache revealing revoked information
- Connector over-permissioning
- Prompt or content injection from external calendar text
- Secrets committed to Git or exposed in logs
- Forecast/demo data presented as measured
