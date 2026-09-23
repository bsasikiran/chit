# Chit: Market Synthesis and Product Backlog

## Strategic position

Chit should begin as a **trustworthy, always-visible household overview**, not an autonomous butler. Its first job is to bring schedules, chores, weather, energy and solar context onto one screen, then make it obvious which information is measured, forecast, missing or illustrative. Once households trust that view, Chit can suggest what deserves attention.

This is a rapid, directional synthesis of the product concept and publicly described competitor features—not validated market sizing or customer interviews.

## Target users and pain points

| Priority | Target segment | Job to be done | Why Chit may appeal |
|---|---|---|---|
| 1 | Busy families with school-age children | See who needs to be where, what is due, and who can help over the next three days | A shared screen can reduce dependence on one person remembering and relaying everything. Research on household mental load supports investigating this need, though it does not validate demand for Chit specifically. [web:31] |
| 2 | Smart-home households with solar and dynamic electricity pricing | See household activity, production forecasts, actual generation and prices in one place | Home Assistant already supports local-first dashboards and energy management; Chit can package those inputs around household decisions rather than device controls. [web:32][web:25] |
| 3 | Privacy-conscious, technically capable households | Combine existing services without handing all family data to a single cloud platform | Local-first infrastructure and explicit source labels offer a plausible alternative to cloud-connected family displays; this segment is likely better suited to an early technical pilot than a mass-market launch. [web:32][web:14] |

Three critical pain points to test:

1. **Fragmented visibility:** Calendars, chores, school information and home systems live in different places, leaving someone to assemble the household picture.
2. **Hidden coordination work:** Knowing that an event exists is not the same as knowing who is available, what needs preparing and what remains unfinished. Unequal household mental load makes this a particularly important discovery question. [web:31]
3. **Untrustworthy or unactionable data:** A solar forecast can look like live production unless clearly labeled; stale integrations and unexplained recommendations create similar risks. Home Assistant explicitly distinguishes forecast production from actual generation. [web:25]

## Competitive landscape

| Competitor | Relevant strengths | Implication for Chit |
|---|---|---|
| **Skylight Calendar** | Dedicated household display with synced calendars, chores, lists and meal planning; its paid features include importing information from emails, images and PDFs. It requires an ongoing Wi-Fi connection. [web:14] | A shared screen and chore list alone are not differentiation. Test whether cross-domain context, local-first deployment and visible data provenance matter enough to change behavior. |
| **Home Assistant** | Local-control platform with customizable dashboards, calendar integrations, energy management and solar forecasts that can be compared with actual production. [web:32][web:24][web:25] | Treat it as both a competing DIY solution and a likely integration backbone. Chit’s proposed advantage is a family-readable, low-maintenance layer above raw entities—not a claim that Home Assistant lacks the underlying capabilities. |

FamilyWall is an adjacent family-organizer benchmark for calendars, lists, messaging and location sharing, but the two closest competitors to **this dashboard** are the household display and the configurable smart-home dashboard. [web:13]

## Product backlog

MoSCoW priority below applies to the **first usable pilot**, not the eventual full product.

| Epic | Backlog item / intended outcome | Priority |
|---|---|---|
| 1. Household data foundation | Define a common model for people, events, tasks, devices and energy readings; retain source, timestamp and availability for every item | Must Have |
| 1. Household data foundation | Connect at least one real calendar, one weather source and Home Assistant where available; degrade gracefully when a source is absent | Must Have |
| 1. Household data foundation | Add a connector framework for further school, appliance, inverter and tariff providers | Should Have |
| 2. Shared at-a-glance dashboard | Build a readable TV/tablet view with current weather, hourly outlook, week overview, next-three-day events and outstanding chores | Must Have |
| 2. Shared at-a-glance dashboard | Show household members’ availability when supported by their connected calendars; never imply availability from missing data | Must Have |
| 2. Shared at-a-glance dashboard | Allow configurable cards and household-specific layouts | Should Have |
| 3. Truth and privacy | Label values as measured, forecast, manually entered, unavailable or demo; show last-updated time and source | Must Have |
| 3. Truth and privacy | Support local deployment, access control and a screen-safe mode that hides sensitive family details on a shared display | Must Have |
| 3. Truth and privacy | Add per-person permissions for sensitive information, including health data | Should Have |
| 4. Household and energy context | Show connected appliance states, upcoming schedules and unfinished chores without automatically changing device settings | Must Have |
| 4. Household and energy context | Show public solar estimates alongside actual inverter output **only when connected**, with distinct labels | Must Have |
| 4. Household and energy context | Combine available electricity prices, solar forecasts and schedules into explainable, read-only suggestions | Should Have |
| 5. Proactive interaction | Surface a small number of relevant “needs attention” cards, each with a reason and underlying source | Should Have |
| 5. Proactive interaction | Support read-only Telegram or WhatsApp queries, subject to an integration and privacy review | Could Have |
| 5. Proactive interaction | Require explicit confirmation before messaging others, changing schedules or controlling appliances | Could Have |
| 6. Future specialist modules | Add opt-in school, health, finance and tax agents behind separate permissions and clear data boundaries | Could Have |

**Pilot sequence:** Establish trustworthy source ingestion and the shared screen first. Then test whether energy context and explainable attention cards help households act. Defer broad agent autonomy until the team has evidence that the underlying view is accurate and useful.
