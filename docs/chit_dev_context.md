# Chit-Dev — Codebase Context

> **Purpose of this document:** Quick-start reference for working in this repo with Antigravity. Read this before touching any code.

---

## What Chit Is

Chit is a **read-only household dashboard** — a trustworthy at-a-glance overview displayed on a TV (via Raspberry Pi in kiosk mode). It surfaces weather, calendar events, family presence, appliance state, solar/energy context, and attention cards. It is **not** an autonomous agent; it does not send messages, control devices, or modify schedules in the pilot.

---

## Source-of-Truth Hierarchy

When documents disagree, this order wins:

1. `docs/backlog/stories/` — approved story + acceptance criteria
2. `docs/releases/pilot-scope.md` — current pilot boundary
3. `docs/product/product-vision.md` — product principles
4. `docs/architecture/adr/` — accepted architectural decisions
5. `docs/architecture/` — architecture docs
6. `docs/specifications/` — machine-readable contracts
7. `docs/product/market-synthesis.md` — directional research

---

## Repository Layout

```
chit-dev/
├── dashboard/          HTML pages (served by local Python server)
│   ├── ux_home.html           TV dashboard (weather, calendar, energy, family)
│   ├── household-setup.html   Owner setup wizard (largest file, 49 KB)
│   ├── calendar-home.html     Calendar-focused view
│   └── login.html             Single-owner login page
├── js/                Vanilla JS modules (ES modules, no build step)
│   ├── main.js        Entrypoint — wires all modules together
│   ├── config.js      Runtime config (home name, Tibber token, lat/lon, calendar)
│   ├── tibber.js      Tibber GraphQL → energy card renderer
│   ├── weather.js     Open-Meteo → weather card renderer
│   └── calendar.js   Stub; shows unavailable state until source configured
├── server/            Python local server (stdlib only + 3 deps)
│   ├── run.py         ThreadingHTTPServer — routes, auth, calendar API
│   ├── bootstrap_owner.py  One-time owner account setup script
│   └── chit_store/
│       ├── store.py   EncryptedHouseholdStore — all SQLite access (SQLCipher)
│       ├── auth.py    OwnerAuth — Argon2id + session + CSRF
│       └── migrations/ SQL migration files (001, 002, 003)
├── docs/              All product, architecture and spec docs
│   ├── architecture/  Overview, data-model, integrations, ADRs, diagrams
│   ├── backlog/       backlog.yaml + 24 story files + 5 epic files
│   ├── product/       Vision, personas, journey, glossary, UX flows
│   ├── releases/      pilot-scope.md, changelog.md
│   └── specifications/ api.openapi.yaml, data-states.yaml, domain-model.yaml, permissions.yaml
├── assets/            Static assets
├── css/               Stylesheets
├── data/              Local data files
├── requirements.txt   sqlcipher3-wheels, icalendar, argon2-cffi
└── AGENTS.md          Agent rules (= this repo's user rules)
```

---

## Architecture in Brief

| Layer | What | Technology |
|---|---|---|
| Persistence | Encrypted local DB | SQLite via SQLCipher (`sqlcipher3-wheels`) |
| Server | Local loopback HTTP | Python `http.server` (ThreadingHTTPServer) |
| Calendar ingestion | iCal/webcal fetch | `icalendar` library, read-only |
| Auth | Single owner account | Argon2id hash + opaque session cookie (12 h, `127.0.0.1` only) |
| Frontend | Static HTML + ES modules | Vanilla JS, no build step |
| Energy | Dynamic tariff | Tibber GraphQL API (token in `js/config.js`) |
| Weather | Public forecast | Open-Meteo REST API (lat/lon in `js/config.js`) |
| Smart home | Optional, read-only | Home Assistant (no write capability in pilot) |
| Display | Raspberry Pi + TV | Browser kiosk mode |

**Data never flows back from dashboard → external systems. All connectors are read-only.**

---

## The Five Data States (Non-Negotiable)

