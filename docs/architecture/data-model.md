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

## Persistence and access boundary

Chit's Chit-owned structured records use SQLite on the household-controlled host, with encryption at rest required. The encryption mechanism and key lifecycle must be selected before implementation. Browser clients access persisted data through the application/API boundary, not by opening the database file.

Subscribed calendar events remain authoritative at their external source and are not durably mirrored by default. Persist source configuration, household mappings and Chit-owned derived records; any event cache must have an explicit need and bounded retention. The storage decision is recorded in [ADR-0004](adr/0004-sqlite-encrypted-local-storage.md).

This persistence decision does not define application authentication, authorization or member-level access management. Those remain separate design work.

The initial relational structure separates household and member profiles from optional adult work patterns, child care days, child activity recurrence, calendar-source/member mappings, chore-generation rules and chores/assignees. Household ownership references one adult member. Calendar-source access is read-only. Generated chores retain their source occurrence and rule references so repeated refreshes can be idempotent; completed or manually modified chores are not overwritten by a source refresh.

The initial schema is versioned through SQL migrations under `server/chit_store/migrations/`. It deliberately has no general-purpose subscribed-event table. Database access is currently a Python repository module, not yet an HTTP API or application access-control implementation.

## Detailed contract

The draft machine-readable definition is `docs/specifications/domain-model.yaml`.
