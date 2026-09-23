# Integration Architecture

## Connector contract

Each connector implements five concerns:

1. Authentication and secret references
2. Capability declaration
3. Retrieval or subscription
4. Mapping to normalized entities
5. Health, error and freshness reporting

Provider payloads must not leak into dashboard components. Connector contract tests verify required provenance and graceful failure.

## Pilot integrations

| Integration | Requirement | Access mode | Failure behaviour |
|---|---|---|---|
| Calendar | At least one real provider | Read-only | Events unavailable; no inferred availability |
| Weather | At least one provider/location | Read-only | Weather card unavailable or stale |
| Home Assistant | Optional | Read-only token and entity allowlist | Home/device cards degrade independently |
| Solar inverter | Optional through connector or Home Assistant | Read-only | Actual production unavailable; forecasts remain distinct |
| Dynamic tariff | Optional for energy suggestions | Read-only | No complete price-based suggestion without evidence |

## Secrets

Store secret values outside source control. Configuration may contain environment-variable or secret-store references, but never tokens, passwords or private keys.

## Side-effect boundary

Pilot connectors must not expose command execution to application services. Any future write capability requires a separate ADR, least-privilege credentials, explicit confirmation and auditable commands.
