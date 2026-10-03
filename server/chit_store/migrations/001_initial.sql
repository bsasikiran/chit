CREATE TABLE households (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL CHECK (length(trim(name)) > 0),
    timezone TEXT NOT NULL,
    country_code TEXT,
    region TEXT,
    owner_member_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (owner_member_id) REFERENCES household_members(id)
        DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE household_members (
    id TEXT PRIMARY KEY,
    household_id TEXT NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('adult', 'child', 'helper')),
    name TEXT NOT NULL CHECK (length(trim(name)) > 0),
    birth_date TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (id, household_id)
);

CREATE INDEX household_members_by_household ON household_members(household_id, role, name);

CREATE TRIGGER household_owner_must_be_adult
BEFORE UPDATE OF owner_member_id ON households
WHEN NOT EXISTS (
    SELECT 1 FROM household_members
    WHERE id = NEW.owner_member_id
      AND household_id = NEW.id
      AND role = 'adult'
)
BEGIN
    SELECT RAISE(ABORT, 'household owner must be an adult in this household');
END;

CREATE TRIGGER household_owner_cannot_be_removed
BEFORE DELETE ON household_members
WHEN EXISTS (
    SELECT 1 FROM households
    WHERE id = OLD.household_id AND owner_member_id = OLD.id
)
BEGIN
    SELECT RAISE(ABORT, 'transfer household ownership before removing the owner');
END;

CREATE TABLE adult_settings (
    member_id TEXT PRIMARY KEY REFERENCES household_members(id) ON DELETE CASCADE,
    work_start TEXT,
    work_end TEXT,
    commute_minutes INTEGER CHECK (commute_minutes IS NULL OR commute_minutes >= 0),
    evening_weekend_availability TEXT NOT NULL DEFAULT 'not_set'
        CHECK (evening_weekend_availability IN ('not_set', 'available', 'unavailable', 'varies')),
    focus_start TEXT,
    focus_end TEXT,
    babysitting_max_evenings INTEGER
        CHECK (babysitting_max_evenings IS NULL OR babysitting_max_evenings >= 0),
    babysitting_notice TEXT NOT NULL DEFAULT 'not_set'
        CHECK (babysitting_notice IN ('not_set', 'same_day', 'one_day', 'two_days', 'one_week'))
);

CREATE TABLE adult_work_days (
    member_id TEXT NOT NULL REFERENCES adult_settings(member_id) ON DELETE CASCADE,
    weekday INTEGER NOT NULL CHECK (weekday BETWEEN 0 AND 6),
    location TEXT NOT NULL CHECK (location IN ('office', 'home', 'off')),
    PRIMARY KEY (member_id, weekday)
);

CREATE TABLE child_settings (
    member_id TEXT PRIMARY KEY REFERENCES household_members(id) ON DELETE CASCADE,
    school_or_care_name TEXT,
    school_type_or_year TEXT,
    after_school_care TEXT NOT NULL DEFAULT 'not_set'
        CHECK (after_school_care IN ('not_set', 'yes', 'no', 'varies')),
    pickup_time TEXT,
    supervision_policy TEXT NOT NULL DEFAULT 'not_set'
        CHECK (supervision_policy IN ('not_set', 'always', 'sometimes', 'independent')),
    travel_minutes INTEGER CHECK (travel_minutes IS NULL OR travel_minutes >= 0)
);

CREATE TABLE child_care_days (
    member_id TEXT NOT NULL REFERENCES child_settings(member_id) ON DELETE CASCADE,
    weekday INTEGER NOT NULL CHECK (weekday BETWEEN 0 AND 6),
    PRIMARY KEY (member_id, weekday)
);

CREATE TABLE child_pickup_adults (
    child_id TEXT NOT NULL,
    adult_id TEXT NOT NULL,
    household_id TEXT NOT NULL,
    PRIMARY KEY (child_id, adult_id),
    FOREIGN KEY (child_id, household_id)
        REFERENCES household_members(id, household_id) ON DELETE CASCADE,
    FOREIGN KEY (adult_id, household_id)
        REFERENCES household_members(id, household_id) ON DELETE CASCADE
);

CREATE TRIGGER child_pickup_assignment_must_be_adult
BEFORE INSERT ON child_pickup_adults
WHEN NOT EXISTS (
    SELECT 1 FROM household_members
    WHERE id = NEW.child_id AND household_id = NEW.household_id AND role = 'child'
) OR NOT EXISTS (
    SELECT 1 FROM household_members
    WHERE id = NEW.adult_id AND household_id = NEW.household_id AND role = 'adult'
)
BEGIN
    SELECT RAISE(ABORT, 'pickup assignment must link a child to an adult in the same household');
END;

CREATE TABLE child_activities (
    id TEXT PRIMARY KEY,
    member_id TEXT NOT NULL REFERENCES child_settings(member_id) ON DELETE CASCADE,
    name TEXT NOT NULL CHECK (length(trim(name)) > 0),
    location TEXT,
    start_time TEXT,
    end_time TEXT
);