Defined in [`docs/specifications/data-states.yaml`](file:///Users/bejjasas/chanti-ai/projects/chit_ux/chit-dev/docs/specifications/data-states.yaml). Every value on the dashboard must carry exactly one:

| State | Meaning | May appear as "actual"? |
|---|---|---|
| `measured` | Observed by an authorised connected source | ✅ |
| `forecast` | Predicted for a future/current period | ❌ |
| `manual` | Entered explicitly by an authorised person | ❌ |
| `unavailable` | Missing, disconnected or unusable | ❌ |
| `demo` | Illustrative, never a household fact | ❌ |

**Rules:** label required on shared display; colour-only distinction is forbidden.

---

## API Contract (Draft)

Defined in [`docs/specifications/api.openapi.yaml`](file:///Users/bejjasas/chanti-ai/projects/chit_ux/chit-dev/docs/specifications/api.openapi.yaml).

Current live routes in `server/run.py`:

| Method | Path | Auth? | Purpose |
|---|---|---|---|
| GET | `/api/health` | No | `{status: ready, storage: encrypted-sqlite}` |
| GET | `/api/auth/status` | No | Whether owner account is configured |
| POST | `/api/auth/login` | No | Login → session cookie + CSRF token |
| POST | `/api/auth/logout` | Session + CSRF | Revoke session |
| GET | `/api/home/calendar` | Session | iCal events for next 21 days |
| POST | `/api/households/setup` | Session + CSRF | Configure household |
| GET | `/dashboard/household-setup.html` | Session | Setup wizard |
| GET | `/dashboard/calendar-home.html` | Session | Calendar view |

---

## JS Module Map

```
main.js
  ├── config.js         → CHIT_CONFIG (homeName, tibberToken, lat, lon, calendarEmbedHtml)
  ├── tibber.js         → initEnergy()  (Tibber GraphQL, renders energy card, graceful unavailable)
  ├── weather.js        → initWeather() (Open-Meteo, renders hourly + 7-day, graceful unavailable)
  └── calendar.js       → initCalendar() (STUB — renders "unavailable" state)
```

**`config.js` contains a real Tibber token** — do not commit changes to this file to VCS; it is gitignored locally.

---

## Accepted ADRs

| ADR | Decision |
|---|---|
| ADR-0001 | Local-first deployment (Mac Mini, loopback only) |
| ADR-0002 | Home Assistant = optional read-only integration boundary |
| ADR-0003 | Data provenance model — every record carries source, state, observedAt, ingestedAt |
| ADR-0004 | SQLite + SQLCipher for local storage; key via `CHIT_DB_KEY_HEX` env var |
| ADR-0005 | Single local owner account; Argon2id; 12-hour sessions; `127.0.0.1` only |

---

## Pilot Scope (4 slices)

| Pilot | Focus | Key stories |
|---|---|---|
| 1 — Trusted foundation | Source ingestion, provenance, privacy | US-101–106, US-301–304 |
| 2 — Shared daily view | Household dashboard, calendar availability | US-201–204, US-305, US-401, US-404 |
| 3 — Energy context | Solar forecast vs actuals, explainable suggestions | US-402–406 |
| 4 — Focused attention | Dismissible, explained attention cards | US-501–503 |

**Deferred forever (pilot scope):** WhatsApp/Telegram, appliance control, health/finance/tax agents, autonomous actions.

---

## Dashboard Modules

| Module | Data source | Graceful failure |
|---|---|---|
| Weather | Open-Meteo (public) | Card shows "Unavailable" |
| Calendar | iCal/webcal via Python server | Card shows "Unavailable"; no inferred availability |
| Family+ | Home Assistant (optional) | Degrades independently |
| Household/Appliances | Home Assistant (optional, read-only) | Degrades independently |
| Solar/Energy | Tibber + optional inverter/HA | Forecast ≠ actuals; actual only when connected |
| Attention cards | Derived insights | Must cite evidence source |

---

## Key Invariants to Never Break

1. **Never label forecast, manual, or demo data as measured.**
2. **Treat missing information as `unavailable`; never infer from absence.**
3. **All connectors are read-only in the pilot.** Write capability requires a new ADR.
4. **`observedAt` and `ingestedAt` must never be substituted for one another.**
5. **Screen-safe mode must hide sensitive data when the shared display credential is active.**
6. **Secrets (Tibber token, DB key) must never be committed to source control.**
7. **DB access only through the Python server/API boundary — no direct browser → SQLite.**

---

## Before Writing Any Code

- Identify the story ID(s) and read the story file in `docs/backlog/stories/`.
- Check relevant ADRs in `docs/architecture/adr/`.
- Confirm acceptance criteria are unambiguous.
- Propose a new ADR for any change affecting deployment, data ownership, privacy, integration boundaries, or major technology choices.

---

## Running Locally

```bash
# 1. Create and activate venv (already exists at .venv)
source .venv/bin/activate

# 2. First-time: bootstrap owner account
CHIT_DB_KEY_HEX=<32-byte-hex> python server/bootstrap_owner.py

# 3. Start the server
CHIT_DB_KEY_HEX=<32-byte-hex> python server/run.py

# 4. Open dashboard (no build step — plain HTML/JS)
open http://127.0.0.1:8080/
```

The JS dashboard at `dashboard/ux_home.html` can also be opened directly from the filesystem for the Tibber/weather modules (no server needed for those).

---

## Story Status Summary (as of 2026-09-23)

All 24 stories (US-101–US-503) are in status **`ready`**. No stories are marked `in-progress` or `done` yet — implementation has not started against the formal backlog.

