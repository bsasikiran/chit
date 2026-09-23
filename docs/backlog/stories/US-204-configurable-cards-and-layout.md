---
id: US-204
title: Configurable cards and layout
epic: EPIC-02
priority: should
status: ready
release: pilot-2
journey_touchpoints:
- FL5
- DU1
persona: Household Coordinator
dependencies:
- US-201
architecture_refs:
- docs/architecture/architecture-overview.md
components:
- dashboard-ui
---

# US-204: Configurable cards and layout

## User story

As a **Household Coordinator**, I want to choose which cards appear and arrange them for my household, so that the most relevant information receives the most attention.

## Acceptance criteria

### AC-1: Card selection

Given an authorised administrator, when they enable or disable an optional card, then the shared view reflects the selection.

### AC-2: Ordering

Given enabled cards, when their order is changed, then the layout persists for that display profile.

### AC-3: Required trust cues

Given a layout change, then provenance, unavailable and privacy indicators cannot be disabled.

## Product constraints

- Preserve applicable provenance and data-state metadata.
- Do not add external side effects unless explicitly required above.
- Apply household access and screen-safe policies before returning sensitive information.

## Definition of done

- Acceptance criteria have automated coverage where technically feasible.
- Relevant contract, architecture and operational documentation is updated.
- Error, unavailable and stale paths have been verified.
