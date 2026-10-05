# Alfred – The Time Keeper: Sources, Settings and Rules

Status: Draft v0.3 (product split and source-ownership clarification) | Project: Chit | Branch: dev

## 0. Product split: calendar coordination and time intelligence

Alfred has two related but separately scoped parts. Part 1 establishes a useful, trustworthy household time surface. Part 2 uses that household context to decide what information or recommendation is useful at a particular time.

### Part 1: Household calendar and coordination

- Provide Today, upcoming agenda and week views, with household-wide and per-member filtering.
- Configure household members, calendar sources, source-to-member mappings and shared-display privacy.
- Combine household calendar data with read-only subscribed calendars without making Chit the owner of those calendars.
- Apply explicit, explainable source rules to turn selected calendar events into household chores when useful, such as creating a waste-collection reminder for the responsible household member or members.
- Support image/PDF and pasted-text intake as a later, human-reviewed source workflow. Do not save extracted events as confirmed without review.

Part 1 may create Chit-owned settings and task records, but it does not require a Chit-owned copy of every subscribed calendar event. A derived chore is a distinct household task linked to its source occurrence, not a write-back to the subscribed calendar.

### Part 2: Time intelligence

- Evaluate availability, conflicts, childcare gaps, pickup feasibility and other household constraints using verified calendar and settings data.
- Select and explain timely information, warnings or recommendations for the household.
- Keep deterministic rules responsible for outcomes such as availability and conflicts. An LLM may extract proposed data or phrase explanations, but does not decide those outcomes.
- Require explicit approval before any external action. Messaging, schedule changes and autonomous actions remain out of scope until separately approved.

The deterministic task-generation rules in Part 1 are bounded coordination rules: they create or update a linked chore under a configured rule. Broader prioritisation, childcare reasoning and proactive briefings belong to Part 2. Part 2 must not be a prerequisite for the calendar views to be useful.

### Scope and approval boundary

The split above records product direction, not new approved pilot acceptance criteria. The current pilot stories establish read-only calendar retrieval and display of existing chores. Calendar-triggered chore creation, document storage and Chit-owned event authoring need explicit stories and architecture/privacy review before implementation. Changes to data ownership or connector permissions may require an ADR.

## 1. Decision: Alfred coordinates household time; sources retain event authority

Use existing calendar services wherever they are suitable. Each source remains authoritative for the events it owns. A read-only subscription (for example, a waste collection or club ICS feed) is an input to Alfred, not a calendar that Alfred takes over. This replaces the earlier assumption that Alfred must own all calendar events in its own datastore.

Alfred provides the household-level value by combining source data, mapping events to household members, and applying explicit coordination rules. It may store household configuration and Chit-owned records such as derived chores. It does not need a persistent local repository containing a second, writable copy of every subscribed calendar.

Connectors may normalize records for a view or rule evaluation and may use a bounded cache if needed for performance or resilience. Any cache is an implementation detail, not a second source of truth; its retention, refresh and deletion behavior must be documented and minimized. A disconnected or stale source must be shown as stale or unavailable rather than treated as an empty calendar.

External calendar write-back, bidirectional sync and a Chit-owned general-purpose event store are not assumed. Decide these independently if a later user need justifies them.

## 2. Principles

1. Time saved is the product metric (minutes saved per household per week).
2. Read, recommend, act: Alfred recommends first and acts only with approval.
3. Nothing imported from an image or PDF is saved without review.
4. Every event and suggestion shows its source and confidence.
5. Local-first processing for personal data. No child data sent to external services without explicit opt-in.

## 3. Prerequisite: household settings

Rules can only be calculated when the basics are configured. Onboarding must complete these before Alfred produces suggestions.

### 3.1 Household
- Household name, time zone (default Europe/Berlin), country and federal state (drives school holidays and public holidays).
- Members: adults, children, optional external helpers (babysitter, grandparents).

### 3.2 Per adult
- Weekly work pattern: for each weekday, office / home / off.
- General office hours and commute time (door to door).
- At-home working hours and focus blocks.
- Default availability for evenings and weekends.
- Babysitting preferences: max evenings per week, notice needed.

