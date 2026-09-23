---
id: US-401
title: Chores and appliance context
epic: EPIC-04
priority: must
status: ready
release: pilot-2
journey_touchpoints:
- DU1
- DU4
persona: Household Coordinator
dependencies:
- US-104
- US-201
architecture_refs:
- docs/architecture/integrations.md
components:
- dashboard-api
- dashboard-ui
---

# US-401: Chores and appliance context

## User story

As a **Household Coordinator**, I want to see unfinished chores, connected appliance states and upcoming appliance schedules together, so that I can understand what still needs attention at home.

## Acceptance criteria

### AC-1: Combined context

Given chore and approved appliance data exist, then the household card displays unfinished chores, current states and schedules together.

### AC-2: Provenance

Given appliance information appears, then source, data state and freshness are available.

### AC-3: No control

Given the user views an appliance, then no control action is offered in the pilot.

## Product constraints

- Preserve applicable provenance and data-state metadata.
- Do not add external side effects unless explicitly required above.
- Apply household access and screen-safe policies before returning sensitive information.

## Definition of done

- Acceptance criteria have automated coverage where technically feasible.
- Relevant contract, architecture and operational documentation is updated.
- Error, unavailable and stale paths have been verified.
