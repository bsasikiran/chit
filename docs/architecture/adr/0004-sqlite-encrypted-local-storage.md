# ADR-0004: Use SQLite with encrypted local storage

- Status: Accepted
- Date: 2026-10-01

## Context

Chit needs lightweight, free-to-deploy persistence for structured household data on household-controlled infrastructure. It must be practical to bundle, fast for household-scale queries, and suitable for combining normalized source data and deriving Chit-owned records such as tasks. Subscribed calendars remain externally authoritative; Chit does not need a durable mirror of every subscribed event.

## Decision

- Use SQLite as the embedded relational database for Chit-owned structured data on the local host.
- Require SQLCipher encryption at rest for the database. The initial Python implementation uses the `sqlcipher3-wheels` SQLCipher 4 driver. Supply a 32-byte key through `CHIT_DB_KEY_HEX`; never store the key alongside the database or in source control. Production key provisioning, rotation, recovery and unattended startup remain deployment decisions.
- Include database backups and other persisted household files in the encryption and retention design.
- Access the database through the local application/API boundary. Browser clients must not open or manage the database file directly.
- Do not persist a complete copy of subscribed calendar events by default. Store source configuration, mappings, and Chit-owned derived records; any event cache must have a documented need, bounded retention, and explicit stale/deletion behavior.
- This decision does not select the application's authentication, authorization, household membership, or member access-management design. Those remain to be decided separately; encryption at rest does not replace application access controls.

## Consequences

SQLite provides a compact, transactional store without a separate database server and suits a household-scale local deployment. The local application service owns database access and migrations.

The deployment must define backup/restore behavior, protect backups and persisted files, and test database migrations. Keep the database on local storage rather than a shared network filesystem. Revisit the database choice through a new ADR if Chit requires distributed multi-writer operation or a centrally hosted workload with materially different concurrency needs.

## Supersession

If this decision changes, add a new ADR that identifies this record as superseded. Do not rewrite the accepted decision history.
