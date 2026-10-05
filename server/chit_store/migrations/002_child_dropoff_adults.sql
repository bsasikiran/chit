CREATE TABLE child_dropoff_adults (
    child_id TEXT NOT NULL,
    adult_id TEXT NOT NULL,
    household_id TEXT NOT NULL,
    PRIMARY KEY (child_id, adult_id),
    FOREIGN KEY (child_id, household_id)
        REFERENCES household_members(id, household_id) ON DELETE CASCADE,
    FOREIGN KEY (adult_id, household_id)
        REFERENCES household_members(id, household_id) ON DELETE CASCADE
);

CREATE TRIGGER child_dropoff_assignment_must_be_adult
BEFORE INSERT ON child_dropoff_adults
WHEN NOT EXISTS (
    SELECT 1 FROM household_members
    WHERE id = NEW.child_id AND household_id = NEW.household_id AND role = 'child'
) OR NOT EXISTS (
    SELECT 1 FROM household_members
    WHERE id = NEW.adult_id AND household_id = NEW.household_id AND role = 'adult'
)
BEGIN
    SELECT RAISE(ABORT, 'drop-off assignment must link a child to an adult in the same household');
END;
