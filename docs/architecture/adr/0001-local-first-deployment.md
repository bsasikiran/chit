# ADR-0001: Use local-first deployment

- Status: Accepted
- Date: 2026-09-23

## Context

The pilot handles household schedules, presence, device and energy information.

## Decision

Run core ingestion, normalization, policy, dashboard and storage components on household-controlled infrastructure. Cloud integrations are explicit external sources, not the default processing environment.

## Consequences

Local deployment improves control but adds installation, updates, backup and observability responsibilities.

## Supersession

If this decision changes, add a new ADR that identifies this record as superseded. Do not rewrite the accepted decision history.
