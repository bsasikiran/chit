---
id: US-106
title: Extensible connector framework
epic: EPIC-01
priority: should
status: ready
release: pilot-1
journey_touchpoints:
- D2
- FL2
persona: Household Administrator
dependencies:
- US-101
- US-102
architecture_refs:
- docs/architecture/integrations.md
components:
- connectors
---

# US-106: Extensible connector framework

## User story

As a **Household Administrator**, I want to add supported school, appliance, inverter and tariff sources over time, so that Chit can grow with my household without a redesign.

## Acceptance criteria

### AC-1: Connector contract

Given a new provider, then it can implement authentication, retrieval, normalization, health and freshness interfaces without modifying domain consumers.

### AC-2: Capability declaration

Given a connector is installed, then it declares supported entity types and permissions.

### AC-3: Contract tests

Given a connector implementation, then automated contract tests verify required metadata and failure behaviour.

## Product constraints

- Preserve applicable provenance and data-state metadata.
- Do not add external side effects unless explicitly required above.
- Apply household access and screen-safe policies before returning sensitive information.

## Definition of done

- Acceptance criteria have automated coverage where technically feasible.
- Relevant contract, architecture and operational documentation is updated.
- Error, unavailable and stale paths have been verified.
