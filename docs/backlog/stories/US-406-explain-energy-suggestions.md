---
id: US-406
title: Explain energy suggestions
epic: EPIC-04
priority: should
status: ready
release: pilot-3
journey_touchpoints:
- IE2
- IE3
persona: Household Member
dependencies:
- US-405
architecture_refs:
- docs/architecture/data-model.md
components:
- insights
- dashboard-ui
---

# US-406: Explain energy suggestions

## User story

As a **Household Member**, I want every energy suggestion to explain which prices, forecasts and schedules were considered, so that I can verify the recommendation before acting.

## Acceptance criteria

### AC-1: Reason shown

Given a suggestion exists, then it includes a plain-language reason.

### AC-2: Evidence shown

Given a user opens details, then supporting sources, values, data states and freshness are visible.

### AC-3: Limitations shown

Given relevant data is estimated, stale or unavailable, then the explanation states that limitation.

## Product constraints

- Preserve applicable provenance and data-state metadata.
- Do not add external side effects unless explicitly required above.
- Apply household access and screen-safe policies before returning sensitive information.

## Definition of done

- Acceptance criteria have automated coverage where technically feasible.
- Relevant contract, architecture and operational documentation is updated.
- Error, unavailable and stale paths have been verified.