### 3.3 Per child
- Birth date and age band (drives whether babysitting is needed).
- School or kita, federal state, school type and grade (drives holiday calendar).
- After-school care (Hort / Nachmittagsbetreuung): days, pick-up time, closing days.
- Activities (sports, music) with default days and times.
- Pick-up and drop-off rules: who may do it, travel time, can the child go alone.
- Babysitting required: always / only if no adult is home / never.

### 3.4 Helpers
- Name, availability pattern, contact, which children they may look after, lead time.

## 4. Source catalogue

| # | Source | Applies to | Ingestion | Review | Recurrence |
|---|---|---|---|---|---|
| S1 | Public school holidays and public holidays | Each child, household | Automatic from public iCal/API by federal state and school type | Confirm once | Yearly refresh |
| S2 | After-school care closings and special events | Each child | Upload PDF or image, paste text, or manual | Always | Per document |
| S3 | Sports and activities | Each child | Recurring rule, subscribed ICS (club calendar), manual games, PDF or image import | Always for PDF/image | Weekly rules plus one-off games |
| S4 | Adult work pattern | Each adult | Settings (office/home/off, hours) | n/a | Weekly |
| S5 | Individual events (office, friends) | One adult | Manual or quick-add text | Light | Optional |
| S6 | Couple events (date night, appointments) | Both adults | Manual or quick-add | Light | Optional |
| S7 | Family events (day trip, visit, vacation) | Whole household | Manual, multi-day supported | Light | Optional |
| S8 | External calendars (Apple, Google, ICS) | Optional | Read-only import connector | Mapping once | Sync interval |

### 4.0 Source authority and calendar composition

The source catalogue describes where information comes from; it does not imply that every source is copied into a persistent Chit event store.

- **Subscribed/read-only source:** The provider or published feed remains authoritative. Alfred reads occurrences through a connector and presents a merged household view. It never writes back to the feed.
- **Household-managed calendar:** If a household already manages events in an external calendar service, that service remains authoritative unless a separate decision explicitly changes this. Creating or editing events through its API requires an approved write scope and is not implied by read access.
- **Chit-owned coordination data:** Household settings, source-to-member mappings, rule configuration, and derived household tasks may be stored by Chit. These records refer back to their source evidence where applicable.
- **Transient normalized view:** Events from multiple services may be normalized and combined for display or rule evaluation. Persistent caching is optional, bounded by a documented retention need, and must not become an unacknowledged second source of truth.

For a merged view, preserve the source identity and event identity for each occurrence. Use those identities to avoid duplicates and to recognize the same occurrence across refreshes. Keep the original source, freshness and data state accessible. If a provider does not give enough identity or freshness information, represent that limitation rather than silently treating uncertain events as authoritative or current.

Do not merge solely by matching titles and approximate times: unrelated events can look alike, and recurring events need occurrence-level identity. Cross-provider duplicate detection beyond stable provider identifiers needs a separately specified matching and review policy.

### 4.1 S1 Public calendars
- Choose a source per federal state (school holidays, bridge days, public holidays) and store the source URL and last-refreshed date.
- Each child gets a calendar layer, because school type or state can differ.
- Alfred flags new holiday blocks as "childcare needed" if both adults work.

### 4.2 S2 After-school care and special events
- Input: image, PDF, pasted email text.
- Pipeline: extract text (OCR for images) -> local LLM turns text into structured events -> validation (dates in range, time zone, duplicates) -> review screen with source snippet beside each proposed event -> save.
- Typical results: closing days, holiday programs, parent evenings, excursions with special pick-up time, items to bring.

### 4.3 S3 Sports and activities
Three input modes per activity:
1. Recurring training: weekday, start, end, location, season start and end, exceptions (holidays, cancelled sessions).
2. Subscribed calendar: ICS/webcal from a club, read-only, refreshed on a schedule.
3. One-off games or tournaments: manual, or image/PDF import using the S2 pipeline.
Each event carries: child, transport need (drop-off, pick-up, stay and watch), who is expected, and equipment notes.

### Calendar events that become household chores

