# ADR-0003: Preserve provenance in every normalized record

- Status: Accepted
- Date: 2026-09-23

## Context

Users must distinguish measured, forecast, manual, unavailable and demo information and identify stale sources.

## Decision

Every normalized record carries source, data state, availability, observed time when supplied, ingestion time and schema version.

## Consequences

Connectors have additional mapping work, but dashboard and insight services can provide consistent trust cues.

## Supersession

If this decision changes, add a new ADR that identifies this record as superseded. Do not rewrite the accepted decision history.
