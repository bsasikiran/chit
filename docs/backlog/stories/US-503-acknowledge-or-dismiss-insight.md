---
id: US-503
title: Acknowledge or dismiss insight
epic: EPIC-05
priority: should
status: ready
release: pilot-4
journey_touchpoints:
- IE1
- IE4
persona: Household Member
dependencies:
- US-501
architecture_refs:
- docs/architecture/security-privacy.md
components:
- insights
- dashboard-ui
---

# US-503: Acknowledge or dismiss insight

## User story

As a **Household Member**, I want to acknowledge or dismiss an attention card without triggering an external action, so that I remain in control while Chit learns which insights are useful.

## Acceptance criteria

### AC-1: Acknowledge

Given a visible card, when a member acknowledges it, then Chit records the local interaction without external side effects.

### AC-2: Dismiss

Given a visible card, when a member dismisses it, then it leaves the active view according to retention policy.

### AC-3: No external action

Given either interaction, then Chit does not message people, modify schedules or control devices.

## Product constraints

- Preserve applicable provenance and data-state metadata.
- Do not add external side effects unless explicitly required above.
- Apply household access and screen-safe policies before returning sensitive information.

## Definition of done

- Acceptance criteria have automated coverage where technically feasible.
- Relevant contract, architecture and operational documentation is updated.
- Error, unavailable and stale paths have been verified.
