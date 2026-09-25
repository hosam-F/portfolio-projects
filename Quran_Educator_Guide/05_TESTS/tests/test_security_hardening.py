import tempfile
import unittest
from pathlib import Path

from quran_educator.application.domain_services import (
    DomainAuthorizationError,
    DomainValidationError,
    ProgressService,
    StudentDomainService,
)
from quran_educator.domain.models import AuthorizationContext
from quran_educator.infrastructure.migrations import initialize_database
from quran_educator.infrastructure.quran_firewall import ContentBlockedError, QuranContentFirewall, SourceMetadata


class SecurityHardeningTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.factory = initialize_database(Path(self.temp.name) / "security.sqlite")
        self.allowed = AuthorizationContext("TEST-USER-SEC", "TEACHER", frozenset({"student:create", "progress:write"}))
        self.denied = AuthorizationContext("TEST-USER-DENIED", "TRAINEE_TEACHER", frozenset())

    def tearDown(self):
        self.factory._quran_engine.dispose()

    def test_unauthorized_service_action_is_rejected_and_audited(self):
        with self.assertRaises(DomainAuthorizationError):
            StudentDomainService(self.factory).add_student(self.denied, 999, "TEST-STUDENT-SEC", "TEST DATA ONLY")
        with self.factory() as session:
            rows = session.query(__import__("quran_educator.infrastructure.db", fromlist=["AuditEntry"]).AuditEntry).all()
            self.assertTrue(any(row.outcome == "DENIED" for row in rows))

    def test_metadata_only_firewall_rejects_runtime_content(self):
        firewall = QuranContentFirewall(SourceMetadata("Synthetic Provider", "0-test", "local", "local", "V1 Reviewer"))
        with self.assertRaises(ContentBlockedError):
            firewall.mutate_runtime_text("synthetic placeholder")
        with self.assertRaises(ContentBlockedError):
            firewall.validate_synthetic_fixture({"content_type": "SYNTHETIC_QURAN_FIXTURE", "status": "TEST DATA ONLY", "text": "blocked"})

    def test_invalid_progress_range_is_rejected(self):
        with self.assertRaises(DomainValidationError):
            ProgressService(self.factory).record_progress(self.allowed, 1, 1, "0-test", 1, 4, 2, "IN_PROGRESS", completion=50)


if __name__ == "__main__":
    unittest.main()
