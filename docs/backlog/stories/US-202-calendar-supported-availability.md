---
id: US-202
title: Calendar-supported availability
epic: EPIC-02
priority: must
status: ready
release: pilot-2
journey_touchpoints:
- DU2
- DU3
persona: Household Coordinator
dependencies:
- US-103
architecture_refs:
- docs/architecture/data-model.md
- docs/architecture/security-privacy.md
components:
- dashboard-api
- dashboard-ui
---

# US-202: Calendar-supported availability

## User story

As a **Household Coordinator**, I want to see each member’s calendar-based availability, so that I can identify who may be able to help with upcoming commitments.

## Acceptance criteria

### AC-1: Supported status

Given a member has an authorised calendar, then Chit derives busy or free only for the relevant displayed period.

### AC-2: Source basis

Given availability is shown, then the supporting calendar and update time are accessible.

### AC-3: Privacy

Given an event is private, then availability may be shown without exposing its title or details.

## Product constraints

- Preserve applicable provenance and data-state metadata.
- Do not add external side effects unless explicitly required above.
- Apply household access and screen-safe policies before returning sensitive information.

## Definition of done

- Acceptance criteria have automated coverage where technically feasible.
- Relevant contract, architecture and operational documentation is updated.
- Error, unavailable and stale paths have been verified.
