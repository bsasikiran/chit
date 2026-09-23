---
id: US-101
title: Consistent household data model
epic: EPIC-01
priority: must
status: ready
release: pilot-1
journey_touchpoints:
- FL3
- DU1
- DU2
persona: Household Coordinator
dependencies: []
architecture_refs:
- docs/architecture/data-model.md
components:
- normalization
- storage
---

# US-101: Consistent household data model

## User story

As a **Household Coordinator**, I want events, tasks, people, devices and energy information presented through a consistent household model, so that I can understand information from different services without interpreting each service separately.

## Acceptance criteria

### AC-1: Normalized entity

Given a supported connector returns data, when Chit ingests it, then it maps the record to the applicable person, event, task, device or energy schema.

### AC-2: Required metadata

Given a normalized record is stored, then it includes household, source, availability and time metadata required by the domain specification.

### AC-3: Invalid record

Given required fields cannot be mapped, then Chit rejects or quarantines the record and exposes a diagnosable error.

## Product constraints

- Preserve applicable provenance and data-state metadata.
- Do not add external side effects unless explicitly required above.
- Apply household access and screen-safe policies before returning sensitive information.

## Definition of done

- Acceptance criteria have automated coverage where technically feasible.
- Relevant contract, architecture and operational documentation is updated.
- Error, unavailable and stale paths have been verified.
