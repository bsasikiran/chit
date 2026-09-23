---
id: US-303
title: Local deployment and access control
epic: EPIC-03
priority: must
status: ready
release: pilot-1
journey_touchpoints:
- D3
- FL1
persona: Privacy-Conscious Household Administrator
dependencies: []
architecture_refs:
- docs/architecture/security-privacy.md
components:
- deployment
- identity
---

# US-303: Local deployment and access control

## User story

As a **Privacy-Conscious Household Administrator**, I want to deploy Chit locally and restrict access to authorised users, so that household data remains under my control.

## Acceptance criteria

### AC-1: Local operation

Given supported local infrastructure, then core pilot services can run without sending household data to an unapproved cloud processor.

### AC-2: Authentication

Given a protected administration route, then unauthenticated users cannot access it.

### AC-3: Authorisation

Given a signed-in member, then protected operations enforce the assigned household role.

## Product constraints

- Preserve applicable provenance and data-state metadata.
- Do not add external side effects unless explicitly required above.
- Apply household access and screen-safe policies before returning sensitive information.

## Definition of done

- Acceptance criteria have automated coverage where technically feasible.
- Relevant contract, architecture and operational documentation is updated.
- Error, unavailable and stale paths have been verified.
