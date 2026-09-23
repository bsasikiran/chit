---
id: US-103
title: Connect calendar and weather
epic: EPIC-01
priority: must
status: ready
release: pilot-1
journey_touchpoints:
- D2
- FL2
persona: Household Administrator
dependencies: []
architecture_refs:
- docs/architecture/integrations.md
components:
- connectors
- dashboard-api
---

# US-103: Connect calendar and weather

## User story

As a **Household Administrator**, I want to connect at least one real calendar and one weather source, so that the dashboard reflects my household plans and local conditions.

## Acceptance criteria

### AC-1: Calendar connection

Given valid calendar credentials, when the administrator authorises the connector, then upcoming events can be ingested.

### AC-2: Weather connection

Given a valid location, when setup completes, then current and forecast weather can be retrieved.

### AC-3: Permission failure

Given authorisation fails, then setup explains the failure without exposing credentials.

## Product constraints

- Preserve applicable provenance and data-state metadata.
- Do not add external side effects unless explicitly required above.
- Apply household access and screen-safe policies before returning sensitive information.

## Definition of done

- Acceptance criteria have automated coverage where technically feasible.
- Relevant contract, architecture and operational documentation is updated.
- Error, unavailable and stale paths have been verified.
