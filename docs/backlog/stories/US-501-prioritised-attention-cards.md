---
id: US-501
title: Prioritised attention cards
epic: EPIC-05
priority: should
status: ready
release: pilot-4
journey_touchpoints:
- IE1
persona: Household Coordinator
dependencies:
- US-302
architecture_refs:
- docs/architecture/architecture-overview.md
components:
- insights
- dashboard-ui
---

# US-501: Prioritised attention cards

## User story

As a **Household Coordinator**, I want a small number of prioritised needs-attention cards, so that I can focus on the most relevant household issues without being overwhelmed.

## Acceptance criteria

### AC-1: Bounded list

Given several candidate issues, then the dashboard shows no more than the configured attention-card limit.

### AC-2: Deterministic priority

Given candidates compete for display, then documented severity, urgency and confidence rules determine order.

### AC-3: No unsupported card

Given evidence is insufficient, then Chit does not present the candidate as an attention item.

## Product constraints

- Preserve applicable provenance and data-state metadata.
- Do not add external side effects unless explicitly required above.
- Apply household access and screen-safe policies before returning sensitive information.

## Definition of done

- Acceptance criteria have automated coverage where technically feasible.
- Relevant contract, architecture and operational documentation is updated.
- Error, unavailable and stale paths have been verified.
