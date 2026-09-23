---
id: US-402
title: Separate solar forecast and actuals
epic: EPIC-04
priority: must
status: ready
release: pilot-3
journey_touchpoints:
- DU5
- IE3
persona: Energy-Aware Homeowner
dependencies:
- US-301
architecture_refs:
- docs/architecture/data-model.md
- docs/architecture/integrations.md
components:
- energy
- dashboard-ui
---

# US-402: Separate solar forecast and actuals

## User story

As a **Energy-Aware Homeowner**, I want public solar estimates displayed separately from actual inverter output, so that I do not confuse forecast production with measured generation.

## Acceptance criteria

### AC-1: Separate series

Given forecast and inverter data both exist, then they render as separately labelled series or values.

### AC-2: State labels

Given solar forecast appears, it is labelled forecast; given inverter output appears, it is labelled measured.

### AC-3: Independent freshness

Given the sources update at different times, then each displays its own freshness.

## Product constraints

- Preserve applicable provenance and data-state metadata.
- Do not add external side effects unless explicitly required above.
- Apply household access and screen-safe policies before returning sensitive information.

## Definition of done

- Acceptance criteria have automated coverage where technically feasible.
- Relevant contract, architecture and operational documentation is updated.
- Error, unavailable and stale paths have been verified.
