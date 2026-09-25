import tempfile
import unittest
from pathlib import Path

from quran_educator.application.domain_services import DomainAuthorizationError, StudentDomainService
from quran_educator.domain.models import AuthorizationContext
from quran_educator.infrastructure.db import AuditEntry, Organization
from quran_educator.infrastructure.migrations import initialize_database
from quran_educator.infrastructure.quran_firewall import ContentBlockedError, QuranContentFirewall, SourceMetadata


class SecurityRegressionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.factory = initialize_database(Path(self.temp.name) / "security-regression.sqlite")
        with self.factory() as session:
            org = Organization(external_id="TEST-SEC-ORG-127", name="TEST DATA ONLY", is_synthetic=True)
            session.add(org)
            session.flush()
            # نحتفظ ببيئة منظمة فقط؛ اختبار الصلاحية يجب أن يرفض قبل فحص العلاقة.
            self.org_id = org.id
            session.commit()
        self.admin = AuthorizationContext("TEST-ADMIN-127", "ADMIN", frozenset({"student:create"}))
        self.teacher = AuthorizationContext("TEST-TEACHER-127", "TEACHER", frozenset({"student:create"}))
        self.trainee = AuthorizationContext("TEST-TRAINEE-127", "TRAINEE_TEACHER", frozenset())

    def tearDown(self):
        self.factory._quran_engine.dispose()

    def test_admin_and_teacher_allowed_path_requires_valid_group(self):
        for context in (self.admin, self.teacher):
            with self.assertRaises(Exception):
                StudentDomainService(self.factory).add_student(context, 999999, "TEST-STUDENT-SEC-127", "TEST DATA ONLY")

    def test_trainee_denied_and_audited(self):
        with self.assertRaises(DomainAuthorizationError):
            StudentDomainService(self.factory).add_student(self.trainee, 1, "TEST-STUDENT-SEC-127", "TEST DATA ONLY")
        with self.factory() as session:
            self.assertTrue(session.query(AuditEntry).filter_by(outcome="DENIED").count() >= 1)

    def test_firewall_regression(self):
        firewall = QuranContentFirewall(SourceMetadata("Synthetic Provider", "0-test", "local", "local", "V1 Reviewer"))
        with self.assertRaises(ContentBlockedError):
            firewall.import_runtime_content(Path("nonexistent.synthetic"))
        with self.assertRaises(ContentBlockedError):
            firewall.mutate_runtime_text("blocked synthetic runtime text")
        firewall.validate_synthetic_fixture({"content_type": "SYNTHETIC_QURAN_FIXTURE", "status": "TEST DATA ONLY"})


if __name__ == "__main__":
    unittest.main()
