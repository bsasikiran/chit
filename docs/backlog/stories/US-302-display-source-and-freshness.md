---
id: US-302
title: Display source and freshness
epic: EPIC-03
priority: must
status: ready
release: pilot-1
journey_touchpoints:
- FL3
- DU5
- IE2
persona: Household Member
dependencies:
- US-102
- US-301
architecture_refs:
- docs/architecture/data-model.md
components:
- dashboard-api
- dashboard-ui
---

# US-302: Display source and freshness

## User story

As a **Household Member**, I want to see the source and last-updated time for dashboard information, so that I can detect stale or unreliable data.

## Acceptance criteria

### AC-1: Source displayed

Given a dashboard value has a source, then the source name is visible or accessible.

### AC-2: Freshness displayed

Given a record has ingestion metadata, then the last-updated time is displayed in a comprehensible form.

### AC-3: Stale status

Given the freshness threshold is exceeded, then the value is visibly stale and does not appear current.

## Product constraints

- Preserve applicable provenance and data-state metadata.
- Do not add external side effects unless explicitly required above.
- Apply household access and screen-safe policies before returning sensitive information.

## Definition of done

- Acceptance criteria have automated coverage where technically feasible.
- Relevant contract, architecture and operational documentation is updated.
- Error, unavailable and stale paths have been verified.
