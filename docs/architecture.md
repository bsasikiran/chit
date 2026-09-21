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

The dashboard (displayed on TV via Raspberry Pi) presents the most important user information:

- **Weather**: Current conditions and forecasts
- **Solar Production**: Expected daily solar energy generation
- **Electricity Pricing**: Graph of average hourly dynamic electricity prices
- **Power Usage Overlay**: Expected consumption graph overlaid on production graph
- **Calendar**: Today's events, reminders, and upcoming tasks (2–3 days or week view)
- **Health Metrics**: Key health data and reminders (if applicable)

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
