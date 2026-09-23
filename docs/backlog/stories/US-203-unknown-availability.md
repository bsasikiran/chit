---
id: US-203
title: Unknown availability
epic: EPIC-02
priority: must
status: ready
release: pilot-2
journey_touchpoints:
- DU3
- DU5
persona: Household Member
dependencies:
- US-202
architecture_refs:
- docs/architecture/data-model.md
components:
- dashboard-api
- dashboard-ui
---

# US-203: Unknown availability

## User story

As a **Household Member**, I want missing calendar information shown as unknown rather than available, so that I do not make plans based on an unsupported assumption.

## Acceptance criteria

### AC-1: Missing calendar

Given no authorised calendar exists for a member, then availability displays unknown.

### AC-2: Stale calendar

Given calendar data exceeds its freshness threshold, then availability is stale or unknown, not free.

### AC-3: No inference

Given a time range contains no retrieved events but synchronization is incomplete, then Chit does not assert availability.

## Product constraints

- Preserve applicable provenance and data-state metadata.
- Do not add external side effects unless explicitly required above.
- Apply household access and screen-safe policies before returning sensitive information.

## Definition of done

- Acceptance criteria have automated coverage where technically feasible.
- Relevant contract, architecture and operational documentation is updated.
- Error, unavailable and stale paths have been verified.
