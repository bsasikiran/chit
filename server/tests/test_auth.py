import unittest
from pathlib import Path
import tempfile

from chit_store import EncryptedHouseholdStore
from chit_store.auth import OwnerAuth


TEST_KEY = "a7" * 32


class OwnerAuthTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        store = EncryptedHouseholdStore(Path(self.temp_dir.name) / "auth.db", TEST_KEY)
        self.auth = OwnerAuth(store)
        self.store = store

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_bootstrap_stores_hash_and_allows_single_owner(self):
        self.auth.create_owner("owner", "a-long-development-password")
        self.assertTrue(self.auth.is_configured())
        self.assertEqual(self.auth.verify_credentials("owner", "a-long-development-password"), "owner")
        self.assertIsNone(self.auth.verify_credentials("owner", "incorrect-password"))
        with self.store._connection() as connection:
            stored_hash = connection.execute("SELECT password_hash FROM auth_account WHERE id = 1").fetchone()[0]
        self.assertTrue(stored_hash.startswith("$argon2id$"))
        self.assertNotIn("a-long-development-password", stored_hash)
        with self.assertRaises(ValueError):
            self.auth.create_owner("second", "another-long-password")

    def test_session_requires_valid_csrf_and_can_be_revoked(self):
        self.auth.create_owner("owner", "a-long-development-password")
        session = self.auth.create_session("owner")
        current = self.auth.get_session(session["session_token"])
        self.assertEqual(current["username"], "owner")
        self.assertTrue(self.auth.validate_csrf(current, session["csrf_token"]))
        self.assertFalse(self.auth.validate_csrf(current, "incorrect"))
        self.auth.revoke_session(session["session_token"])
        self.assertIsNone(self.auth.get_session(session["session_token"]))

    def test_password_policy_rejects_short_password(self):
        with self.assertRaises(ValueError):
            self.auth.create_owner("owner", "short")
        self.assertFalse(self.auth.is_configured())


if __name__ == "__main__":
    unittest.main()