Do not turn every calendar event into a task. A household administrator configures explicit rules for source calendars or event categories that have a useful household responsibility. Waste collection is a representative case: a subscribed feed supplies collection type and date; a household rule can produce a chore such as "Put paper recycling out" with a due time and one or more responsible members.

The chore is a Chit-owned task, not a copy of the source event and not a change to the subscribed calendar. The task should retain a reference to the source calendar and occurrence, the rule that produced it, its generation/update time, and its assigned member or members. The UI should make clear which details came from the feed and which came from household configuration.

Generation must be repeatable without creating duplicate tasks on every refresh. When an open source occurrence changes, update the linked open chore or surface the change for review according to an agreed policy. Do not silently erase a completed or manually changed chore when a feed changes or an occurrence disappears. The lifecycle for changed, cancelled and completed generated chores needs explicit acceptance criteria.

This is deterministic coordination, not an agent decision: configured source/category rules define whether a task is created, its due-time offset, and eligible assignees. Do not infer a responsible person from event absence or assign a person without an explicit household rule. Broader childcare conclusions and prioritisation remain in Part 2.

### 4.4 S4 to S7 Adult and shared events
Event scope decides who must be free:

| Scope | Attendees | Childcare rule |
|---|---|---|
| Individual | One adult | The other adult covers. Babysitter only if the other adult is unavailable. |
| Couple | Both adults | Babysitter needed for every child who needs supervision. |
| Family | Everyone | No babysitter. Check every member's conflicts instead. |

Individual events can be shared as "optional for the other partner" (for example, a friend invite where only one of them goes).

## 5. Core data model (draft; not a mandate to persist subscribed events)

- Household(id, timezone, state)
- Member(id, household_id, role[adult|child|helper], name, birth_date)
- MemberSettings(member_id, work_pattern, office_hours, commute_min, babysitting_policy, ...)
- Source(id, type, owner_scope, url_or_file, last_sync, trust_level)
- Event: normalized source occurrence for a view or rule; retain provider/calendar identity and occurrence identity. Persistence and write ownership are source-specific decisions, not assumed by this conceptual model.
- Task(id, title, owner[], due, source_occurrence_ref, generation_rule_ref, state, updated_at)
- Suggestion(id, type, reason, affected_events[], proposed_change, state[open|accepted|dismissed])
- AuditLog(id, actor, action, before, after, timestamp)

These draft fields must be reconciled with the accepted normalized record envelope and domain specification before implementation. In particular, generated tasks need provenance and lifecycle semantics; do not add fields or data states that conflict with the approved contracts.

## 6. Rule engine (first rules)

1. Availability = work pattern (S4) minus confirmed events minus travel buffers.
2. Conflict: an attendee has two overlapping events including buffers.
3. Childcare gap: for each child who needs supervision at a time, at least one adult or helper must be available. Otherwise raise "babysitter needed" with the date, time and the reason.
4. Pick-up feasibility: pick-up time minus travel time must fall inside the assigned adult's availability.
5. Holiday gap: school holiday or care closing on a day when both adults are in the office raises a childcare warning at least 14 days ahead (configurable).
6. Free-slot finder: find slots of N minutes where chosen members are all free (date night, family outing).
7. Load balancing: report how many pick-ups, evenings and childcare duties each adult carries per week.
8. Energy and weather overlay (later): suggest laundry or similar tasks in the cheapest Tibber window, and flag weather for outdoor events.

Rules are deterministic code. The local LLM is used only for extraction and for writing explanations, not for deciding availability.

## 7. Ingestion pipeline (image and PDF)

1. Upload or share to Alfred.
2. Store the original file encrypted.
3. Text extraction (PDF text layer, otherwise OCR).
4. Local LLM extracts events into the JSON schema.
5. Validation: dates plausible, school year matches, duplicates detected, time zone applied.
6. Review screen: original snippet beside the proposed event, with a confidence score. Low confidence is highlighted.
7. Approve, edit or reject. Approved events become confirmed.
8. Quality tracking: record the correction rate per source type to decide when review can be lighter.

## 8. Security and privacy

