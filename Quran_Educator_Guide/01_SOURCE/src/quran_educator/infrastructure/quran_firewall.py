"""Quran content firewall for controlled synthetic-data development."""
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path


class ContentBlockedError(RuntimeError):
    pass


@dataclass(frozen=True)
class SourceMetadata:
    provider: str
    version: str
    license_url: str
    source_url: str
    reviewer: str
    sha256: str | None = None


class QuranContentFirewall:
    """Allows contracts and synthetic fixtures, never real Quran runtime content."""

    CONTENT_GATE = "NO-GO"

    def __init__(self, metadata: SourceMetadata):
        self.metadata = metadata

    def verify_file_hash(self, path: Path, expected_sha256: str) -> bool:
        digest = sha256(path.read_bytes()).hexdigest()
        return digest.lower() == expected_sha256.lower()

    def import_runtime_content(self, _path: Path):
        raise ContentBlockedError(
            "CONTENT_GATE=NO-GO: Quran runtime import is blocked in controlled development."
        )

    def mutate_runtime_text(self, _value: str):
        raise ContentBlockedError(
            "Quran runtime text is read-only and unavailable in synthetic development."
        )

    @staticmethod
    def validate_synthetic_fixture(fixture: dict) -> None:
        if fixture.get("content_type") != "SYNTHETIC_QURAN_FIXTURE":
            raise ContentBlockedError("Fixture must be explicitly marked TEST DATA ONLY.")
        if fixture.get("status") != "TEST DATA ONLY":
            raise ContentBlockedError("Synthetic Quran fixture status is invalid.")
        if "text" in fixture:
            raise ContentBlockedError("Synthetic fixture must not contain Quran text.")
