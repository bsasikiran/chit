---
id: US-102
title: Preserve provenance and freshness
epic: EPIC-01
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
- normalization
- storage
---

# US-102: Preserve provenance and freshness

## User story

As a **Household Member**, I want every item to retain its source, update time and availability status, so that I can judge whether the information is current and trustworthy.

## Acceptance criteria

### AC-1: Provenance retained

Given an item is ingested, then source ID, source type, observed time and ingested time are retained.

### AC-2: Freshness calculable

Given a source has a configured freshness threshold, when an item is read, then its current or stale state can be determined.

### AC-3: Unknown metadata

Given a provider omits an observation time, then the field is unknown and Chit does not substitute the ingestion time as if observed.

## Product constraints

- Preserve applicable provenance and data-state metadata.
- Do not add external side effects unless explicitly required above.
- Apply household access and screen-safe policies before returning sensitive information.

## Definition of done

- Acceptance criteria have automated coverage where technically feasible.
- Relevant contract, architecture and operational documentation is updated.
- Error, unavailable and stale paths have been verified.
