# Alfred – The Time Keeper: Sources, Settings and Rules

Status: Draft v0.2 (extends the Alfred build plan) | Project: Chit | Branch: dev

## 1. Decision: Alfred owns the calendar

Apple Calendar is no longer the system of record. Alfred keeps its own secure datastore, and every external source (including Apple Calendar) becomes an optional import or export connector.

Why:
- Removes the biggest dependency and risk (no public Apple Calendar API, CalDAV quirks, no semantic data such as "needs babysitter").
- Alfred needs data a normal calendar cannot hold: who must attend, who is responsible, babysitting need, travel buffers, source confidence.
- Local LLMs and a private store keep family and children's data inside the household.
- Faster iteration: the schema and rules are ours.

Trade-offs to manage:
- Families still look at phone calendars. Provide a one-way export (ICS feed per member) so Alfred events show up in Apple/Google Calendar. Two-way sync is optional and later.
- Ingestion quality (PDF/image) becomes critical, so every import goes through human review.

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

### 4.4 S4 to S7 Adult and shared events
Event scope decides who must be free:

| Scope | Attendees | Childcare rule |
|---|---|---|
| Individual | One adult | The other adult covers. Babysitter only if the other adult is unavailable. |
| Couple | Both adults | Babysitter needed for every child who needs supervision. |
| Family | Everyone | No babysitter. Check every member's conflicts instead. |

Individual events can be shared as "optional for the other partner" (for example, a friend invite where only one of them goes).

## 5. Core data model (draft)

- Household(id, timezone, state)
- Member(id, household_id, role[adult|child|helper], name, birth_date)
- MemberSettings(member_id, work_pattern, office_hours, commute_min, babysitting_policy, ...)
- Source(id, type, owner_scope, url_or_file, last_sync, trust_level)
- Event(id, title, start, end, all_day, timezone, scope[individual|couple|family|child], attendees[], organizer, location, travel_buffer_min, needs_transport, needs_childcare, recurrence_rule, exceptions[], source_id, source_snippet, confidence, status[proposed|confirmed|cancelled], created_by, updated_at)
- Task(id, title, owner, due, linked_event_id)
- Suggestion(id, type, reason, affected_events[], proposed_change, state[open|accepted|dismissed])
- AuditLog(id, actor, action, before, after, timestamp)

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

- Encrypted datastore (encryption at rest) and hosting in the EU or on a home server.
- Local LLM inference (for example via Ollama or llama.cpp) for any file containing personal or children's data.
- Per-member permissions: adults see everything by default, helpers see only the events they are assigned to.
- Audit log for all changes, export and delete-everything function.
- Secrets in environment variables, never in the repository.

## 9. Time engine requirements

- Store instants in UTC, with the original time zone and rule kept for recurrences.
- Correct handling of daylight saving, recurring events with exceptions, multi-day and all-day events.
- ICS export per member and per child, with stable event UIDs.
- Unit tests first. Include daylight saving transition weeks and school-holiday edge cases.

## 10. Build order (revised)

| Phase | Outcome |
|---|---|
| 0 | Settings schema, onboarding, data model and docs |
| 1 | Manual event entry with scopes, work pattern and a household timeline ("Today", "Week") |
| 2 | S1 public holidays and school holidays, S3 recurring training, ICS export |
| 3 | Rule engine: conflicts, childcare gaps, pick-up feasibility, free-slot finder |
| 4 | S2/S3 image and PDF import with local LLM and review screen |
| 5 | Optional S8 external calendar import, Tibber and weather overlay, daily brief |
| 6 | Recommend-and-approve actions, helper (babysitter) requests |

## 11. Open questions and research

- Best public source for school holidays in the household's federal state, and whether it covers each school type.
- Which local model and OCR combination gives the best accuracy on German school letters and club schedules.
- Babysitter workflow: message templates, who confirms, and how to handle last-minute changes.
- How to display Alfred events in phone calendars with the least friction (ICS subscription vs. two-way sync).
- Handling shared custody or extended family (grandparents) as additional members.
- Metric collection: how to measure minutes saved without being intrusive.

## 12. Acceptance checks

- A full real week, including school, care, activities and adult work pattern, is represented correctly without Apple Calendar.
- A date night event automatically produces a babysitter need, and a family event does not.
- An uploaded care-closing PDF yields correct events after one review.
- Switching a child's federal state changes the holidays shown.
