"""Synthetic seed data only; never imports Quran text or real personal data."""
from quran_educator.infrastructure.db import (
    Attendance, Circle, Curriculum, CurriculumUnit, EducationalDomain, Group,
    Organization, Project, Provenance, Session, Source, Student, UserAccount,
)


def seed_synthetic_dataset(session_factory):
    with session_factory() as session:
        organization = Organization(external_id="TEST_ORG_001", name="Synthetic Organization", is_synthetic=True)
        session.add(organization)
        session.flush()
        circle = Circle(external_id="TEST_CIRCLE_001", name="Synthetic Circle", organization_id=organization.id)
        session.add(circle)
        session.flush()
        group = Group(external_id="TEST_GROUP_001", name="Synthetic Group", circle_id=circle.id)
        session.add(group)
        session.flush()
        teacher = UserAccount(external_id="TEST-TEACHER-001", display_name="Synthetic Teacher 001", role="TEACHER")
        trainee = UserAccount(external_id="TEST-TRAINEE-001", display_name="Synthetic Trainee 001", role="TRAINEE_TEACHER")
        session.add_all([teacher, trainee])
        student = Student(external_id="TEST-STUDENT-001", display_name="Synthetic Student 001", group_id=group.id)
        session.add(student)
        session.flush()
        lesson = Session(external_id="TEST-SESSION-001", session_date="2099-01-01", group_id=group.id)
        session.add(lesson)
        session.flush()
        session.add(Attendance(session_id=lesson.id, student_id=student.id, status="PRESENT"))
        curriculum = Curriculum(external_id="TEST-CURRICULUM-001", name="Synthetic Curriculum", version="0.1-test")
        session.add(curriculum)
        session.flush()
        domain = EducationalDomain(external_id="TEST-DOMAIN-001", name="Synthetic Domain", curriculum_id=curriculum.id)
        session.add(domain)
        session.flush()
        session.add(CurriculumUnit(external_id="TEST-UNIT-001", name="Synthetic Unit", domain_id=domain.id))
        session.add(Project(external_id="TEST-PROJECT-001", name="Synthetic Project", student_id=student.id, status="PLANNED"))
        source = Source(external_id="TEST-SOURCE-001", provider="Synthetic Provider", version="0-test", review_status="PENDING_REVIEW")
        session.add(source)
        session.flush()
        session.add(Provenance(source_id=source.id, entity_type="SyntheticCurriculum", entity_id="TEST-CURRICULUM-001", evidence="TEST DATA ONLY"))
        session.commit()
