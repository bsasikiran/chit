---
id: US-404
title: Read-only appliance information
epic: EPIC-04
priority: must
status: ready
release: pilot-2
journey_touchpoints:
- DU4
- IE4
persona: Household Member
dependencies:
- US-104
architecture_refs:
- docs/architecture/security-privacy.md
- docs/architecture/integrations.md
components:
- home-assistant
- dashboard-ui
---

# US-404: Read-only appliance information

## User story

As a **Household Member**, I want appliance information to remain read-only during the pilot, so that I retain control over device changes while evaluating Chit’s reliability.

## Acceptance criteria

### AC-1: No command path

Given the pilot deployment, then application credentials and APIs do not permit appliance control.

### AC-2: No misleading controls

Given an appliance card renders, then it contains no UI that implies a command can be sent.

### AC-3: Audit check

Given a pilot build is verified, then an integration test confirms no device-control service is called.

## Product constraints

- Preserve applicable provenance and data-state metadata.
- Do not add external side effects unless explicitly required above.
- Apply household access and screen-safe policies before returning sensitive information.

## Definition of done

- Acceptance criteria have automated coverage where technically feasible.
- Relevant contract, architecture and operational documentation is updated.
- Error, unavailable and stale paths have been verified.
