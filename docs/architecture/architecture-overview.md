# Chit Technical Architecture

## 1. Architecture Decision

Chit will use a **cloud-and-edge-portable modular monolith**. The same domain model and API contracts will support:

- A managed cloud deployment for multi-tenant operation.
- An edge gateway for local processing with optional cloud synchronization.
- A standalone local appliance that continues to operate without internet access.

The first implementation will avoid premature microservices. The application will be split into clear modules and independently deployable boundaries, but will initially run as one web/API process plus an optional background worker. Services will be extracted only when scale, isolation, or operational requirements justify it.

The architecture must not make a hosted Next.js runtime, PostgreSQL, Redis, or continuous cloud connectivity mandatory for the core product path.

## 2. Deployment Profiles

### Cloud

- Multi-tenant application deployed on a managed cloud platform.
- Next.js frontend and TypeScript API.
- Managed PostgreSQL as the system of record.
- Managed object storage for exports, backups, and larger artifacts.
- Managed queue or worker platform for imports, calculations, notifications, and exports.
- OIDC/SAML-capable identity provider for enterprise authentication.

### Edge gateway

- Runs on an ARM64 or x86_64 Linux device such as a Raspberry Pi-class computer, industrial gateway, NAS, or mini-PC.
- Local API, SQLite database, background worker, and static frontend.
- Operates during network outages and synchronizes selected data when connectivity returns.
- Uses outbound HTTPS by default; MQTT is optional for telemetry or device-command requirements.
- Can be centrally monitored and updated when enrolled with the cloud control plane.

### Local appliance

- Runs entirely on a local Linux device.
- Uses SQLite and local authentication or an explicitly configured local identity mode.
- Does not require cloud services for core dashboard, configuration, calculations, or local data capture.
- Is packaged with Docker Compose for pilots and development; a managed appliance image or installer may be introduced for production hardware.

## 3. Technology Stack

| Layer | Decision | Notes |
|---|---|---|
| UI | React, Next.js, TypeScript | Use Next.js for the cloud UI; support static export and independent API access for local deployments. |
| Styling and components | Tailwind CSS and shadcn/ui | Accessible, consistent, and easy to theme for desktop and touchscreen layouts. |
| Client server-state | TanStack Query | Caching, retries, invalidation, background refresh, and offline-aware query behavior. |
| Client UI-state | Zustand | Filter drafts, layout, selected entities, and display preferences only. |
| Forms and validation | React Hook Form and Zod | Shared validation for forms, query parameters, and API payloads. |
| API | TypeScript with Fastify or Hono | REST endpoints with OpenAPI documentation. Keep the API independently deployable from the frontend. |
| Cloud database | PostgreSQL | Multi-tenant system of record and source for centralized reporting. |
| Local database | SQLite | Local appliance and edge persistence. Use Drizzle ORM and keep core migrations portable. |
| ORM and migrations | Drizzle ORM and Drizzle Kit | Explicit schema, type safety, and controlled migrations. |
| Cache and jobs | Managed Redis-compatible service or platform queue | Optional initially; use for rate limiting, idempotency, cache, and job coordination when required. |
| Charts | Apache ECharts | Primary charting library for time series, zooming, annotations, brushing, and dense datasets. |
| Lightweight charts | Recharts | KPI cards, sparklines, and simple low-volume charts only. |
| Tables | TanStack Table and TanStack Virtual | Server-side pagination, sorting, filtering, column management, and virtualization. |
| Packaging | Docker Compose, ARM64 and x86_64 images | Provide reproducible cloud, edge, and local development environments. |
| Local reverse proxy | Caddy or nginx | Local routing, static assets, and TLS where required. |
| Desktop companion | Tauri, optional | Use only if device provisioning, filesystem, USB, serial, or OS integration requires a native wrapper. |
| Observability | Sentry, structured logs, OpenTelemetry-compatible traces | Track frontend failures, API latency, sync failures, and database performance. |
| Testing | Vitest, React Testing Library, Playwright, and API contract tests | Cover domain logic, UI behavior, deployment-critical flows, and API compatibility. |

## 4. Application Boundaries

The codebase will use the following logical modules:

- Identity and authorization.
- Tenant, organization, and membership management.
- Dashboard views, widgets, layouts, and saved filters.
- Data sources, integration accounts, synchronization, and provider adapters.
- Domain entities, metric definitions, calculations, and data-quality status.
- Query and aggregation services for chart and table data.
- Export jobs and generated artifacts.
- Notifications and user preferences.
- Audit events, diagnostics, backups, and device management.

The domain layer must not call provider SDKs directly. Integration adapters translate external schemas into canonical domain records. This keeps cloud providers and device protocols replaceable.

## 5. API and Data Contracts