- Store Chit-owned structured data in SQLite on household-controlled infrastructure and require encryption at rest, including protection for backups and persisted files. Select the encryption mechanism and key lifecycle before implementation (see [ADR-0004](../architecture/adr/0004-sqlite-encrypted-local-storage.md)).
- Application authentication, authorization and member access management remain undecided and must be designed separately; database encryption does not replace them.
- Local LLM inference (for example via Ollama or llama.cpp) for any file containing personal or children's data.
- Per-member permissions: adults see everything by default, helpers see only the events they are assigned to.
- Audit log for all changes, export and delete-everything function.
- Secrets in environment variables, never in the repository.

## 9. Time engine requirements

- Store instants in UTC, with the original time zone and rule kept for recurrences.
- Correct handling of daylight saving, recurring events with exceptions, multi-day and all-day events.
- ICS export per member and per child, with stable event UIDs.
- Unit tests first. Include daylight saving transition weeks and school-holiday edge cases.

## 10. Build order by product part

| Phase | Part | Outcome |
|---|---|---|
| 0 | Part 1 foundation | Confirm event ownership, read/write permissions, source retention/cache policy, member mapping, task-generation lifecycle and the pilot/story boundary. Update stories and contracts before implementation. |
| 1 | Part 1 calendar | Build Today, agenda and week views over at least one real calendar source; show household/member filters, source health, freshness, private-event masking and unknown/unavailable states. |
| 2 | Part 1 composition | Combine read-only subscribed sources with household calendar sources; preserve identities and provenance, prevent repeat ingestion, and validate that refresh or source failure does not imply free time. |
| 3 | Part 1 coordination | Add configured, deterministic event-to-chore rules using a narrow case such as waste collection. Store linked task records, avoid duplicates, and test source changes, cancellation and completion behavior. This requires a new/updated story beyond US-401's current display-only acceptance criteria. |
| 4 | Part 1 additional intake | Add public/school calendars, recurring activities and human-reviewed image/PDF or pasted-text intake only after source-specific retention, privacy, validation and review behavior are approved. |
| 5 | Part 2 time intelligence | Add availability, conflicts, childcare gaps, pickup feasibility, free-slot search and workload summaries as independently testable deterministic services. |
| 6 | Part 2 timely guidance | Add explainable, appropriately timed information and recommendations; require approval for external actions. |

## 11. Open questions and research

- For events that household members create, should Alfred open the existing provider calendar, use an explicitly authorized provider write integration, or create a Chit-owned event? Do not silently mix these ownership models.
- Which sources need a persistent cache, and what is the minimum retention period needed for display resilience, rule evaluation and deletion on disconnect?
- What stable identifiers and freshness guarantees do target subscribed feeds provide, and how should duplicates across different providers be reviewed?
- For generated chores, should the first version create them automatically under an administrator-configured rule or present a proposal for confirmation? How should changed/cancelled feed occurrences affect open, edited and completed chores?
- Which waste collection source is reliable for the target household and does it expose bin type, collection date, stable occurrence identity and update/cancellation information?
- Best public source for school holidays in the household's federal state, and whether it covers each school type.
- Which local model and OCR combination gives the best accuracy on German school letters and club schedules.
- Babysitter workflow: message templates, who confirms, and how to handle last-minute changes.
- How to display Alfred events in phone calendars with the least friction (ICS subscription vs. two-way sync).
- Handling shared custody or extended family (grandparents) as additional members.
- Metric collection: how to measure minutes saved without being intrusive.

## 12. Acceptance checks

- A full real week can be presented from the connected household sources without requiring Alfred to own a duplicate persistent copy of every subscribed calendar.
- A subscribed waste-collection occurrence can produce at most one linked chore for the configured household rule, with source, due time and assigned member(s) visible.
- A changed or cancelled subscribed occurrence does not silently delete a completed or manually changed chore.
- A date night event automatically produces a babysitter need, and a family event does not.
- An uploaded care-closing PDF yields correct events after one review.
- Switching a child's federal state changes the holidays shown.

The final three checks involve Part 2 or later Part 1 intake capabilities and should not block delivery of the initial calendar view. Acceptance criteria and ordering must be assigned to approved stories before implementation.
