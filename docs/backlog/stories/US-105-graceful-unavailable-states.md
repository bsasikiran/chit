---
id: US-105
title: Graceful unavailable states
epic: EPIC-01
priority: must
status: ready
release: pilot-1
journey_touchpoints:
- FL3
- DU3
- DU5
persona: Household Member
dependencies:
- US-101
architecture_refs:
- docs/architecture/data-model.md
components:
- dashboard-api
- dashboard-ui
---

# US-105: Graceful unavailable states

## User story

As a **Household Member**, I want a clear unavailable state when a source is disconnected or unsupported, so that missing data is not mistaken for a real status.

## Acceptance criteria

### AC-1: Unavailable label

Given required source data is absent, when a card renders, then it displays unavailable rather than a zero, empty success state or inferred value.

### AC-2: Reason visible

Given data is unavailable, then the user can see whether the cause is unconfigured, disconnected, unsupported or unknown.

### AC-3: Partial dashboard

Given one source is unavailable, then unaffected cards continue to render.

## Product constraints

- Preserve applicable provenance and data-state metadata.
- Do not add external side effects unless explicitly required above.
- Apply household access and screen-safe policies before returning sensitive information.

## Definition of done

- Acceptance criteria have automated coverage where technically feasible.
- Relevant contract, architecture and operational documentation is updated.
- Error, unavailable and stale paths have been verified.
