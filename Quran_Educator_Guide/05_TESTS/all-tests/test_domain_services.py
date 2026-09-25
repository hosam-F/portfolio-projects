import tempfile
import unittest
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from quran_educator.application.domain_services import (
    CircleService, DomainAuthorizationError, DomainValidationError,
    ProgressService, ProjectService, SessionService, StudentDomainService, TeacherService,
)
from quran_educator.application.seed import seed_synthetic_dataset
from quran_educator.domain.models import AuthorizationContext
from quran_educator.infrastructure.backup import create_manual_backup, restore_verified, verify_backup
from quran_educator.infrastructure.db import AuditEntry, Circle, Group, Organization, Source, Student, UserAccount
from quran_educator.infrastructure.migrations import initialize_database


class DomainServiceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.factory = initialize_database(Path(self.temp.name) / "services.sqlite")
        seed_synthetic_dataset(self.factory)
        self.admin = AuthorizationContext("TEST-ADMIN-001", "ADMIN", frozenset({
            "circle:create", "circle:deactivate", "group:create", "student:create", "student:update", "student:move", "student:deactivate",
            "session:create", "session:close", "attendance:write", "curriculum:create", "curriculum:update", "project:create",
            "progress:write", "teacher:evidence", "audit:write",
        }))
        self.teacher = AuthorizationContext("TEST-TEACHER-001", "TEACHER", frozenset({
            "student:create", "session:create", "session:open", "session:close", "attendance:write", "progress:write", "teacher:evidence", "observation:create",
        }))
        self.trainee = AuthorizationContext("TEST-TRAINEE-001", "TRAINEE_TEACHER", frozenset({"student:read"}))

    def tearDown(self):
        self.factory._quran_engine.dispose()
        self.temp.cleanup()

    def ids(self):
        with self.factory() as session:
            org = session.scalar(select(Organization).where(Organization.external_id == "TEST_ORG_001"))
            circle = session.scalar(select(Circle).where(Circle.external_id == "TEST_CIRCLE_001"))
            group = session.scalar(select(Group).where(Group.external_id == "TEST_GROUP_001"))
            teacher = session.scalar(select(UserAccount).where(UserAccount.external_id == "TEST-TEACHER-001"))
            student = session.scalar(select(Student).where(Student.external_id == "TEST-STUDENT-001"))
            source = session.scalar(select(Source).where(Source.external_id == "TEST-SOURCE-001"))
            return org.id, circle.id, group.id, teacher.id, student.id, source.id

    def test_circle_and_student_services_happy_path_and_audit(self):
        org_id, circle_id, group_id, _, _, _ = self.ids()
        circle_service = CircleService(self.factory)
        new_circle_id = circle_service.create_circle(self.admin, org_id, "TEST_CIRCLE_002", "Synthetic Circle 002")
        new_group_id = circle_service.assign_group(self.admin, new_circle_id, "TEST_GROUP_002", "Synthetic Group 002")
        student_service = StudentDomainService(self.factory)
        student_id = student_service.add_student(self.admin, new_group_id, "TEST-STUDENT-002", "Synthetic Student 002")
        student_service.move_student(self.admin, student_id, group_id)
        student_service.update_student(self.admin, student_id, "Synthetic Student Updated")
        with self.factory() as session:
            actions = [row.action for row in session.scalars(select(AuditEntry)).all()]
        self.assertIn("CREATE", actions)
        self.assertIn("ASSIGN", actions)
        self.assertIn("UPDATE", actions)

    def test_student_invalid_and_unauthorized_cases(self):
        _, _, group_id, _, _, _ = self.ids()
        service = StudentDomainService(self.factory)
        with self.assertRaises(DomainAuthorizationError):
            service.add_student(self.trainee, group_id, "TEST-STUDENT-003", "Synthetic")
        with self.assertRaises(DomainValidationError):
            service.add_student(self.admin, 99999, "TEST-STUDENT-003", "Synthetic")
        service.add_student(self.admin, group_id, "TEST-STUDENT-003", "Synthetic")
        with self.assertRaises(IntegrityError):
            service.add_student(self.admin, group_id, "TEST-STUDENT-003", "Duplicate")

    def test_session_attendance_and_closed_session_rejection(self):
        _, _, group_id, teacher_id, student_id, _ = self.ids()
        service = SessionService(self.factory)
        session_id = service.create_session(self.teacher, group_id, teacher_id, "TEST-SESSION-002", "2099-01-02")
        service.open_session(self.teacher, session_id)
        service.record_attendance(self.teacher, session_id, student_id, "PRESENT")
        service.close_session(self.teacher, session_id)
        with self.assertRaises(DomainValidationError):
            service.record_attendance(self.teacher, session_id, student_id, "ABSENT")
        with self.assertRaises(DomainValidationError):
            service.record_attendance(self.teacher, session_id, student_id, "INVALID")

    def test_progress_allows_metadata_only_synthetic_source_and_rejects_range(self):
        _, _, _, _, student_id, source_id = self.ids()
        service = ProgressService(self.factory)
        item_id = service.record_progress(self.teacher, student_id, source_id, "0-test", 1, 1, 2, "REVIEWED")
        self.assertGreater(item_id, 0)
        with self.assertRaises(DomainValidationError):
            service.record_progress(self.teacher, student_id, source_id, "0-test", 1, 5, 2, "REVIEWED")

    def test_service_data_backup_compatibility(self):
        source_db = Path(self.temp.name) / "services.sqlite"
        backup = Path(self.temp.name) / "services.backup.sqlite"
        restored = Path(self.temp.name) / "services.restored.sqlite"
        self.factory._quran_engine.dispose()
        create_manual_backup(source_db, backup)
        self.assertTrue(verify_backup(backup))
        restore_verified(backup, restored)
        self.assertEqual(restored.read_bytes(), source_db.read_bytes())
        self.factory = initialize_database(source_db)

    def test_trainee_cannot_modify_sensitive_services(self):
        _, _, group_id, _, _, _ = self.ids()
        with self.assertRaises(DomainAuthorizationError):
            StudentDomainService(self.factory).add_student(self.trainee, group_id, "TEST-STUDENT-004", "Synthetic")
        with self.assertRaises(DomainAuthorizationError):
            TeacherService(self.factory).add_evidence(self.trainee, 1, "REFLECTION", "Synthetic")


if __name__ == "__main__":
    unittest.main()
