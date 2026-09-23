# ADR-0002: Use Home Assistant as an optional read-only integration boundary

- Status: Accepted
- Date: 2026-09-23

## Context

Home Assistant already aggregates many household device and energy entities, but Chit must not become a device-control surface during trust-building.

## Decision

Integrate Home Assistant through an entity allowlist and read-only credentials. Do not expose service calls or command APIs to pilot application components.

## Consequences

Chit can reuse existing integrations while reducing side-effect risk. Future control requires a superseding ADR.

## Supersession

If this decision changes, add a new ADR that identifies this record as superseded. Do not rewrite the accepted decision history.
