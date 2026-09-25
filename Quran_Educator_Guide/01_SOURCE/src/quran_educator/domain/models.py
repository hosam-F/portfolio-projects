"""Domain value objects and policy models for the controlled V1 foundation."""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class SourceStatus(str, Enum):
    UNKNOWN = "UNKNOWN"
    PENDING_REVIEW = "PENDING_REVIEW"
    APPROVED = "APPROVED"
    SUSPENDED = "SUSPENDED"
    EXCLUDED = "EXCLUDED"


class ContentGate(str, Enum):
    TEST_DATA_ONLY = "TEST_DATA_ONLY"
    CONTENT_BLOCKED = "CONTENT_BLOCKED"


@dataclass(frozen=True)
class SyntheticStudent:
    identifier: str
    display_name: str
    synthetic: bool = True


@dataclass(frozen=True)
class QuranSourceContract:
    provider: str
    version: str
    license_url: str
    sha256: Optional[str]
    reviewer: str
    status: SourceStatus
    content_gate: ContentGate = ContentGate.CONTENT_BLOCKED

    def is_runtime_eligible(self) -> bool:
        """Real Quran content is never eligible in the controlled foundation."""
        return False


@dataclass(frozen=True)
class AuthorizationContext:
    user_id: str
    role: str
    permissions: frozenset[str]

    def can(self, permission: str) -> bool:
        return permission in self.permissions
