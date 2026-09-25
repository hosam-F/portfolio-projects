"""Small V1 domain services with centralized authorization and audit behavior."""
from sqlalchemy import select
from quran_educator.domain.models import AuthorizationContext
from quran_educator.infrastructure.db import (
    Attendance, AuditEntry, Circle, Curriculum, CurriculumUnit, EducationalDomain,
    Group, Project, ProgressRecord, Session as SessionEntity, Source, Student,
    TeacherEvidence, UserAccount,
)


class DomainValidationError(ValueError):
    pass


class DomainAuthorizationError(PermissionError):
    pass


def _require(context: AuthorizationContext, permission: str):
    if not context.can(permission):
        raise DomainAuthorizationError(f"Missing permission: {permission}")


def _require_audited(factory, context, permission, action, entity_type, entity_id):
    if context.can(permission):
        return
    with factory() as session:
        _audit(session, context, action, entity_type, entity_id, "DENIED", f"Missing permission: {permission}")
        session.commit()
    raise DomainAuthorizationError(f"Missing permission: {permission}")


def _audit(session, context, action, entity_type, entity_id, outcome, reason=None):
    session.add(AuditEntry(
        actor_id=context.user_id,
        action=action,
        entity_type=entity_type,
        entity_id=str(entity_id),
        outcome=outcome,
        reason=reason,
    ))


class CircleService:
    def __init__(self, factory):
        self.factory = factory

    def create_circle(self, context, organization_id, external_id, name):
        _require(context, "circle:create")
        if not external_id.startswith("TEST_") and not external_id.startswith("TEST-"):
            raise DomainValidationError("Controlled development requires a TEST circle identifier.")
        with self.factory() as session:
            from quran_educator.infrastructure.db import Organization
            if session.get(Organization, organization_id) is None:
                raise DomainValidationError("Organization does not exist.")
            circle = Circle(organization_id=organization_id, external_id=external_id, name=name)
            session.add(circle)
            session.flush()
            _audit(session, context, "CREATE", "Circle", circle.id, "SUCCESS")
            session.commit()
            return circle.id

    def deactivate_circle(self, context, circle_id):
        _require(context, "circle:deactivate")
        with self.factory() as session:
            circle = session.get(Circle, circle_id)
            if circle is None:
                raise DomainValidationError("Circle does not exist.")
            circle.is_active = False
            _audit(session, context, "DEACTIVATE", "Circle", circle.id, "SUCCESS")
            session.commit()

    def assign_group(self, context, circle_id, external_id, name):
        _require(context, "group:create")
        with self.factory() as session:
            if session.get(Circle, circle_id) is None:
                raise DomainValidationError("Circle does not exist.")
            group = Group(circle_id=circle_id, external_id=external_id, name=name)
            session.add(group)
            session.flush()
            _audit(session, context, "ASSIGN", "Group", group.id, "SUCCESS")
            session.commit()
            return group.id


class StudentDomainService:
    def __init__(self, factory):
        self.factory = factory

    def add_student(self, context, group_id, external_id, display_name):
        _require_audited(self.factory, context, "student:create", "CREATE", "Student", external_id)
        if not external_id.startswith("TEST-"):
            raise DomainValidationError("Only synthetic student identifiers are accepted.")
        with self.factory() as session:
            if session.get(Group, group_id) is None:
                raise DomainValidationError("Group does not exist.")
            student = Student(group_id=group_id, external_id=external_id, display_name=display_name)
            session.add(student)
            session.flush()
            _audit(session, context, "CREATE", "Student", student.id, "SUCCESS")
            session.commit()
            return student.id

    def update_student(self, context, student_id, display_name):
        _require(context, "student:update")
        with self.factory() as session:
            student = session.get(Student, student_id)
            if student is None or not student.is_active:
                raise DomainValidationError("Student is missing or deactivated.")
            student.display_name = display_name
            _audit(session, context, "UPDATE", "Student", student.id, "SUCCESS")
            session.commit()

    def move_student(self, context, student_id, new_group_id):
        _require(context, "student:move")
        with self.factory() as session:
            student = session.get(Student, student_id)
            if student is None or not student.is_active:
                raise DomainValidationError("Student is missing or deactivated.")
            if session.get(Group, new_group_id) is None:
                raise DomainValidationError("Target group does not exist.")
            student.group_id = new_group_id
            _audit(session, context, "ASSIGN", "Student", student.id, "SUCCESS")
            session.commit()

    def deactivate_student(self, context, student_id):
        _require(context, "student:deactivate")
        with self.factory() as session:
            student = session.get(Student, student_id)
            if student is None:
                raise DomainValidationError("Student does not exist.")
            student.is_active = False
            _audit(session, context, "DEACTIVATE", "Student", student.id, "SUCCESS")
            session.commit()


