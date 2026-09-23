---
id: US-405
title: Read-only energy suggestions
epic: EPIC-04
priority: should
status: ready
release: pilot-3
journey_touchpoints:
- IE3
- IE4
persona: Energy-Aware Homeowner
dependencies:
- US-402
- US-403
architecture_refs:
- docs/architecture/data-model.md
components:
- insights
- energy
---

# US-405: Read-only energy suggestions

## User story

As a **Energy-Aware Homeowner**, I want Chit to combine available electricity prices, solar forecasts and household schedules into a read-only suggestion, so that I can choose a more suitable time for flexible energy use.

## Acceptance criteria

### AC-1: Evidence threshold

Given required price, forecast and schedule inputs are available and fresh enough, then Chit may produce a suggested time window.

### AC-2: Incomplete evidence

Given required input is missing, then Chit identifies the gap and does not present a fully supported suggestion.

### AC-3: Read-only

Given a suggestion is displayed, then accepting or viewing it does not schedule or control an appliance.

## Product constraints

- Preserve applicable provenance and data-state metadata.
- Do not add external side effects unless explicitly required above.
- Apply household access and screen-safe policies before returning sensitive information.

## Definition of done

- Acceptance criteria have automated coverage where technically feasible.
- Relevant contract, architecture and operational documentation is updated.
- Error, unavailable and stale paths have been verified.
