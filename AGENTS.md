# Chit Agent Instructions

## Product intent

Chit is a trustworthy, read-only household overview before it is an autonomous assistant. Do not introduce messaging, schedule changes, appliance control or other external side effects unless an approved story explicitly requires them.

## Sources of truth

Use this precedence when documents disagree:

1. Approved story and acceptance criteria in `docs/backlog/stories/`
2. Current pilot scope in `docs/releases/pilot-scope.md`
3. Product principles in `docs/product/product-vision.md`
4. Accepted decisions in `docs/architecture/adr/`
5. Architecture documents in `docs/architecture/`
6. Machine-readable contracts in `docs/specifications/`
7. Directional research in `docs/product/market-synthesis.md`

Do not treat archived dashboard prototypes as current requirements.

## Before coding

- Identify one or more story IDs and read their dependencies and architecture references.
- Confirm that acceptance criteria are unambiguous and testable.
- Check relevant ADRs and specifications.
- Ask for clarification instead of inventing product behaviour.
- Propose a new ADR when a change affects deployment, data ownership, privacy, integration boundaries or major technology choices.

## Non-negotiable rules

- Preserve source, observed time, ingestion time, availability and data state for normalized records.
- Use only the states defined in `docs/specifications/data-states.yaml`.
- Treat missing information as `unavailable` or `unknown`; never infer availability from absence.
- Never label forecast, manual or demo values as measured.
- Keep pilot device integrations read-only.
- Apply screen-safe presentation before returning shared-display data.
- Minimise data collection and enforce explicit permissions for sensitive domains.

## Definition of done

- All story acceptance criteria are implemented and covered by tests.
- Linting, type checks and automated tests pass.
- API/schema changes update the corresponding specification.
- Architectural changes update documentation and, when significant, add an ADR.
- The pull request lists story IDs, files changed, checks run, residual risks and deferred work.
