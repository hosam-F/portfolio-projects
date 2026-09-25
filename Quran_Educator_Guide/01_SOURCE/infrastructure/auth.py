from __future__ import annotations

import hashlib
import hmac
import secrets
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path


SCHEME = "scrypt"
SCRYPT_N = 2**14
SCRYPT_R = 8
SCRYPT_P = 1
KEY_LENGTH = 64
MAX_FAILURES = 5
LOCK_MINUTES = 15
SESSION_MINUTES = 60


@dataclass(frozen=True)
class AuthenticatedSession:
    token: str
    account_id: int
    username: str
    display_name: str
    role: str


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _hash_password(password: str, salt: bytes | None = None) -> str:
    if not isinstance(password, str) or len(password) < 10:
        raise ValueError("يجب أن تتكون كلمة المرور من عشرة أحرف على الأقل.")
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=SCRYPT_N, r=SCRYPT_R, p=SCRYPT_P, dklen=KEY_LENGTH)
    return f"{SCHEME}${SCRYPT_N}${SCRYPT_R}${SCRYPT_P}${salt.hex()}${digest.hex()}"


def _verify_password(password: str, encoded: str) -> bool:
    try:
        scheme, n, r, p, salt_hex, digest_hex = encoded.split("$", 5)
        if scheme != SCHEME:
            return False
        digest = hashlib.scrypt(password.encode("utf-8"), salt=bytes.fromhex(salt_hex), n=int(n), r=int(r), p=int(p), dklen=len(bytes.fromhex(digest_hex)))
        return hmac.compare_digest(digest.hex(), digest_hex)
    except (ValueError, TypeError):
        return False


class LocalAuthService:
    """مصادقة محلية للإنتاج؛ لا تُستخدم مع fixtures إلا في اختبارات معزولة."""

    def __init__(self, database_path: Path):
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_schema()

    def _connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        return connection

    @contextmanager
    def _managed_connection(self):
        connection = self._connect()
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def _ensure_schema(self) -> None:
        with self._managed_connection() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS auth_accounts (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL UNIQUE COLLATE NOCASE,
                    display_name TEXT NOT NULL,
                    role TEXT NOT NULL CHECK (role IN ('ADMIN','SUPERVISOR','TEACHER','REPORT_VIEWER')),
                    password_hash TEXT NOT NULL,
                    is_active INTEGER NOT NULL DEFAULT 1,
                    failed_attempts INTEGER NOT NULL DEFAULT 0,
                    locked_until TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS auth_sessions (
                    id INTEGER PRIMARY KEY,
                    account_id INTEGER NOT NULL REFERENCES auth_accounts(id) ON DELETE RESTRICT,
                    token_hash TEXT NOT NULL UNIQUE,
                    created_at TEXT NOT NULL,
                    expires_at TEXT NOT NULL,
                    revoked_at TEXT
                );
                CREATE TABLE IF NOT EXISTS auth_audit (
                    id INTEGER PRIMARY KEY,
                    account_id INTEGER,
                    username TEXT NOT NULL,
                    action TEXT NOT NULL,
                    outcome TEXT NOT NULL,
                    occurred_at TEXT NOT NULL,
                    FOREIGN KEY(account_id) REFERENCES auth_accounts(id) ON DELETE RESTRICT
                );
                CREATE INDEX IF NOT EXISTS ix_auth_sessions_account ON auth_sessions(account_id);
                CREATE INDEX IF NOT EXISTS ix_auth_audit_username ON auth_audit(username);
                """
            )

    def count_accounts(self) -> int:
        with self._managed_connection() as connection:
            row = connection.execute("SELECT COUNT(*) AS total FROM auth_accounts").fetchone()
            return int(row["total"])

    def create_account(self, username: str, display_name: str, password: str, role: str = "TEACHER") -> int:
        username = username.strip()
        display_name = display_name.strip()
        if not username or not display_name:
            raise ValueError("اسم المستخدم والاسم الظاهر مطلوبان.")
        if role not in {"ADMIN", "SUPERVISOR", "TEACHER", "REPORT_VIEWER"}:
            raise ValueError("الدور غير معتمد.")
        encoded = _hash_password(password)
        now = _now()
        with self._managed_connection() as connection:
            cursor = connection.execute(
                "INSERT INTO auth_accounts(username, display_name, role, password_hash, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                (username, display_name, role, encoded, now, now),
            )
            return int(cursor.lastrowid)

    def authenticate(self, username: str, password: str) -> AuthenticatedSession:
        username = username.strip()
        now = datetime.now(timezone.utc)
        with self._managed_connection() as connection:
            row = connection.execute("SELECT * FROM auth_accounts WHERE username = ?", (username,)).fetchone()
            if row is None:
                self._audit(connection, None, username, "LOGIN", "REJECTED")
                raise ValueError("بيانات الدخول غير صحيحة.")
            locked_until = datetime.fromisoformat(row["locked_until"]) if row["locked_until"] else None
            if not row["is_active"] or (locked_until and locked_until > now):
                self._audit(connection, row["id"], username, "LOGIN", "BLOCKED")
                raise ValueError("الحساب غير متاح حاليًا.")
            if not _verify_password(password, row["password_hash"]):
                failures = int(row["failed_attempts"]) + 1
                lock = (now + timedelta(minutes=LOCK_MINUTES)).isoformat() if failures >= MAX_FAILURES else None
                connection.execute("UPDATE auth_accounts SET failed_attempts = ?, locked_until = ?, updated_at = ? WHERE id = ?", (failures, lock, _now(), row["id"]))
                self._audit(connection, row["id"], username, "LOGIN", "REJECTED")
                raise ValueError("بيانات الدخول غير صحيحة.")
            token = secrets.token_urlsafe(32)
            token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
            created = _now()
            expires = (now + timedelta(minutes=SESSION_MINUTES)).isoformat()
            connection.execute("UPDATE auth_accounts SET failed_attempts = 0, locked_until = NULL, updated_at = ? WHERE id = ?", (_now(), row["id"]))
            connection.execute("INSERT INTO auth_sessions(account_id, token_hash, created_at, expires_at) VALUES (?, ?, ?, ?)", (row["id"], token_hash, created, expires))
            self._audit(connection, row["id"], username, "LOGIN", "SUCCESS")
            return AuthenticatedSession(token, row["id"], row["username"], row["display_name"], row["role"])

    def revoke_session(self, token: str) -> None:
        token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
        with self._managed_connection() as connection:
            connection.execute("UPDATE auth_sessions SET revoked_at = ? WHERE token_hash = ? AND revoked_at IS NULL", (_now(), token_hash))

    def validate_session(self, token: str) -> AuthenticatedSession | None:
        token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
        with self._managed_connection() as connection:
            row = connection.execute(
                "SELECT a.*, s.expires_at, s.revoked_at FROM auth_sessions s JOIN auth_accounts a ON a.id = s.account_id WHERE s.token_hash = ?",
                (token_hash,),
            ).fetchone()
            if row is None or row["revoked_at"] or datetime.fromisoformat(row["expires_at"]) <= datetime.now(timezone.utc) or not row["is_active"]:
                return None
            return AuthenticatedSession(token, row["id"], row["username"], row["display_name"], row["role"])

    @staticmethod
    def _audit(connection, account_id: int | None, username: str, action: str, outcome: str) -> None:
        connection.execute("INSERT INTO auth_audit(account_id, username, action, outcome, occurred_at) VALUES (?, ?, ?, ?, ?)", (account_id, username, action, outcome, _now()))