class SessionService:
    def __init__(self, factory):
        self.factory = factory

    def create_session(self, context, group_id, teacher_id, external_id, session_date):
        _require(context, "session:create")
        with self.factory() as session:
            if session.get(Group, group_id) is None:
                raise DomainValidationError("Group does not exist.")
            teacher = session.get(UserAccount, teacher_id)
            if teacher is None or teacher.role not in ("ADMIN", "TEACHER"):
                raise DomainValidationError("Only ADMIN or TEACHER can own a session.")
            item = SessionEntity(group_id=group_id, teacher_id=teacher_id, external_id=external_id, session_date=session_date)
            session.add(item)
            session.flush()
            _audit(session, context, "CREATE", "Session", item.id, "SUCCESS")
            session.commit()
            return item.id

    def open_session(self, context, session_id):
        _require_audited(self.factory, context, "session:open", "OPEN_SESSION", "Session", session_id)
        with self.factory() as session:
            item = session.get(SessionEntity, session_id)
            if item is None or item.status != "DRAFT":
                raise DomainValidationError("Only a draft session can be opened.")
            item.status = "OPEN"
            _audit(session, context, "OPEN_SESSION", "Session", item.id, "SUCCESS")
            session.commit()

    def close_session(self, context, session_id):
        _require_audited(self.factory, context, "session:close", "CLOSE_SESSION", "Session", session_id)
        with self.factory() as session:
            item = session.get(SessionEntity, session_id)
            if item is None:
                raise DomainValidationError("Session does not exist.")
            if item.status == "CLOSED":
                raise DomainValidationError("Session is already closed.")
            item.status = "CLOSED"
            _audit(session, context, "UPDATE", "Session", item.id, "SUCCESS")
            session.commit()

    def record_attendance(self, context, session_id, student_id, status):
        _require_audited(self.factory, context, "attendance:write", "ATTENDANCE", "Attendance", f"{session_id}:{student_id}")
        if status not in {"PRESENT", "ABSENT", "LATE", "EXCUSED"}:
            raise DomainValidationError("Invalid attendance status.")
        with self.factory() as session:
            item = session.get(SessionEntity, session_id)
            student = session.get(Student, student_id)
            if item is None or student is None:
                raise DomainValidationError("Session or student does not exist.")
            if item.status != "OPEN":
                raise DomainValidationError("Only an open session can be modified.")
            if item.group_id != student.group_id:
                raise DomainValidationError("Student does not belong to the session group.")
            attendance = Attendance(session_id=session_id, student_id=student_id, status=status)
            session.add(attendance)
            session.flush()
            _audit(session, context, "ATTENDANCE", "Attendance", attendance.id, "SUCCESS")
            session.commit()
            return attendance.id


class CurriculumService:
    def __init__(self, factory):
        self.factory = factory

    def create_curriculum(self, context, external_id, name, version):
        _require(context, "curriculum:create")
        with self.factory() as session:
            item = Curriculum(external_id=external_id, name=name, version=version)
            session.add(item)
            session.flush()
            _audit(session, context, "CREATE", "Curriculum", item.id, "SUCCESS")
            session.commit()
            return item.id

    def activate_curriculum(self, context, curriculum_id):
        _require_audited(self.factory, context, "curriculum:activate", "ACTIVATE", "Curriculum", curriculum_id)
        with self.factory() as session:
            item = session.get(Curriculum, curriculum_id)
            if item is None or item.status != "DRAFT":
                raise DomainValidationError("Only a draft curriculum can be activated.")
            item.status = "ACTIVE"
            _audit(session, context, "ACTIVATE", "Curriculum", item.id, "SUCCESS")
            session.commit()

    def archive_curriculum(self, context, curriculum_id):
        _require_audited(self.factory, context, "curriculum:archive", "ARCHIVE", "Curriculum", curriculum_id)
        with self.factory() as session:
            item = session.get(Curriculum, curriculum_id)
            if item is None or item.status != "ACTIVE":
                raise DomainValidationError("Only an active curriculum can be archived.")
            item.status = "ARCHIVED"
            _audit(session, context, "ARCHIVE", "Curriculum", item.id, "SUCCESS")
            session.commit()

    def create_unit(self, context, domain_id, external_id, name):
        _require(context, "curriculum:update")
        with self.factory() as session:
            if session.get(EducationalDomain, domain_id) is None:
                raise DomainValidationError("Educational domain does not exist.")
            item = CurriculumUnit(domain_id=domain_id, external_id=external_id, name=name)
            session.add(item)
            session.flush()
            _audit(session, context, "CREATE", "CurriculumUnit", item.id, "SUCCESS")
            session.commit()
            return item.id

    def assign_student(self, context, student_id, unit_id):
        _require_audited(self.factory, context, "curriculum:assign", "ASSIGN", "StudentAssignment", f"{student_id}:{unit_id}")
        from quran_educator.infrastructure.db import StudentAssignment
        with self.factory() as session:
            student = session.get(Student, student_id)
            unit = session.get(CurriculumUnit, unit_id)
            curriculum = session.get(Curriculum, session.get(EducationalDomain, unit.domain_id).curriculum_id) if unit else None
            if student is None or unit is None or curriculum is None:
                raise DomainValidationError("Student, unit, and curriculum must exist.")
            if curriculum.status != "ACTIVE":
                raise DomainValidationError("Only an active curriculum can be assigned.")
            assignment = StudentAssignment(student_id=student_id, unit_id=unit_id)
            session.add(assignment)
            session.flush()
            _audit(session, context, "ASSIGN", "StudentAssignment", assignment.id, "SUCCESS")
            session.commit()
            return assignment.id


