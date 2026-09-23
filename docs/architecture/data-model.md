# Data Model

## Purpose

The normalized model lets dashboard and insight components consume household information without depending on provider-specific payloads. Every record carries provenance, timing, availability and data-state metadata.

## Core entities

| Entity | Purpose | Key relationships |
|---|---|---|
| Household | Tenant and policy boundary | Contains members, sources and displays |
| Person | Household participant | Owns permissions, calendars and tasks |
| Event | Time-bound commitment | References people and a calendar source |
| Task | Chore or responsibility | May reference an assignee and due time |
| Device | Read-only connected equipment | References Home Assistant or another source |
| EnergyReading | Power or energy observation/forecast | References source, period and unit |
| TariffPeriod | Electricity price for a time window | References tariff source and currency/unit |
| Insight | Explainable attention or energy item | References supporting records |

## Record envelope

All normalized records must include:

- `id`, `householdId` and `entityType`
- `source.id`, `source.type` and optional provider reference
- `dataState`: `measured`, `forecast`, `manual`, `unavailable` or `demo`
- `availability.status` and optional reason
- `observedAt` when supplied by the source
- `ingestedAt` assigned by Chit
- schema version

## Time semantics

`observedAt` describes when the underlying fact occurred. `ingestedAt` describes when Chit received it. They must not be substituted for one another. Event start/end times are domain fields and do not replace provenance times.

## Freshness

Freshness is evaluated using source-specific policy. A stale record may remain visible for context but must not appear live. If freshness cannot be determined, it is unknown.

## Detailed contract

The draft machine-readable definition is `docs/specifications/domain-model.yaml`.
