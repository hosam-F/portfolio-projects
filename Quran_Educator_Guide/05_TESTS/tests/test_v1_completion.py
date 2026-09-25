import tempfile
import unittest
from pathlib import Path

from quran_educator.application.domain_services import (
    CircleService,
    CurriculumService,
    DomainAuthorizationError,
    DomainValidationError,
    ProgressService,
    SessionService,
    StudentDomainService,
)
from quran_educator.domain.models import AuthorizationContext
from quran_educator.infrastructure.db import EducationalDomain, Organization, Source, UserAccount
from quran_educator.infrastructure.migrations import initialize_database


class V1CompletionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.factory = initialize_database(Path(self.temp.name) / "completion.sqlite")
        self.teacher = AuthorizationContext("TEST-TEACHER-127", "TEACHER", frozenset({
            "circle:create", "group:create", "student:create", "curriculum:create", "curriculum:update",
            "curriculum:activate", "curriculum:archive", "curriculum:assign", "session:create", "session:open",
            "session:close", "attendance:write", "progress:write", "audit:write",
        }))
        self.trainee = AuthorizationContext("TEST-TRAINEE-127", "TRAINEE_TEACHER", frozenset())
        with self.factory() as session:
            org = Organization(external_id="TEST-ORG-127", name="TEST DATA ONLY", is_synthetic=True)
            user = UserAccount(external_id="TEST-TEACHER-127", display_name="TEST DATA ONLY", role="TEACHER", is_synthetic=True)
            source = Source(external_id="TEST-SOURCE-127", provider="Synthetic Provider", version="0-test", is_synthetic=True)
            session.add_all([org, user, source])
            session.commit()
            self.org_id, self.teacher_id, self.source_id = org.id, user.id, source.id
        self.circle_id = CircleService(self.factory).create_circle(self.teacher, self.org_id, "TEST-CIRCLE-127", "TEST DATA ONLY")
        self.group_id = CircleService(self.factory).assign_group(self.teacher, self.circle_id, "TEST-GROUP-127", "TEST DATA ONLY")
        self.student_id = StudentDomainService(self.factory).add_student(self.teacher, self.group_id, "TEST-STUDENT-127", "TEST DATA ONLY")
        curriculum = CurriculumService(self.factory)
        self.curriculum_id = curriculum.create_curriculum(self.teacher, "TEST-CURRICULUM-127", "TEST CURRICULUM", "0-test")
        with self.factory() as session:
            domain = EducationalDomain(curriculum_id=self.curriculum_id, external_id="TEST-DOMAIN-127", name="TEST DATA ONLY")
            session.add(domain)
            session.flush()
            self.domain_id = domain.id
            session.commit()
        self.unit_id = curriculum.create_unit(self.teacher, self.domain_id, "TEST-UNIT-127", "TEST UNIT 001")
        self.curriculum_service = curriculum

    def tearDown(self):
        self.factory._quran_engine.dispose()

    def test_assignment_requires_active_curriculum_and_rejects_duplicate(self):
        with self.assertRaises(DomainValidationError):
            self.curriculum_service.assign_student(self.teacher, self.student_id, self.unit_id)
        self.curriculum_service.activate_curriculum(self.teacher, self.curriculum_id)
        self.curriculum_service.assign_student(self.teacher, self.student_id, self.unit_id)
        with self.assertRaises(Exception):
            self.curriculum_service.assign_student(self.teacher, self.student_id, self.unit_id)
        self.curriculum_service.archive_curriculum(self.teacher, self.curriculum_id)
        with self.assertRaises(DomainValidationError):
            self.curriculum_service.assign_student(self.teacher, self.student_id, self.unit_id)

    def test_assignment_requires_authorization(self):
        self.curriculum_service.activate_curriculum(self.teacher, self.curriculum_id)
        with self.assertRaises(DomainAuthorizationError):
            self.curriculum_service.assign_student(self.trainee, self.student_id, self.unit_id)

    def test_closed_session_rejects_attendance(self):
        session_service = SessionService(self.factory)
        session_id = session_service.create_session(self.teacher, self.group_id, self.teacher_id, "TEST-SESSION-127", "2099-01-01")
        session_service.open_session(self.teacher, session_id)
        session_service.record_attendance(self.teacher, session_id, self.student_id, "EXCUSED")
        session_service.close_session(self.teacher, session_id)
        with self.assertRaises(DomainValidationError):
            session_service.record_attendance(self.teacher, session_id, self.student_id, "PRESENT")

    def test_progress_boundary_values_and_invalid_values(self):
        service = ProgressService(self.factory)
        for value in (0, 1, 50, 99, 100):
            self.assertGreater(service.record_progress(self.teacher, self.student_id, self.source_id, "0-test", 1, 1, 2, "IN_PROGRESS", value), 0)
        for value in (-1, 101):
            with self.assertRaises(DomainValidationError):
                service.record_progress(self.teacher, self.student_id, self.source_id, "0-test", 1, 1, 2, "IN_PROGRESS", value)


if __name__ == "__main__":
    unittest.main()
