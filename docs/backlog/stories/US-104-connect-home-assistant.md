---
id: US-104
title: Connect Home Assistant
epic: EPIC-01
priority: must
status: ready
release: pilot-1
journey_touchpoints:
- D2
- FL2
- DU4
persona: Household Administrator
dependencies: []
architecture_refs:
- docs/architecture/integrations.md
- docs/architecture/security-privacy.md
components:
- connectors
- home-assistant
---

# US-104: Connect Home Assistant

## User story

As a **Household Administrator**, I want to connect Home Assistant when it is available, so that relevant home and energy information can appear alongside household plans.

## Acceptance criteria

### AC-1: Optional connection

Given no Home Assistant instance is configured, then calendar and weather functions remain usable.

### AC-2: Read-only access

Given Home Assistant is connected, then Chit reads only approved entities and cannot invoke control services.

### AC-3: Connection health

Given the instance becomes unreachable, then its data is marked stale or unavailable and the rest of the dashboard remains available.

## Product constraints

- Preserve applicable provenance and data-state metadata.
- Do not add external side effects unless explicitly required above.
- Apply household access and screen-safe policies before returning sensitive information.

## Definition of done

- Acceptance criteria have automated coverage where technically feasible.
- Relevant contract, architecture and operational documentation is updated.
- Error, unavailable and stale paths have been verified.
