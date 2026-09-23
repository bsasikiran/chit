---
id: US-305
title: Per-person sensitive permissions
epic: EPIC-03
priority: should
status: ready
release: pilot-2
journey_touchpoints:
- FL1
- FL4
persona: Privacy-Conscious Member
dependencies:
- US-303
architecture_refs:
- docs/architecture/security-privacy.md
components:
- identity
- policy
---

# US-305: Per-person sensitive permissions

## User story

As a **Privacy-Conscious Member**, I want to control which sensitive information other household members can access, so that personal details such as health information remain private.

## Acceptance criteria

### AC-1: Explicit consent

Given sensitive data is connected, then access is denied until the person grants an explicit permission.

### AC-2: Granular policy

Given permission is granted, then it identifies recipient role, data category and allowed presentation context.

### AC-3: Revocation

Given a person revokes permission, then subsequent reads are denied and cached shared-display content is invalidated.

## Product constraints

- Preserve applicable provenance and data-state metadata.
- Do not add external side effects unless explicitly required above.
- Apply household access and screen-safe policies before returning sensitive information.

## Definition of done

- Acceptance criteria have automated coverage where technically feasible.
- Relevant contract, architecture and operational documentation is updated.
- Error, unavailable and stale paths have been verified.
