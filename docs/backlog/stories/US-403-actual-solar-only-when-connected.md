---
id: US-403
title: Actual solar only when connected
epic: EPIC-04
priority: must
status: ready
release: pilot-3
journey_touchpoints:
- FL3
- DU5
- IE3
persona: Energy-Aware Homeowner
dependencies:
- US-104
- US-402
architecture_refs:
- docs/architecture/integrations.md
components:
- energy
- dashboard-api
---

# US-403: Actual solar only when connected

## User story

As a **Energy-Aware Homeowner**, I want actual solar generation shown only when an inverter is connected, so that the dashboard never presents estimated data as a live measurement.

## Acceptance criteria

### AC-1: Connected measurement

Given an authorised inverter source is healthy, then its observed output may be shown as measured.

### AC-2: No inverter

Given no inverter source exists, then actual generation is unavailable and forecast remains separately visible.

### AC-3: Lost connection

Given the inverter becomes unreachable, then the last measurement becomes stale and is not presented as live.

## Product constraints

- Preserve applicable provenance and data-state metadata.
- Do not add external side effects unless explicitly required above.
- Apply household access and screen-safe policies before returning sensitive information.

## Definition of done

- Acceptance criteria have automated coverage where technically feasible.
- Relevant contract, architecture and operational documentation is updated.
- Error, unavailable and stale paths have been verified.