CREATE TABLE child_activity_days (
    activity_id TEXT NOT NULL REFERENCES child_activities(id) ON DELETE CASCADE,
    weekday INTEGER NOT NULL CHECK (weekday BETWEEN 0 AND 6),
    PRIMARY KEY (activity_id, weekday)
);

CREATE TABLE calendar_sources (
    id TEXT PRIMARY KEY,
    household_id TEXT NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    name TEXT NOT NULL CHECK (length(trim(name)) > 0),
    category TEXT NOT NULL CHECK (category IN (
        'waste_collection', 'school_care', 'sport_activity', 'work', 'family', 'other'
    )),
    subscription_url TEXT NOT NULL,
    access_mode TEXT NOT NULL DEFAULT 'read_only' CHECK (access_mode = 'read_only'),
    connection_state TEXT NOT NULL DEFAULT 'not_checked'
        CHECK (connection_state IN ('not_checked', 'available', 'unavailable', 'stale', 'unknown')),
    last_checked_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (id, household_id)
);

CREATE TABLE calendar_source_members (
    source_id TEXT NOT NULL,
    household_id TEXT NOT NULL,
    member_id TEXT NOT NULL,
    PRIMARY KEY (source_id, member_id),
    FOREIGN KEY (source_id, household_id)
        REFERENCES calendar_sources(id, household_id) ON DELETE CASCADE,
    FOREIGN KEY (member_id, household_id)
        REFERENCES household_members(id, household_id) ON DELETE CASCADE
);

CREATE TABLE chore_generation_rules (
    id TEXT PRIMARY KEY,
    household_id TEXT NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    source_id TEXT NOT NULL,
    title_template TEXT NOT NULL CHECK (length(trim(title_template)) > 0),
    enabled INTEGER NOT NULL DEFAULT 1 CHECK (enabled IN (0, 1)),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (id, source_id),
    FOREIGN KEY (source_id, household_id)
        REFERENCES calendar_sources(id, household_id) ON DELETE CASCADE
);

CREATE TABLE chore_rule_assignees (
    rule_id TEXT NOT NULL,
    source_id TEXT NOT NULL,
    member_id TEXT NOT NULL,
    household_id TEXT NOT NULL,
    PRIMARY KEY (rule_id, member_id),
    FOREIGN KEY (rule_id, source_id)
        REFERENCES chore_generation_rules(id, source_id) ON DELETE CASCADE,
    FOREIGN KEY (source_id, household_id)
        REFERENCES calendar_sources(id, household_id) ON DELETE CASCADE,
    FOREIGN KEY (member_id, household_id)
        REFERENCES household_members(id, household_id) ON DELETE CASCADE
);

CREATE TABLE chores (
    id TEXT PRIMARY KEY,
    household_id TEXT NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    title TEXT NOT NULL CHECK (length(trim(title)) > 0),
    due_at TEXT,
    state TEXT NOT NULL DEFAULT 'open' CHECK (state IN ('open', 'completed', 'cancelled')),
    data_state TEXT NOT NULL CHECK (data_state IN ('measured', 'forecast', 'manual', 'unavailable', 'demo')),
    availability_status TEXT NOT NULL DEFAULT 'available'
        CHECK (availability_status IN ('available', 'unavailable', 'unknown')),
    availability_reason TEXT,
    source_observed_at TEXT,
    ingested_at TEXT NOT NULL,
    source_id TEXT,
    source_occurrence_ref TEXT,
    generation_rule_id TEXT,
    manually_modified INTEGER NOT NULL DEFAULT 0 CHECK (manually_modified IN (0, 1)),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    CHECK (
        (source_id IS NULL AND source_occurrence_ref IS NULL AND generation_rule_id IS NULL)
        OR
        (source_id IS NOT NULL AND source_occurrence_ref IS NOT NULL AND generation_rule_id IS NOT NULL)
    ),
    UNIQUE (source_id, source_occurrence_ref, generation_rule_id),
    FOREIGN KEY (source_id, household_id)
        REFERENCES calendar_sources(id, household_id) ON DELETE CASCADE,
    FOREIGN KEY (generation_rule_id, source_id)
        REFERENCES chore_generation_rules(id, source_id) ON DELETE CASCADE
);

CREATE INDEX chores_by_household_state_due ON chores(household_id, state, due_at);

CREATE TABLE chore_assignees (
    chore_id TEXT NOT NULL REFERENCES chores(id) ON DELETE CASCADE,
    member_id TEXT NOT NULL,
    household_id TEXT NOT NULL,
    PRIMARY KEY (chore_id, member_id),
    FOREIGN KEY (member_id, household_id)
        REFERENCES household_members(id, household_id) ON DELETE CASCADE
);
