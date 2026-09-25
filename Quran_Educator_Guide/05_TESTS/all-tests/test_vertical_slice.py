import tempfile
import unittest
from pathlib import Path
from sqlalchemy import select

from quran_educator.application.domain_services import (
    DomainValidationError,
    CircleService, CurriculumService, ObservationService, ProgressService,
    SessionService, StudentDomainService,
)
from quran_educator.domain.models import AuthorizationContext
from quran_educator.infrastructure.backup import create_manual_backup, restore_verified, verify_backup
from quran_educator.infrastructure.db import (
    AuditEntry, Circle, Curriculum, EducationalDomain, Group, Organization, Source, Student, UserAccount,
)
from quran_educator.infrastructure.migrations import initialize_database


class VerticalSliceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp.name) / "vertical.sqlite"
        self.factory = initialize_database(self.db_path)
        self.ctx = AuthorizationContext("TEST-USER-001", "TEACHER", frozenset({
            "circle:create", "group:create", "student:create", "curriculum:create", "curriculum:update",
            "curriculum:activate", "curriculum:archive", "curriculum:assign", "session:create", "session:open", "session:close",
            "attendance:write", "progress:write", "observation:create", "audit:write",
        }))

    def tearDown(self):
        self.factory._quran_engine.dispose()
        self.temp.cleanup()

    def test_curriculum_assignment_and_closed_observation_boundaries(self):
        with self.factory() as session:
            org = Organization(external_id="TEST-ORG-BOUNDARY", name="TEST DATA ONLY", is_synthetic=True)
            teacher = UserAccount(external_id="TEST-USER-BOUNDARY", display_name="TEST DATA ONLY", role="TEACHER", is_synthetic=True)
            session.add_all([org, teacher])
            session.commit()
            org_id, teacher_id = org.id, teacher.id
        circle_id = CircleService(self.factory).create_circle(self.ctx, org_id, "TEST-CIRCLE-BOUNDARY", "TEST DATA ONLY")
        group_id = CircleService(self.factory).assign_group(self.ctx, circle_id, "TEST-GROUP-BOUNDARY", "TEST DATA ONLY")
        student_id = StudentDomainService(self.factory).add_student(self.ctx, group_id, "TEST-STUDENT-BOUNDARY", "TEST DATA ONLY")
        curriculum_service = CurriculumService(self.factory)
        curriculum_id = curriculum_service.create_curriculum(self.ctx, "TEST-CURRICULUM-BOUNDARY", "TEST DATA ONLY", "0-test")
        with self.factory() as session:
            domain = EducationalDomain(curriculum_id=curriculum_id, external_id="TEST-DOMAIN-BOUNDARY", name="TEST DATA ONLY")
            session.add(domain)
            session.flush()
            domain_id = domain.id
            source = Source(external_id="TEST-SOURCE-BOUNDARY", provider="Synthetic Provider", version="0-test", review_status="PENDING_REVIEW", is_synthetic=True)
            session.add(source)
            session.commit()
            source_id = source.id
        unit_id = curriculum_service.create_unit(self.ctx, domain_id, "TEST-UNIT-BOUNDARY", "TEST DATA ONLY")
        with self.assertRaises(DomainValidationError):
            curriculum_service.assign_student(self.ctx, student_id, unit_id)
        curriculum_service.activate_curriculum(self.ctx, curriculum_id)
        curriculum_service.assign_student(self.ctx, student_id, unit_id)
        curriculum_service.archive_curriculum(self.ctx, curriculum_id)
        with self.assertRaises(DomainValidationError):
            curriculum_service.assign_student(self.ctx, student_id, unit_id)
        session_service = SessionService(self.factory)
        session_id = session_service.create_session(self.ctx, group_id, teacher_id, "TEST-SESSION-BOUNDARY", "2099-01-03")
        session_service.open_session(self.ctx, session_id)
        session_service.record_attendance(self.ctx, session_id, student_id, "PRESENT")
        ObservationService(self.factory).create_observation(self.ctx, student_id, session_id, teacher_id, "GENERAL", "TEST OBSERVATION ONLY")
        session_service.close_session(self.ctx, session_id)
        with self.assertRaises(DomainValidationError):
            ObservationService(self.factory).create_observation(self.ctx, student_id, session_id, teacher_id, "GENERAL", "TEST OBSERVATION ONLY")

    def test_complete_synthetic_vertical_slice_backup_restore_verify(self):
        with self.factory() as session:
            org = Organization(external_id="TEST-ORG-001", name="TEST DATA ONLY", is_synthetic=True)
            session.add(org)
            teacher = UserAccount(external_id="TEST-USER-001", display_name="TEST DATA ONLY", role="TEACHER", is_synthetic=True)
            session.add(teacher)
            source = Source(external_id="TEST-SOURCE-VS-001", provider="Synthetic Provider", version="0-test", review_status="PENDING_REVIEW", is_synthetic=True)
            session.add(source)
            session.commit()
            org_id = org.id
            teacher_id = teacher.id
            source_id = source.id

        circle_id = CircleService(self.factory).create_circle(self.ctx, org_id, "TEST-CIRCLE-001", "TEST DATA ONLY")
        group_id = CircleService(self.factory).assign_group(self.ctx, circle_id, "TEST-GROUP-001", "TEST DATA ONLY")
        student_id = StudentDomainService(self.factory).add_student(self.ctx, group_id, "TEST-STUDENT-001", "TEST DATA ONLY")

        curriculum_service = CurriculumService(self.factory)
        curriculum_id = curriculum_service.create_curriculum(self.ctx, "TEST-CURRICULUM-001", "TEST DATA ONLY", "0-test")
        with self.factory() as session:
            domain = EducationalDomain(curriculum_id=curriculum_id, external_id="TEST-DOMAIN-001", name="TEST DATA ONLY")
            session.add(domain)
            session.flush()
            domain_id = domain.id
            session.commit()
        unit_id = curriculum_service.create_unit(self.ctx, domain_id, "TEST-UNIT-001", "TEST DATA ONLY")
        curriculum_service.activate_curriculum(self.ctx, curriculum_id)
        assignment_id = curriculum_service.assign_student(self.ctx, student_id, unit_id)
        self.assertGreater(assignment_id, 0)

        session_service = SessionService(self.factory)
        session_id = session_service.create_session(self.ctx, group_id, teacher_id, "TEST-SESSION-001", "2099-01-01")
        session_service.open_session(self.ctx, session_id)
        session_service.record_attendance(self.ctx, session_id, student_id, "PRESENT")
        progress_id = ProgressService(self.factory).record_progress(self.ctx, student_id, source_id, "0-test", 1, 1, 2, "IN_PROGRESS", completion=50)
        observation_id = ObservationService(self.factory).create_observation(self.ctx, student_id, session_id, teacher_id, "PROGRESS", "TEST OBSERVATION ONLY")
        self.assertGreater(progress_id, 0)
        self.assertGreater(observation_id, 0)
        session_service.close_session(self.ctx, session_id)

        with self.factory() as session:
            audit_count = session.query(AuditEntry).count()
            self.assertGreaterEqual(audit_count, 10)
            self.assertEqual(session.scalar(select(Curriculum).where(Curriculum.id == curriculum_id)).status, "ACTIVE")
            self.assertEqual(session.scalar(select(Student).where(Student.id == student_id)).is_synthetic, True)

        self.factory._quran_engine.dispose()
        backup = Path(self.temp.name) / "vertical.backup.sqlite"
        restored = Path(self.temp.name) / "vertical.restored.sqlite"
        create_manual_backup(self.db_path, backup)
        self.assertTrue(verify_backup(backup))
        restore_verified(backup, restored)
        self.assertEqual(restored.read_bytes(), self.db_path.read_bytes())
        self.factory = initialize_database(self.db_path)


if __name__ == "__main__":
    unittest.main()
