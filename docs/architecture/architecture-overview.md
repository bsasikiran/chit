# Chit System Architecture

## Overview

**Chit** is a personal automation and intelligence platform—a "logic layer" or "brain" that orchestrates agents, time-based triggers, and data flows across local hardware, cloud services, and user interfaces.

---

## Core Components

### 1. Logic Layer: Chit (The Brain)

- Central orchestration engine
- Manages agent communication and task routing
- Executes time-based triggered scripts and automations
- Ensures no hallucination: only provides information when it has verified data

### 2. Agent Network

| Agent | Role | Description |
|-------|------|-------------|
| **meA** | Catch & Dispatch | Primary intake agent; receives user inputs and routes tasks to specialized agents |
| **Kara** | Tax Agent | Handles tax-related queries, calculations, and document organization |
| **Buffett** | Financial Agent | Manages financial tracking, budgeting, investment insights, and expense analysis |
| **Baymax** | Health Agent | Tracks health metrics, provides reminders, and offers wellness guidance |
| **Alfred** | Butler Agent | Manages calendar, reminders, scheduling, and general productivity tasks |

### 3. User Interface

- **Primary**: WhatsApp or Telegram (messaging-based interaction)
- **Secondary**: Web dashboard displayed on TV via Raspberry Pi

---

## Hardware Infrastructure

### Local Stack (Mac Mini)

- **Plex Media Server**: Media library and streaming
- **Home Assistant**: Smart home automation and device integration
- **OpenClaw**: Local LLM inference and AI processing
- **HTTP Container**: Hosts HTML/JS pages and dashboard interface
- **Lite Database**: Lightweight local datastore for structured data

### Work Mac

- **Local AI Processing**: Handles intensive AI/ML tasks requiring more compute
- **Development Environment**: Coding, testing, and deployment workflows

### Raspberry Pi

- **TV Display**: Connected to television to show web-based dashboard
- **Kiosk Mode**: Runs browser in fullscreen for always-on dashboard view

### Cloud Services

- **Gemini Pro**: Cloud-based AI for tasks requiring external dependencies, enhanced reasoning, or when local models are insufficient

---

## Dashboard Features

The dashboard (displayed on TV via Raspberry Pi) is an always-ready, read-only awareness board. During the first design phase all modules remain visible; prioritisation and responsive real-estate rules will evolve after the complete information surface is understood.

### Weather module

- Today is the primary visual: current temperature, condition, and the next eight hourly points in one row.
- A seven-day row shows only the weather type plus high and low temperatures.
- Public forecast data can come from Open-Meteo; the current prototype supports location coordinates and a demo fallback.

### Calendar module

- Shows every scheduled event plus chores and reminders across the next three days.
- Calendar data is expected from a connected calendar service; the dashboard must distinguish connected data from demo or unavailable data.

### Family+ module

- Shows each household member's current presence and context without persisting their hour-by-hour location.
- Surfaces near-term school and family events, such as the next five working days and the next exam.
- Shows consented key health metrics such as steps, sleep, and HRV. The model can extend to seniors and their metrics.

### Household module

- Shows appliance state and schedules for the washing machine, dryer, and dishwasher.
- Connects chores to electricity price and solar windows, including unfinished weekly washing and the best available run time.
- Home Assistant is the local integration boundary for device state and automation.

### Solar production module

- Separates public estimates from private inverter data: weather and sun-position estimates may be fetched publicly, while measured production requires a user-configured inverter or Home Assistant connection.
- Displays estimated daily production, current output, peak production hour, dynamic electricity price, and the best household action.

### Current dashboard composition

The first home board is implemented in `dashboard/ux_home.html`. It keeps Weather, Calendar, Family+, Household, Solar, and connection configuration visible at once. It uses demo data when a private integration is not configured and labels connection state so estimates are not presented as measured facts.

---

## Data Flow

```
User Input (WhatsApp/Telegram)
        ↓
      meA (Catch & Dispatch)
        ↓
   ┌────┴────┬─────────┬────────┬────────┐
   ↓         ↓         ↓        ↓        ↓
  Kara    Buffett   Baymax  Alfred  Other
(Tax)   (Finance) (Health) (Calendar) Agents
   ↓         ↓         ↓        ↓        ↓
   └────┬────┴─────────┴────────┴────────┘
        ↓
    Chit (Logic Layer)
        ↓
   ┌────┴────────────────────┐
   ↓                         ↓
Local Hardware          Cloud Services
(Mac Mini, RPi)         (Gemini Pro)
        ↓
   Dashboard (TV)
```

---

## Design Principles

1. **No Hallucination**: Agents only respond with verified, available information
2. **Local-First**: Prioritize local processing for privacy and speed
3. **Hybrid Architecture**: Seamlessly blend local and cloud resources
4. **Modular Agents**: Each agent has a clear, focused responsibility
5. **Passive Display**: Dashboard provides at-a-glance awareness without interaction
6. **Conversational Interface**: Natural language interaction via messaging apps

---

## Technology Stack Summary

| Layer | Technology |
|-------|------------|
| **Orchestration** | Chit (custom logic layer) |
| **AI/LLM** | OpenClaw (local), Gemini Pro (cloud) |
| **Messaging** | WhatsApp / Telegram |
| **Smart Home** | Home Assistant |
| **Media** | Plex |
| **Web Server** | HTTP container (HTML/JS) |
| **Database** | Lite Database (local) |
| **Display** | Raspberry Pi + TV |
| **Compute** | Mac Mini (primary), Work Mac (intensive tasks) |

---

## Future Considerations

- Agent memory and context persistence
- Inter-agent collaboration protocols
- Data synchronization between local and cloud
- Security and access control for messaging interfaces
- Expansion to additional specialized agents (e.g., legal, travel, shopping)

---

*Document created: September 21, 2026*

## Documentation status

This overview describes the broader intended ecosystem. The approved first-pilot boundaries and implementation order are defined by `docs/releases/pilot-scope.md`, the accepted ADRs and individual backlog stories. If the broader vision conflicts with pilot scope, the pilot documents take precedence.

## Pilot architecture boundary

The first pilot consists of connector adapters, a normalized household data layer, read-only insight services, an API/presentation policy layer and a shared dashboard. Home Assistant remains an optional read-only integration boundary. Messaging and specialist agents remain outside the first pilot.

See the architecture-as-code files under `docs/architecture/diagrams/` and machine-readable contracts under `docs/specifications/`.
