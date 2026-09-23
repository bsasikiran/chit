---
id: US-201
title: Shared household dashboard
epic: EPIC-02
priority: must
status: ready
release: pilot-2
journey_touchpoints:
- FL5
- DU1
- DU2
persona: Household Member
dependencies:
- US-103
architecture_refs:
- docs/architecture/architecture-overview.md
components:
- dashboard-ui
- dashboard-api
---

# US-201: Shared household dashboard

## User story

As a **Household Member**, I want a readable TV or tablet view showing weather, hourly outlook, week overview, the next three days and outstanding chores, so that I can understand household priorities at a glance.

## Acceptance criteria

### AC-1: Required cards

Given required sources are connected, then the shared view shows current weather, hourly outlook, week overview, three-day events and outstanding chores.

### AC-2: Viewing distance

Given the configured shared-display mode, then primary content remains readable without interaction at the target display resolution.

### AC-3: Honest fallback

Given a card lacks data, then it uses the approved unavailable state rather than silently replacing it with demo data.

## Product constraints

- Preserve applicable provenance and data-state metadata.
- Do not add external side effects unless explicitly required above.
- Apply household access and screen-safe policies before returning sensitive information.

## Definition of done

- Acceptance criteria have automated coverage where technically feasible.
- Relevant contract, architecture and operational documentation is updated.
- Error, unavailable and stale paths have been verified.
