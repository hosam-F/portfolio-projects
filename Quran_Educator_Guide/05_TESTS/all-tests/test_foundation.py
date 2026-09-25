import json
import tempfile
import unittest
from pathlib import Path

from quran_educator.application.services import AuthorizationError, ExportService, StudentService
from quran_educator.domain.models import AuthorizationContext
from quran_educator.infrastructure.backup import (
    BackupIntegrityError,
    create_manual_backup,
    restore_verified,
    verify_backup,
)
from quran_educator.infrastructure.db import create_session_factory
from quran_educator.presentation.reporting import create_synthetic_status_report
from quran_educator.infrastructure.quran_firewall import (
    ContentBlockedError,
    QuranContentFirewall,
    SourceMetadata,
)


ROOT = Path(__file__).resolve().parents[1]


class FoundationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.session_factory = create_session_factory(self.root / "synthetic.sqlite")
        self.admin = AuthorizationContext(
            user_id="TEST-TEACHER-001",
            role="TEST_ADMIN",
            permissions=frozenset({"student:create", "student:read", "export:local", "audit:write"}),
        )
        self.limited = AuthorizationContext(
            user_id="TEST-TRAINEE-001",
            role="TRAINEE_TEACHER",
            permissions=frozenset({"student:read"}),
        )

    def tearDown(self):
        self.session_factory._quran_engine.dispose()
        self.temp.cleanup()

    def test_synthetic_fixture_is_explicit_and_contains_no_quran_text(self):
        fixture = json.loads((ROOT / "data" / "synthetic" / "fixtures.json").read_text(encoding="utf-8"))
        self.assertEqual(fixture["fixture_status"], "TEST DATA ONLY")
        self.assertEqual(fixture["warning"], "NOT QURAN CONTENT")
        self.assertNotIn("text", fixture)

    def test_student_service_accepts_only_synthetic_identifiers(self):
        service = StudentService(self.session_factory)
        record_id = service.create_synthetic_student(self.admin, "TEST-STUDENT-001", "Synthetic Student 001")
        self.assertGreater(record_id, 0)
        self.assertEqual(len(service.list_students(self.admin)), 1)
        with self.assertRaises(ValueError):
            service.create_synthetic_student(self.admin, "REAL-001", "Any")

    def test_authorization_and_export_are_restricted(self):
        service = StudentService(self.session_factory)
        with self.assertRaises(AuthorizationError):
            service.create_synthetic_student(self.limited, "TEST-STUDENT-002", "Synthetic")
        export = ExportService(self.session_factory)
        with self.assertRaises(AuthorizationError):
            export.export_local(self.limited, self.root / "blocked.txt")
        export.export_local(self.admin, self.root / "allowed.txt")
        self.assertTrue((self.root / "allowed.txt").exists())

    def test_quran_firewall_blocks_runtime_content_and_validates_fixture(self):
        firewall = QuranContentFirewall(SourceMetadata(
            provider="Tanzil", version="1.1", license_url="https://tanzil.net/docs/Text_License",
            source_url="https://tanzil.net/download/", reviewer="م/ حسام الجرافي",
        ))
        QuranContentFirewall.validate_synthetic_fixture({
            "content_type": "SYNTHETIC_QURAN_FIXTURE", "status": "TEST DATA ONLY"
        })
        with self.assertRaises(ContentBlockedError):
            firewall.import_runtime_content(self.root / "quran.txt")
        with self.assertRaises(ContentBlockedError):
            QuranContentFirewall.validate_synthetic_fixture({
                "content_type": "SYNTHETIC_QURAN_FIXTURE", "status": "TEST DATA ONLY", "text": "blocked"
            })

    def test_pyside6_and_reportlab_foundation(self):
        from PySide6.QtWidgets import QApplication
        from reportlab.pdfgen import canvas
        self.assertIsNotNone(QApplication)
        self.assertIsNotNone(canvas)
        output = self.root / "status.pdf"
        create_synthetic_status_report(output)
        self.assertTrue(output.exists())
        self.assertGreater(output.stat().st_size, 0)

    def test_manual_backup_verify_and_reject_tampering(self):
        source = self.root / "source.sqlite"
        backup = self.root / "backup.sqlite"
        restored = self.root / "restored.sqlite"
        source.write_bytes(b"synthetic database")
        create_manual_backup(source, backup)
        self.assertTrue(verify_backup(backup))
        restore_verified(backup, restored)
        self.assertEqual(restored.read_bytes(), source.read_bytes())
        backup.write_bytes(b"tampered")
        self.assertFalse(verify_backup(backup))
        with self.assertRaises(BackupIntegrityError):
            restore_verified(backup, self.root / "rejected.sqlite")


if __name__ == "__main__":
    unittest.main()
