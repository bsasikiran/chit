from __future__ import annotations

from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import secrets
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHash, VerificationError, VerifyMismatchError

from .store import EncryptedHouseholdStore, _now, _required_text


SESSION_HOURS = 12
PASSWORD_HASHER = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=2, hash_len=32, salt_len=16)
DUMMY_PASSWORD_HASH = PASSWORD_HASHER.hash("invalid-owner-password-for-timing-equalization")


def _token_hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _hash_password(password: str) -> str:
    return PASSWORD_HASHER.hash(password)


def _verify_password(password: str, encoded: str) -> bool:
    try:
        return PASSWORD_HASHER.verify(encoded, password)
    except (InvalidHash, VerificationError, VerifyMismatchError, ValueError):
        return False


class OwnerAuth:
    def __init__(self, store: EncryptedHouseholdStore):
        self.store = store

    def is_configured(self) -> bool:
        with self.store._connection() as connection:
            return connection.execute("SELECT 1 FROM auth_account WHERE id = 1").fetchone() is not None

    def create_owner(self, username: str, password: str) -> None:
        username = _required_text(username, "username")
        if len(username) > 100:
            raise ValueError("username must be 100 characters or fewer")
        if len(password) < 12:
            raise ValueError("password must be at least 12 characters")
        password_hash = _hash_password(password)
        try:
            with self.store._connection() as connection:
                connection.execute(
                    "INSERT INTO auth_account(id, username, password_hash, created_at) VALUES (1, ?, ?, ?)",
                    (username, password_hash, _now()),
                )
        except Exception as error:
            if "UNIQUE constraint failed" in str(error):
                raise ValueError("the owner account is already configured") from error
            raise

    def verify_credentials(self, username: str, password: str) -> str | None:
        normalized = username.strip()
        with self.store._connection() as connection:
            row = connection.execute(
                "SELECT username, password_hash FROM auth_account WHERE id = 1 AND username = ?",
                (normalized,),
            ).fetchone()
        if row is None:
            _verify_password(password, DUMMY_PASSWORD_HASH)
            return None
        if not _verify_password(password, row[1]):
            return None
        return row[0]

    def create_session(self, username: str) -> dict[str, str | int]:
        session_token = secrets.token_urlsafe(32)
        csrf_token = secrets.token_urlsafe(32)
        now = datetime.now(timezone.utc)
        expires = now + timedelta(hours=SESSION_HOURS)
        with self.store._connection() as connection:
            connection.execute("DELETE FROM auth_sessions WHERE expires_at <= ?", (now.isoformat(timespec="seconds"),))
            connection.execute(
                "INSERT INTO auth_sessions(token_hash, csrf_hash, created_at, expires_at) VALUES (?, ?, ?, ?)",
                (_token_hash(session_token), _token_hash(csrf_token), now.isoformat(timespec="seconds"),
                 expires.isoformat(timespec="seconds")),
            )
        return {"session_token": session_token, "csrf_token": csrf_token, "expires_in": SESSION_HOURS * 60 * 60,
                "username": username}

    def get_session(self, session_token: str | None) -> dict[str, str] | None:
        if not session_token:
            return None
        token_hash = _token_hash(session_token)
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        with self.store._connection() as connection:
            row = connection.execute(
                "SELECT username, csrf_hash FROM auth_sessions JOIN auth_account ON auth_account.id = 1 "
                "WHERE token_hash = ? AND expires_at > ?",
                (token_hash, now),
            ).fetchone()
        if row is None:
            return None
        return {"username": row[0], "csrf_hash": row[1], "token_hash": token_hash}

    def validate_csrf(self, session: dict[str, str] | None, csrf_token: str | None) -> bool:
        return bool(session and csrf_token and hmac.compare_digest(session["csrf_hash"], _token_hash(csrf_token)))

    def revoke_session(self, session_token: str | None) -> None:
        if not session_token:
            return
        with self.store._connection() as connection:
            connection.execute("DELETE FROM auth_sessions WHERE token_hash = ?", (_token_hash(session_token),))