The API will use REST with OpenAPI documentation. Zod schemas may be used as the implementation source for runtime validation and contract generation.

Representative endpoints include:

- `GET /api/dashboard-views`
- `GET /api/dashboard-views/:id`
- `GET /api/widgets/:id/data`
- `GET /api/metrics/:id/series`
- `GET /api/data-sources`
- `POST /api/data-sources/:id/sync`
- `GET /api/sync-runs/:id`
- `POST /api/exports`
- `GET /api/exports/:id`
- `GET /api/audit-events`

Chart responses must contain normalized timestamps, values, units, series metadata, timezone, aggregation level, source freshness, synchronization status, and data-quality flags. The API must return an explicit error envelope with a machine-readable code, safe user message, correlation ID, and optional field-level validation details.

Long-running imports, recalculations, exports, and synchronization operations must return a job identifier. The client can poll job status or use server-sent events where progress visibility is valuable. Large result sets must use cursor pagination and server-side aggregation.

## 6. Persistence and Synchronization

PostgreSQL is the cloud system of record. SQLite is the local system of record for edge and appliance profiles. The core transactional schema and repository interfaces must remain portable between both databases.

Core entities include tenants, users, memberships, roles, dashboard views, widgets, layouts, saved filters, data sources, integration accounts, synchronization runs, synchronization errors, domain facts and dimensions, metric definitions, metric versions, metric results, audit events, export jobs, and device registrations.

All imported or calculated data must record source identifier, source timestamp, ingestion run, transformation or metric version, and data-quality status.

Synchronization must be explicit rather than implicit. Each device has a stable device identity and an outbound change or event log. Synchronization uses idempotency keys, checkpoints, retries with exponential backoff, and conflict policies defined per entity type.

- Configuration and reference data should use version checks or last-write-wins only where safe.
- Append-only measurements and audit events should use immutable event identifiers and deduplication.
- Destructive operations require explicit authorization and a tombstone or deletion record that can be synchronized.
- A device must show last successful sync, pending changes, failed changes, and data freshness.

The system must remain useful during an outage. Local reads, calculations, configuration changes, and permitted data capture should continue; cloud-only functions must be clearly marked as unavailable rather than silently failing.

## 7. Authentication and Authorization

- Use an OIDC/SAML-capable managed identity provider for cloud and enterprise deployments.
- Use short-lived sessions in secure, HTTP-only, same-site cookies; never store access tokens in `localStorage`.
- Enforce tenant and resource authorization in the API and repository/query layer, not only in the UI.
- Minimum roles are Viewer, Editor, and Administrator. Add resource-level permissions if teams, portfolios, or data domains require them.
- Local appliance mode must support a secure initial administrator setup, password or local identity configuration, session revocation, and recovery/reset procedures.
- Store integration credentials in a managed secret store in the cloud and encrypted local storage on devices. Never place secrets in source code, browser bundles, ordinary logs, or diagnostic exports.
- Keep an append-only audit log for authentication events, authorization changes, integrations, imports, exports, configuration changes, and destructive actions.
- Support data minimization, configurable retention, deletion/export workflows, and EU-region hosting where required.

## 8. State Management and UX Data States

- TanStack Query is the source of truth for server state.
- Zustand is restricted to client-only state such as layout, transient selections, filter drafts, and display preferences.
- URL query parameters are canonical for shareable dashboard filters and date ranges.
- Query keys must include tenant, resource, filters, date range, sort order, and pagination cursor.
- KPI and summary data should normally be refreshed every 30–120 seconds; historical chart data can be cached for 5–15 minutes unless the metric requires fresher data.
- Configuration, permissions, and completed mutations must invalidate affected queries immediately.
- Optimistic updates are permitted for low-risk preferences only. Data mutations and integration actions require pending states, idempotency keys, server confirmation, and query invalidation.
- The UI must distinguish loading, empty, stale, partial, unavailable, and failed data states.
- Every dashboard data response should expose `lastUpdatedAt`, `sourceStatus`, `syncRunId`, and quality indicators.

## 9. Performance Requirements

Initial service-level objectives are measured at the API edge at p50, p95, and p99:

| Operation | Target | Maximum before degraded handling |
|---|---:|---:|
| Health and authenticated-session check | p95 <= 100 ms | 300 ms |
| Indexed KPI or small read | p95 <= 300 ms | 750 ms |
| Standard dashboard load, excluding browser rendering | p95 <= 750 ms | 1.5 s |
| Filter or date-range interaction | p95 <= 500 ms | 1 s |
| Paginated table query | p95 <= 750 ms | 2 s |
| Mutation or configuration save | p95 <= 500 ms | 1.5 s |
| Integration status lookup | p95 <= 1 s | 3 s |
| Export initiation | p95 <= 1 s to return a job ID | Never generate large exports synchronously |

