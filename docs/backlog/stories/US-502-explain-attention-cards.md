---
id: US-502
title: Explain attention cards
epic: EPIC-05
priority: should
status: ready
release: pilot-4
journey_touchpoints:
- IE1
- IE2
persona: Household Member
dependencies:
- US-501
architecture_refs:
- docs/architecture/data-model.md
components:
- insights
- dashboard-ui
---

# US-502: Explain attention cards

## User story

As a **Household Member**, I want each attention card to show why it appeared and which source supports it, so that I can decide whether the issue requires action.

## Acceptance criteria

### AC-1: Reason

Given an attention card appears, then it provides a concise reason.

### AC-2: Source

Given card details are opened, then source, last update and relevant records are accessible.

### AC-3: Uncertainty

Given supporting information is forecast or stale, then the card visibly communicates uncertainty.

## Product constraints

- Preserve applicable provenance and data-state metadata.
- Do not add external side effects unless explicitly required above.
- Apply household access and screen-safe policies before returning sensitive information.

## Definition of done

- Acceptance criteria have automated coverage where technically feasible.
- Relevant contract, architecture and operational documentation is updated.
- Error, unavailable and stale paths have been verified.
