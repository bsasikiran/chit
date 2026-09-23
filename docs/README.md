# Chit Documentation

This directory is the version-controlled source of truth for product intent, delivery scope, architecture and implementation contracts.

## Reading paths

### Product owner

1. `product/product-vision.md`
2. `product/personas.md`
3. `product/customer-journey.md`
4. `backlog/backlog.yaml`
5. Individual files under `backlog/stories/`

### Solution architect

1. `architecture/architecture-overview.md`
2. `architecture/data-model.md`
3. `architecture/integrations.md`
4. `architecture/security-privacy.md`
5. `architecture/adr/`
6. `specifications/`

### Agentic developer

1. Repository-level `AGENTS.md`
2. Assigned story file and its dependencies
3. Referenced ADRs and architecture documents
4. Machine-readable contracts under `specifications/`
5. `releases/pilot-scope.md`

## Status vocabulary

- `draft`: incomplete or awaiting review
- `ready`: approved and implementable
- `in-progress`: actively being implemented
- `blocked`: cannot proceed because of a documented dependency
- `done`: acceptance criteria verified
- `deferred`: intentionally outside the active release

## Change policy

Product behaviour changes begin in a story. Contract changes update a specification. Significant architectural choices create a new ADR. Supersede accepted ADRs rather than rewriting their decision history.