Additional requirements:

- Define request, database statement, and external-provider timeouts.
- Use connection pooling, payload limits, pagination limits, and compressed responses.
- Enforce maximum synchronous query windows and aggregation limits.
- Use rollup tables or materialized views for expensive time-series queries.
- Downsample chart data and virtualize large tables.
- Track latency by route, tenant, query shape, provider, result size, and cache status.
- For edge devices, define a degraded-performance profile based on the minimum supported CPU, RAM, storage, and network conditions.

## 10. Hardware and Portability Requirements

- Support ARM64 and x86_64 for all production images where technically feasible.
- Define and test a minimum hardware profile before pilot production: CPU, RAM, persistent storage, network, optional display, and supported peripherals.
- Prefer eMMC, SSD, or industrial flash for always-on devices; treat consumer microSD as development or low-duty-cycle storage only.
- Keep application data, configuration, cache, logs, and temporary files in separate locations.
- Assume the root filesystem may be read-only or may fail; provide recovery, backup, restore, and factory-reset procedures.
- Provide local health, diagnostics, version, storage, sync, and connectivity status views.
- Use signed, versioned updates with health checks and rollback. Devices must not be left unusable after a failed update.
- Define a secure provisioning flow, unique device identity, credential rotation, and device decommissioning process.
- Ensure the UI works on desktop browsers and small touchscreens. Do not make hover, large screens, or high-bandwidth connectivity mandatory.
- Keep all device-specific integrations behind interfaces for GPIO, serial, USB, camera, sensor, and network protocols.

## 11. Security and Reliability

- Encrypt traffic in transit and sensitive data at rest.
- Apply least privilege to users, services, integrations, and device credentials.
- Use dependency scanning, secret scanning, image scanning, and signed release artifacts in CI/CD.
- Apply rate limits to authentication, synchronization, exports, and externally exposed APIs.
- Use retries with exponential backoff, circuit breakers, dead-letter handling, and idempotency for external integrations.
- Make backups encrypted, tested, versioned, and restorable to a replacement device or tenant.
- Define retention limits for raw data, audit events, logs, exports, and diagnostic bundles.
- Redact secrets and personal data from logs and error reports.
- Test tenant isolation, offline behavior, failed synchronization, interrupted updates, power loss, storage exhaustion, clock drift, and recovery from backup.

## 12. Main Risks and Mitigations

- **Metric ambiguity:** Version metric definitions, units, timezones, aggregation rules, and source lineage.
- **Slow analytical queries:** Enforce query limits, inspect query plans, add rollups, and move heavy work to jobs.
- **Integration instability:** Isolate provider adapters and use retries, rate-limit handling, circuit breakers, and freshness indicators.
- **Data leakage between tenants:** Apply tenant predicates centrally, consider PostgreSQL row-level security, and run cross-tenant authorization tests.
- **Synchronization conflicts:** Define per-entity conflict policies and make append-only events immutable and deduplicated.
- **Device storage failure:** Use durable storage, health monitoring, encrypted backups, and a replacement-device restore flow.
- **Update failure:** Use signed artifacts, staged rollout, health checks, and rollback partitions or previous images.
- **Browser and chart performance:** Aggregate server-side, downsample time series, virtualize tables, lazy-load widgets, and use Canvas rendering for dense ECharts views.
- **Cost growth:** Keep provider adapters replaceable, use PostgreSQL-compatible designs, monitor usage, and make Redis and warehouse services optional until justified.
- **Operational coupling:** Run ingestion, exports, and recalculation in workers rather than blocking API processes.
- **Overpromised real time:** Define freshness per metric and use scheduled ingestion or polling by default; reserve SSE/WebSockets for validated requirements.

## 13. Delivery Sequence

1. Implement tenant, identity, authorization, audit, metric-definition, freshness, and device-identity foundations.
2. Deliver one vertical slice: authenticated dashboard, representative data source, KPI, time-series chart, paginated table, local persistence, and export job.
3. Run the slice in cloud PostgreSQL and local SQLite using the same domain tests and API contract tests.
4. Package ARM64 and x86_64 images and test offline operation, restart, backup/restore, storage exhaustion, and synchronization recovery.
5. Measure actual query shapes, payload sizes, device resource consumption, and integration failure behavior.
6. Add rollups, Redis, managed queues, fleet management, or service extraction only when measured requirements justify them.

## 14. Explicit Non-Goals

- No microservices decomposition before workload or team boundaries require it.
- No mandatory cloud connection for core local dashboard operation.
- No browser-side downloading of entire fact tables for chart calculations.
- No native Tauri wrapper unless browser packaging or hardware integration requires it.
- No custom hardware design before the product workflow, data model, device interfaces, and update/recovery requirements are validated.