class ProjectService:
    def __init__(self, factory):
        self.factory = factory

    def create_project(self, context, student_id, external_id, name):
        _require(context, "project:create")
        with self.factory() as session:
            student = session.get(Student, student_id)
            if student is None or not student.is_active:
                raise DomainValidationError("Active student is required.")
            item = Project(student_id=student_id, external_id=external_id, name=name, status="PLANNED")
            session.add(item)
            session.flush()
            _audit(session, context, "CREATE", "Project", item.id, "SUCCESS")
            session.commit()
            return item.id


class ProgressService:
    def __init__(self, factory):
        self.factory = factory

    def record_progress(self, context, student_id, source_id, source_version, surah_id, ayah_start, ayah_end, status, completion=0):
        _require(context, "progress:write")
        if ayah_end < ayah_start or ayah_start < 1 or surah_id < 1 or completion < 0 or completion > 100:
            raise DomainValidationError("Invalid progress range or completion.")
        with self.factory() as session:
            student = session.get(Student, student_id)
            source = session.get(Source, source_id)
            if student is None or source is None or not source.is_synthetic:
                raise DomainValidationError("Only a synthetic source contract is permitted.")
            item = ProgressRecord(
                student_id=student_id,
                source_id=source_id,
                source_version=source_version,
                surah_id=surah_id,
                ayah_start=ayah_start,
                ayah_end=ayah_end,
                status=status,
                completion=completion,
            )
            session.add(item)
            session.flush()
            _audit(session, context, "PROGRESS", "ProgressRecord", item.id, "SUCCESS")
            session.commit()
            return item.id


class ObservationService:
    def __init__(self, factory):
        self.factory = factory

    def create_observation(self, context, student_id, session_id, author_id, observation_type, observation_text):
        _require_audited(self.factory, context, "observation:create", "OBSERVATION", "MentorObservation", f"{session_id}:{student_id}")
        from quran_educator.infrastructure.db import MentorObservation
        with self.factory() as session:
            student = session.get(Student, student_id)
            item_session = session.get(SessionEntity, session_id)
            author = session.get(UserAccount, author_id)
            if student is None or item_session is None or author is None:
                raise DomainValidationError("Student, session, and author must exist.")
            if item_session.status != "OPEN":
                raise DomainValidationError("Observation requires an open session.")
            if item_session.group_id != student.group_id:
                raise DomainValidationError("Student does not belong to the session group.")
            item = MentorObservation(student_id=student_id, session_id=session_id, author_id=author_id, observation_type=observation_type, observation_text=observation_text)
            session.add(item)
            session.flush()
            _audit(session, context, "OBSERVATION", "MentorObservation", item.id, "SUCCESS")
            session.commit()
            return item.id


class TeacherService:
    def __init__(self, factory):
        self.factory = factory

    def add_evidence(self, context, teacher_id, evidence_type, description):
        _require_audited(self.factory, context, "teacher:evidence", "CREATE", "TeacherEvidence", teacher_id)
        with self.factory() as session:
            teacher = session.get(UserAccount, teacher_id)
            if teacher is None or teacher.role not in ("ADMIN", "TEACHER", "TRAINEE_TEACHER"):
                raise DomainValidationError("Teacher account does not exist.")
            item = TeacherEvidence(teacher_id=teacher_id, evidence_type=evidence_type, description=description)
            session.add(item)
            session.flush()
            _audit(session, context, "CREATE", "TeacherEvidence", item.id, "SUCCESS")
            session.commit()
            return item.id
