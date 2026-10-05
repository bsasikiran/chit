import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from sqlcipher3 import dbapi2 as encrypted_sqlite
from chit_store import EncryptedHouseholdStore


TEST_KEY = "4c" * 32


class EncryptedHouseholdStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_dir.name) / "household.db"
        self.store = EncryptedHouseholdStore(self.database_path, TEST_KEY)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_database_is_encrypted_and_requires_the_key(self):
        self.store.create_household("Birch family", "Avery")
        with self.assertRaises(sqlite3.DatabaseError):
            sqlite3.connect(str(self.database_path)).execute("SELECT * FROM households").fetchall()
        with self.assertRaises(encrypted_sqlite.DatabaseError):
            EncryptedHouseholdStore(self.database_path, "8d" * 32)
        reopened = EncryptedHouseholdStore(self.database_path, TEST_KEY)
        self.assertEqual(reopened.list_household(
            self.store.list_household(self._household_id())["household"]["id"]
        )["household"]["name"], "Birch family")

    def test_key_is_required_and_must_be_32_bytes_hex(self):
        missing_key_path = Path(self.temp_dir.name) / "missing-key.db"
        with patch.dict("os.environ", {"CHIT_DB_KEY_HEX": ""}):
            with self.assertRaises(ValueError):
                EncryptedHouseholdStore(missing_key_path, None)
            with self.assertRaises(ValueError):
                EncryptedHouseholdStore(missing_key_path, "not-a-key")

    def test_household_profiles_and_pickup_adults_are_persisted(self):
        household = self.store.create_household("Birch family", "Avery", country_code="DE", region="Bayern")
        other_adult = self.store.add_member(household["household_id"], "adult", "Jordan", {
            "work_start": "08:30",
            "work_end": "16:30",
            "commute_minutes": 25,
            "work_days": {"monday": "office", "tuesday": "home"},
            "focus_start": "09:00",
            "focus_end": "11:00",
        })
        self.store.set_household_owner(household["household_id"], other_adult)
        child = self.store.add_member(household["household_id"], "child", "Riley", {
            "birth_date": "2018-04-12",
            "school_or_care_name": "Oak Primary",
            "after_school_care": "yes",
            "care_days": ["monday", "wednesday"],
            "pickup_adult_ids": [household["owner_member_id"], other_adult],
            "activities": [{"name": "Swimming", "location": "Pool", "days": ["friday"]}],
        })
        snapshot = self.store.list_household(household["household_id"])
        self.assertEqual(snapshot["household"]["owner_member_id"], other_adult)
        child_profile = next(member for member in snapshot["members"] if member["id"] == child)
        self.assertEqual(set(child_profile["pickup_adult_ids"]), {household["owner_member_id"], other_adult})
        self.assertEqual(child_profile["care_days"], ["monday", "wednesday"])
        self.assertEqual(child_profile["activities"][0]["name"], "Swimming")
        self.assertEqual(child_profile["activities"][0]["days"], ["friday"])
        owner_profile = next(member for member in snapshot["members"] if member["id"] == other_adult)
        self.assertEqual(owner_profile["work_days"], {"monday": "office", "tuesday": "home"})

    def test_owner_must_be_adult_in_same_household(self):
        first = self.store.create_household("First", "Avery")
        child = self.store.add_member(first["household_id"], "child", "Riley")
        second = self.store.create_household("Second", "Jordan")
        with self.assertRaises(encrypted_sqlite.IntegrityError):
            self.store.set_household_owner(first["household_id"], child)
        with self.assertRaises(encrypted_sqlite.IntegrityError):
            self.store.set_household_owner(first["household_id"], second["owner_member_id"])
        self.assertEqual(self.store.list_household(first["household_id"])["household"]["owner_member_id"], first["owner_member_id"])

    def test_read_only_calendar_source_maps_only_same_household_members(self):
        household = self.store.create_household("Birch family", "Avery")
        child = self.store.add_member(household["household_id"], "child", "Riley")
        source = self.store.add_calendar_source(
            household["household_id"], "City waste", "Waste collection",
            "webcal://calendar.example/waste.ics?secret=private", [child],
        )
        snapshot = self.store.list_household(household["household_id"])
        self.assertEqual(snapshot["calendar_sources"][0]["access_mode"], "read_only")
        self.assertEqual(snapshot["calendar_sources"][0]["member_ids"], [child])
        other = self.store.create_household("Other", "Morgan")
        with self.assertRaises(encrypted_sqlite.IntegrityError):
            self.store.add_calendar_source(
                household["household_id"], "Invalid mapping", "Work",
                "https://calendar.example/work.ics", [other["owner_member_id"]],
            )
        with self.assertRaises(ValueError):
            self.store.add_calendar_source(
                household["household_id"], "Invalid URL", "Family", "file:///private/calendar.ics"
            )

    def test_setup_payload_is_saved_atomically_with_separate_pickup_and_dropoff(self):
        setup = {
            "household": {
                "name": "Birch family",
                "timezone": "Europe/Berlin",
                "country_code": "DE",
                "region": "Bayern",
            },
            "owner_client_id": "adult-1",
            "members": [
                {
                    "client_id": "adult-1",
                    "role": "adult",
                    "name": "Avery",
                    "profile": {
                        "work_start": "09:00",
                        "work_end": "17:00",
                        "commute_minutes": 20,
                        "work_days": {"monday": "office", "tuesday": "home"},
                    },
                },
                {
                    "client_id": "adult-2",
                    "role": "adult",
                    "name": "Jordan",
                    "profile": {"work_days": {"monday": "home"}},
                },
                {
                    "client_id": "child-1",
                    "role": "child",
                    "name": "Riley",
                    "profile": {
                        "school_or_care_name": "Oak School",
                        "care_days": ["mon", "wed"],
                        "pickup_adult_client_ids": ["adult-1"],
                        "dropoff_adult_client_ids": ["adult-2"],
                        "activities": [{"name": "Football", "days": ["fri"]}],
                    },
                },
            ],
            "calendars": [{
                "client_id": "calendar-1",
                "name": "City bins",
                "category": "Waste collection",
                "subscription_url": "https://calendar.example/bins.ics",
                "member_client_ids": [],
                "chore_enabled": True,
                "chore_assignee_client_ids": ["adult-2"],
            }],
        }
        created = self.store.save_household_setup(setup)
        snapshot = self.store.list_household(created["household_id"])
        child = next(member for member in snapshot["members"] if member["name"] == "Riley")
        self.assertEqual(child["pickup_adult_ids"], [created["member_ids"]["adult-1"]])
        self.assertEqual(child["dropoff_adult_ids"], [created["member_ids"]["adult-2"]])
        self.assertEqual(snapshot["calendar_sources"][0]["access_mode"], "read_only")
        self.assertEqual(snapshot["calendar_sources"][0]["member_ids"], [])
        with self.store._connection() as connection:
            rule = connection.execute(
                "SELECT id FROM chore_generation_rules WHERE household_id = ?", (created["household_id"],)
            ).fetchone()
            assignee = connection.execute(
                "SELECT member_id FROM chore_rule_assignees WHERE rule_id = ?", (rule[0],)
            ).fetchone()[0]
        self.assertEqual(assignee, created["member_ids"]["adult-2"])

    def test_invalid_setup_rolls_back_all_household_records(self):
        setup = {
            "household": {"name": "Invalid household", "timezone": "Europe/Berlin"},
            "owner_client_id": "adult-1",
            "members": [{"client_id": "adult-1", "role": "adult", "name": "Avery", "profile": {}}],
            "calendars": [{
                "client_id": "calendar-1",
                "name": "Invalid feed",
                "category": "Family",
                "subscription_url": "file:///private/feed.ics",
                "member_client_ids": [],
            }],
        }
        with self.assertRaises(ValueError):
            self.store.save_household_setup(setup)
        with self.store._connection() as connection:
            self.assertEqual(connection.execute("SELECT count(*) FROM households").fetchone()[0], 0)

    def test_generated_chores_are_idempotent_and_preserve_completed_or_edited_state(self):
        household = self.store.create_household("Birch family", "Avery")
        owner = household["owner_member_id"]
        source = self.store.add_calendar_source(
            household["household_id"], "City waste", "waste_collection",
            "https://calendar.example/waste.ics", [owner],
        )
        rule = self.store.add_chore_rule(household["household_id"], source, "Put recycling out", [owner])
        chore = self.store.upsert_generated_chore(
            household["household_id"], source, rule, "occurrence-2026-10-05", "Put recycling out",
            "2026-10-05T06:00:00+02:00", "2026-10-01T06:00:00+02:00"
        )
        repeated = self.store.upsert_generated_chore(
            household["household_id"], source, rule, "occurrence-2026-10-05", "Put recycling out", "2026-10-05T07:00:00+02:00"
        )
        self.assertEqual(chore, repeated)
        stored_chore = self.store.list_household(household["household_id"])["chores"][0]
        self.assertEqual(stored_chore["data_state"], "measured")
        self.assertEqual(stored_chore["source_observed_at"], "2026-10-01T06:00:00+02:00")
        self.assertTrue(stored_chore["ingested_at"])
        self.assertEqual(stored_chore["assignee_ids"], [owner])
        with self.store._connection() as connection:
            self.assertEqual(connection.execute("SELECT count(*) FROM chores").fetchone()[0], 1)
            self.assertEqual(connection.execute("SELECT count(*) FROM chore_assignees WHERE chore_id = ?", (chore,)).fetchone()[0], 1)
        self.store.update_chore(household["household_id"], chore, "Moved recycling", "2026-10-05T08:00:00+02:00")
        self.store.upsert_generated_chore(
            household["household_id"], source, rule, "occurrence-2026-10-05", "Put recycling out", "2026-10-05T09:00:00+02:00"
        )
        with self.store._connection() as connection:
            row = connection.execute("SELECT title, due_at, manually_modified, data_state FROM chores WHERE id = ?", (chore,)).fetchone()
        self.assertEqual(row, ("Moved recycling", "2026-10-05T08:00:00+02:00", 1, "manual"))
        self.store.update_chore(household["household_id"], chore, "Moved recycling", "2026-10-05T08:00:00+02:00", state="completed")
        self.store.upsert_generated_chore(
            household["household_id"], source, rule, "occurrence-2026-10-05", "Changed upstream", "2026-10-05T10:00:00+02:00"
        )
        with self.store._connection() as connection:
            row = connection.execute("SELECT title, due_at, state FROM chores WHERE id = ?", (chore,)).fetchone()
        self.assertEqual(row, ("Moved recycling", "2026-10-05T08:00:00+02:00", "completed"))

    def _household_id(self):
        with self.store._connection() as connection:
            return connection.execute("SELECT id FROM households LIMIT 1").fetchone()[0]


if __name__ == "__main__":
    unittest.main()
