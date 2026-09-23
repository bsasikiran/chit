---
id: US-301
title: Explicit data-state labels
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
- US-101
architecture_refs:
- docs/architecture/data-model.md
components:
- dashboard-api
- dashboard-ui
---

# US-301: Explicit data-state labels

## User story

As a **Household Member**, I want values labelled as measured, forecast, manually entered, unavailable or demonstration data, so that I understand what each value represents.

## Acceptance criteria

### AC-1: Allowed states

Given a value is returned to the dashboard, then it uses exactly one approved data state.

### AC-2: Visible distinction

Given values with different states appear together, then text or icon labels distinguish them without relying only on colour.

### AC-3: No promotion

Given forecast or demo data exists, then it cannot be transformed or displayed as measured data.

## Product constraints

- Preserve applicable provenance and data-state metadata.
- Do not add external side effects unless explicitly required above.
- Apply household access and screen-safe policies before returning sensitive information.

## Definition of done

- Acceptance criteria have automated coverage where technically feasible.
- Relevant contract, architecture and operational documentation is updated.
- Error, unavailable and stale paths have been verified.
