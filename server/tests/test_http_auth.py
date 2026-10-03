from http.cookies import SimpleCookie
from http.server import ThreadingHTTPServer
from http.client import HTTPConnection
from pathlib import Path
import json
import tempfile
from threading import Thread
import unittest

from chit_store import EncryptedHouseholdStore
from chit_store.auth import OwnerAuth
from run import ChitHandler


TEST_KEY = "9b" * 32


class AuthenticatedHTTPTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        store = EncryptedHouseholdStore(Path(self.temp_dir.name) / "http.db", TEST_KEY)
        self.auth = OwnerAuth(store)
        self.auth.create_owner("owner", "a-long-development-password")
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), ChitHandler)
        self.server.store = store
        self.server.auth = self.auth
        self.server.login_attempts = {}
        self.server_thread = Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()
        self.host, self.port = self.server.server_address

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.server_thread.join(timeout=2)
        self.temp_dir.cleanup()

    def request(self, method, path, body=None, headers=None):
        connection = HTTPConnection(self.host, self.port, timeout=3)
        connection.request(method, path, body=body, headers=headers or {})
        response = connection.getresponse()
        result = (response.status, response.getheaders(), response.read())
        connection.close()
        return result

    def test_owner_login_protects_pages_and_csrf_protects_saves(self):
        status, headers, _ = self.request("GET", "/dashboard/calendar-home.html")
        self.assertEqual(status, 302)
        self.assertTrue(dict(headers)["Location"].startswith("/login.html?next="))

        status, response_headers, body = self.request(
            "POST", "/api/auth/login",
            json.dumps({"username": "owner", "password": "a-long-development-password"}),
            {"Content-Type": "application/json", "Origin": "http://127.0.0.1:%d" % self.port},
        )
        self.assertEqual(status, 200)
        session_data = json.loads(body)
        set_cookie = dict(response_headers)["Set-Cookie"]
        cookie = SimpleCookie()
        cookie.load(set_cookie)
        cookie_header = "%s=%s" % ("chit_session", cookie["chit_session"].value)

        status, _, _ = self.request("GET", "/dashboard/calendar-home.html", headers={"Cookie": cookie_header})
        self.assertEqual(status, 200)

        payload = {
            "household": {"name": "Authenticated household", "timezone": "Europe/Berlin"},
            "owner_client_id": "adult-1",
            "members": [{"client_id": "adult-1", "role": "adult", "name": "Owner", "profile": {}}],
            "calendars": [],
        }
        headers = {"Content-Type": "application/json", "Cookie": cookie_header}
        status, _, _ = self.request("POST", "/api/households/setup", json.dumps(payload), headers)
        self.assertEqual(status, 403)
        headers["X-CSRF-Token"] = session_data["csrf_token"]
        status, _, _ = self.request("POST", "/api/households/setup", json.dumps(payload), headers)
        self.assertEqual(status, 201)

        status, _, _ = self.request("POST", "/api/auth/logout", headers={
            "Cookie": cookie_header, "X-CSRF-Token": session_data["csrf_token"]
        })
        self.assertEqual(status, 200)
        status, _, _ = self.request("GET", "/dashboard/calendar-home.html", headers={"Cookie": cookie_header})
        self.assertEqual(status, 302)

    def test_wrong_origin_and_wrong_password_are_rejected(self):
        status, _, _ = self.request(
            "POST", "/api/auth/login",
            json.dumps({"username": "owner", "password": "a-long-development-password"}),
            {"Content-Type": "application/json", "Origin": "http://attacker.example"},
        )
        self.assertEqual(status, 403)
        status, _, _ = self.request(
            "POST", "/api/auth/login",
            json.dumps({"username": "owner", "password": "incorrect-password"}),
            {"Content-Type": "application/json", "Origin": "http://127.0.0.1:%d" % self.port},
        )
        self.assertEqual(status, 401)


if __name__ == "__main__":
    unittest.main()
