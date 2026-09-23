---
id: US-304
title: Screen-safe mode
epic: EPIC-03
priority: must
status: ready
release: pilot-1
journey_touchpoints:
- D3
- FL4
- DU1
persona: Privacy-Conscious Member
dependencies:
- US-303
architecture_refs:
- docs/architecture/security-privacy.md
components:
- dashboard-api
- dashboard-ui
---

# US-304: Screen-safe mode

## User story

As a **Privacy-Conscious Member**, I want a screen-safe mode that hides sensitive details on the shared display, so that visitors and unauthorised viewers cannot see private information.

## Acceptance criteria

### AC-1: Safe default

Given a shared display session, then screen-safe mode is enabled by default.

### AC-2: Sensitive content

Given private event or person data, then the display masks details according to policy before rendering.

### AC-3: Privileged reveal

Given a user requests sensitive details, then successful authentication and authorisation are required before disclosure.

## Product constraints

- Preserve applicable provenance and data-state metadata.
- Do not add external side effects unless explicitly required above.
- Apply household access and screen-safe policies before returning sensitive information.

## Definition of done

- Acceptance criteria have automated coverage where technically feasible.
- Relevant contract, architecture and operational documentation is updated.
- Error, unavailable and stale paths have been verified.
