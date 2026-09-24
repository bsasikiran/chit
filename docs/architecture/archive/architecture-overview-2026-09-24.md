# Architecture Overview

## Purpose

Chit is designed as a modular, scalable web application with a clear separation between the presentation layer, application services, data persistence, and external integrations. The architecture supports a browser-based user experience, dashboard-style visualisation, background processing, and integration with external data sources.

## High-Level Architecture

```text
+-------------------+
|   Browser / UI    |
|  Dashboard Client |
+---------+---------+
          |
          v
+-------------------+
|   API / Services   |
| Auth, Queries,     |
| Commands, Jobs     |
+----+----------+---+
     |          |
     v          v
+---------+  +----------------+
|Database |  | Integrations   |
|         |  | External APIs  |
+---------+  +----------------+
```

## Architectural Principles

1. **Modular monolith first**: Start with a well-structured modular monolith. Split services only when there is a clear scaling, ownership, or reliability benefit.
2. **API-first design**: The frontend communicates with backend capabilities through a versioned API boundary.
3. **Separation of concerns**: UI, application logic, persistence, and external integrations should remain independently testable.
4. **Secure by default**: Authentication, authorization, validation, auditability, and data minimisation are architectural requirements.
5. **Observable operations**: Important user actions, integration runs, failures, and data freshness should be observable.
6. **Incremental complexity**: Prefer the simplest architecture that satisfies the current product needs.

## Frontend

The frontend is a browser-based dashboard application responsible for:

- Authentication and user session handling.
- Navigation and dashboard composition.
- Filters, date ranges, and saved views.
- Charts, tables, status indicators, and drill-down experiences.
- Form input and configuration workflows.
- Loading, empty, stale, partial, and error states.

The frontend should be structured into reusable components and feature modules. Data fetching and server state should be separated from local UI state. Charts should receive normalised, presentation-ready data rather than raw integration payloads.

## Backend / API Layer

The backend provides:

- Authentication and session integration.
- Tenant, user, and role authorisation.
- Dashboard and widget configuration.
- Query and aggregation services.
- Data ingestion and integration adapters.
- Background jobs for synchronisation, calculations, exports, and notifications.
- Audit events and operational diagnostics.

The API should validate input at its boundary, enforce tenant scope, apply pagination and query limits, and return consistent error structures. Long-running work should be asynchronous and expose job status.

## Data Layer

The primary data store is a relational database. The model should support:

- Users, organisations, memberships, and roles.
- Dashboard views, widgets, layouts, and saved filters.
- Data sources and integration configurations.
- Raw or normalised observations and measurements.
- Metric definitions and calculated results.
- Synchronisation runs and data-quality information.
- Audit events, exports, and notifications.

The data model should preserve source identifiers, timestamps, ingestion metadata, and provenance. Expensive analytical queries should use indexes, pre-aggregated tables, or materialised views where appropriate.

## Integrations

External integrations should be implemented through provider adapters. An adapter is responsible for:

- Authentication with the provider.
- Pagination and rate-limit handling.
- Schema mapping into canonical internal models.
- Retry and failure behaviour.
- Source freshness and synchronisation status.

Provider-specific details should not leak into the core domain model. Integration credentials must be stored securely and never exposed to the browser.

## Background Processing

Background processing should handle:

- Initial and incremental data synchronisation.
- Metric calculation and rollups.
- Scheduled refreshes.
- Export generation.
- Notifications.
- Cleanup and retention tasks.

Jobs should be idempotent, retryable, observable, and safe to resume after failure. Job status should be visible to users when the result affects a dashboard or configuration workflow.

## Security and Privacy

The system should implement:

- Strong authentication and session management.
- Role-based and resource-level authorisation.
- Tenant isolation.
- Input validation and output filtering.
- Encryption in transit and at rest.
- Secret management for integration credentials.
- Audit logging for security-sensitive and data-changing actions.
- Data retention, deletion, and export capabilities.
- Privacy-aware logging and diagnostics.

## Observability

The application should provide:

- Structured application logs.
- Error tracking for frontend and backend failures.
- Metrics for API latency, job duration, integration failures, and data freshness.
- Correlation IDs across browser requests, API calls, and background jobs.
- Health and readiness checks.
- Operational dashboards and alerting for critical failures.

## Scalability and Performance

The initial system should be optimised for simplicity and predictable performance. Requirements include:

- Pagination for tables and large result sets.
- Server-side filtering and aggregation.
- Caching for stable or expensive queries.
- Asynchronous processing for long-running operations.
- Database indexes based on actual query patterns.
- Protection against unbounded queries and payloads.
- Progressive loading and virtualisation for dense dashboards.

## Deployment

The application should support:

- Local development with reproducible configuration.
- Automated testing and continuous integration.
- Separate staging and production environments.
- Managed deployment of the frontend, API, database, and workers.
- Environment-specific secrets and configuration.
- Repeatable migrations and rollback procedures.

## Architectural Evolution

The architecture should evolve through measured evidence. Potential future additions include:

- Dedicated worker services.
- Distributed caching.
- Read replicas or analytical storage.
- Event-driven integration processing.
- Service decomposition by bounded context.
- Advanced notification and workflow capabilities.

These additions should be introduced only when justified by product usage, operational requirements, or team structure.
