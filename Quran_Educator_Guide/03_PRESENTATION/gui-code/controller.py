from pathlib import Path
from sqlalchemy import select
from quran_educator.application.domain_services import CircleService, CurriculumService, ObservationService, ProgressService, SessionService, StudentDomainService
from quran_educator.domain.models import AuthorizationContext
from quran_educator.infrastructure.backup import create_manual_backup, restore_verified, verify_backup
from quran_educator.application.query_services import SearchService
from quran_educator.infrastructure.db import (
    Attendance, AuditEntry, Circle, Curriculum, CurriculumUnit, EducationalDomain,
    Group, MentorObservation, Organization, ProgressRecord, Session as SessionEntity,
    Source, Student, StudentAssignment, UserAccount,
)
from quran_educator.infrastructure.migrations import initialize_database
from quran_educator.presentation.reporting import create_synthetic_status_report


class ControlledAppController:
    """Thin UI adapter; business rules remain in application services."""
    def __init__(self, database_path: Path):
        self.database_path = database_path
        self.factory = initialize_database(database_path)
        self.context = AuthorizationContext(
            "TEST-USER-UI-001", "TEACHER", frozenset({
                "circle:create", "group:create", "student:create", "student:update", "student:move", "student:deactivate", "curriculum:create", "curriculum:update",
                "curriculum:activate", "curriculum:assign", "session:create", "session:open", "session:close",
                "attendance:write", "progress:write", "observation:create", "audit:write",
            })
        )
        self.ids = {}
        self.search_service = SearchService(self.factory)

    def seed_demo(self):
        """Create or reuse the complete synthetic fixture without duplicate rows."""
        def existing(model, external_id):
            with self.factory() as session:
                return session.scalar(select(model).where(model.external_id == external_id))

        with self.factory() as session:
            org = session.scalar(select(Organization).where(Organization.external_id == "TEST-ORG-UI-001"))
            if org is None:
                org = Organization(external_id="TEST-ORG-UI-001", name="TEST DATA ONLY", is_synthetic=True)
                session.add(org)
            teacher = session.scalar(select(UserAccount).where(UserAccount.external_id == "TEST-USER-UI-001"))
            if teacher is None:
                teacher = UserAccount(external_id="TEST-USER-UI-001", display_name="TEST DATA ONLY", role="TEACHER", is_synthetic=True)
                session.add(teacher)
            source = session.scalar(select(Source).where(Source.external_id == "TEST-SOURCE-UI-001"))
            if source is None:
                source = Source(external_id="TEST-SOURCE-UI-001", provider="Synthetic Provider", version="0-test", review_status="PENDING_REVIEW", is_synthetic=True)
                session.add(source)
            session.commit()
            self.ids.update(org_id=org.id, teacher_id=teacher.id, source_id=source.id)

        circle_item = existing(Circle, "TEST-CIRCLE-UI-001")
        circle = circle_item.id if circle_item else CircleService(self.factory).create_circle(self.context, self.ids["org_id"], "TEST-CIRCLE-UI-001", "TEST DATA ONLY")
        group_item = existing(Group, "TEST-GROUP-UI-001")
        group = group_item.id if group_item else CircleService(self.factory).assign_group(self.context, circle, "TEST-GROUP-UI-001", "TEST DATA ONLY")
        student_item = existing(Student, "TEST-STUDENT-UI-001")
        student = student_item.id if student_item else StudentDomainService(self.factory).add_student(self.context, group, "TEST-STUDENT-UI-001", "TEST DATA ONLY")
        curriculum_service = CurriculumService(self.factory)
        curriculum_item = existing(Curriculum, "TEST-CURRICULUM-UI-001")
        curriculum = curriculum_item.id if curriculum_item else curriculum_service.create_curriculum(self.context, "TEST-CURRICULUM-UI-001", "TEST DATA ONLY", "0-test")
        with self.factory() as session:
            domain = session.scalar(select(EducationalDomain).where(EducationalDomain.external_id == "TEST-DOMAIN-UI-001"))
            if domain is None:
                domain = EducationalDomain(curriculum_id=curriculum, external_id="TEST-DOMAIN-UI-001", name="TEST DATA ONLY")
                session.add(domain)
                session.flush()
            domain_id = domain.id
            session.commit()
        unit_item = existing(CurriculumUnit, "TEST-UNIT-UI-001")
        unit = unit_item.id if unit_item else curriculum_service.create_unit(self.context, domain_id, "TEST-UNIT-UI-001", "TEST DATA ONLY")
        with self.factory() as session:
            curriculum_row = session.get(Curriculum, curriculum)
            if curriculum_row and curriculum_row.status == "DRAFT":
                curriculum_service.activate_curriculum(self.context, curriculum)
            assignment = session.scalar(select(StudentAssignment).where(StudentAssignment.student_id == student, StudentAssignment.unit_id == unit))
        if assignment is None:
            curriculum_service.assign_student(self.context, student, unit)
        self.ids.update(circle_id=circle, group_id=group, student_id=student, curriculum_id=curriculum, unit_id=unit)
        return self.ids

    def run_vertical_slice(self):
        if not self.ids:
            self.seed_demo()
        session_service = SessionService(self.factory)
        with self.factory() as session:
            existing_session = session.scalar(select(SessionEntity).where(SessionEntity.external_id == "TEST-SESSION-UI-001"))
        if existing_session is not None:
            self.ids["session_id"] = existing_session.id
            return existing_session.id
        session_id = session_service.create_session(self.context, self.ids["group_id"], self.ids["teacher_id"], "TEST-SESSION-UI-001", "2099-01-01")
        session_service.open_session(self.context, session_id)
        session_service.record_attendance(self.context, session_id, self.ids["student_id"], "PRESENT")
        ProgressService(self.factory).record_progress(self.context, self.ids["student_id"], self.ids["source_id"], "0-test", 1, 1, 2, "IN_PROGRESS", completion=50)
        ObservationService(self.factory).create_observation(self.context, self.ids["student_id"], session_id, self.ids["teacher_id"], "PROGRESS", "TEST OBSERVATION ONLY")
        session_service.close_session(self.context, session_id)
        self.ids["session_id"] = session_id
        return session_id

    def list_records(self, section: str, limit: int = 200):
        """Read-only listing adapter for existing entities; no synthetic rows are invented."""
        bounded = max(1, min(limit, 500))
        with self.factory() as session:
            if section == "organization":
                rows = session.query(Organization).order_by(Organization.id.desc()).limit(bounded).all()
                return [f"{row.name} | {row.external_id} | {'نشط' if row.is_active else 'غير نشط'}" for row in rows]
            if section == "circle":
                rows = session.query(Circle).order_by(Circle.id.desc()).limit(bounded).all()
                return [f"{row.name} | {row.external_id} | المؤسسة #{row.organization_id}" for row in rows]
            if section == "group":
                rows = session.query(Group).order_by(Group.id.desc()).limit(bounded).all()
                return [f"{row.name} | {row.external_id} | الحلقة #{row.circle_id}" for row in rows]
            if section == "curriculum":
                rows = session.query(Curriculum).order_by(Curriculum.id.desc()).limit(bounded).all()
                return [f"{row.name} | {row.external_id} | الإصدار {row.version} | {row.status}" for row in rows]
            if section == "unit":
                rows = session.query(CurriculumUnit).order_by(CurriculumUnit.id.desc()).limit(bounded).all()
                return [f"{row.name} | {row.external_id} | المجال #{row.domain_id}" for row in rows]
            if section == "session":
                rows = session.query(SessionEntity).order_by(SessionEntity.id.desc()).limit(bounded).all()
                return [f"{row.external_id} | {row.session_date} | {row.status} | المجموعة #{row.group_id}" for row in rows]
            if section == "attendance":
                rows = session.query(Attendance).order_by(Attendance.id.desc()).limit(bounded).all()
                return [f"الجلسة #{row.session_id} | الطالب #{row.student_id} | {row.status}" for row in rows]
            if section == "progress":
                rows = session.query(ProgressRecord).order_by(ProgressRecord.id.desc()).limit(bounded).all()
                return [f"الطالب #{row.student_id} | نسبة الإنجاز {row.completion}% | {row.status}" for row in rows]
            if section == "observation":
                rows = session.query(MentorObservation).order_by(MentorObservation.id.desc()).limit(bounded).all()
                return [f"الطالب #{row.student_id} | الجلسة #{row.session_id} | {row.observation_type}" for row in rows]
            return []

    def student_options(self):
        with self.factory() as session:
            rows = session.query(Student).filter(Student.is_active.is_(True)).order_by(Student.display_name).all()
            return [(row.id, row.display_name, row.external_id, row.group_id) for row in rows]

    def add_student_from_ui(self, group_id: int, external_id: str, display_name: str):
        external_id = external_id.strip()
        display_name = display_name.strip()
        if not external_id.startswith("TEST-"):
            raise ValueError("لا يُسمح إلا بمعرّف طالب اصطناعي يبدأ بـ TEST-.")
        if not display_name:
            raise ValueError("اسم الطالب مطلوب.")
        return StudentDomainService(self.factory).add_student(self.context, group_id, external_id, display_name)

    def update_student_from_ui(self, student_id: int, display_name: str):
        display_name = display_name.strip()
        if not display_name:
            raise ValueError("اسم الطالب مطلوب.")
        return StudentDomainService(self.factory).update_student(self.context, student_id, display_name)

    def move_student_from_ui(self, student_id: int, new_group_id: int):
        return StudentDomainService(self.factory).move_student(self.context, student_id, new_group_id)

    def archive_student_from_ui(self, student_id: int):
        return StudentDomainService(self.factory).deactivate_student(self.context, student_id)

    def organization_options(self):
        with self.factory() as session:
            rows = session.query(Organization).filter(Organization.is_active.is_(True)).order_by(Organization.name).all()
            return [(row.id, row.name, row.external_id) for row in rows]

    def circle_options(self):
        with self.factory() as session:
            rows = session.query(Circle).filter(Circle.is_active.is_(True)).order_by(Circle.name).all()
            return [(row.id, row.name, row.external_id) for row in rows]

    def create_circle_from_ui(self, organization_id: int, external_id: str, name: str):
        external_id = external_id.strip()
        name = name.strip()
        if not external_id.startswith(("TEST-", "TEST_")):
            raise ValueError("لا يُسمح إلا بمعرّف اصطناعي يبدأ بـ TEST- أو TEST_.")
        if not name:
            raise ValueError("اسم الحلقة مطلوب.")
        return CircleService(self.factory).create_circle(self.context, organization_id, external_id, name)

    def create_group_from_ui(self, circle_id: int, external_id: str, name: str):
        external_id = external_id.strip()
        name = name.strip()
        if not external_id.startswith(("TEST-", "TEST_")):
            raise ValueError("لا يُسمح إلا بمعرّف اصطناعي يبدأ بـ TEST- أو TEST_.")
        if not name:
            raise ValueError("اسم المجموعة مطلوب.")
        return CircleService(self.factory).assign_group(self.context, circle_id, external_id, name)

    def dashboard_summary(self):
        """Return read-only local counts for the dashboard."""
        with self.factory() as session:
            return {
                "organizations": session.query(Organization).count(),
                "circles": session.query(Circle).count(),
                "groups": session.query(Group).count(),
                "students": session.query(Student).filter(Student.is_active.is_(True)).count(),
                "curricula": session.query(Curriculum).count(),
                "units": session.query(CurriculumUnit).filter(CurriculumUnit.is_active.is_(True)).count(),
                "sessions": session.query(SessionEntity).count(),
            }

    def synthetic_source_options(self):
        with self.factory() as session:
            rows = session.query(Source).filter(Source.is_synthetic.is_(True)).order_by(Source.id).all()
            return [(row.id, row.external_id, row.version) for row in rows]

    def open_session_options(self):
        with self.factory() as session:
            rows = session.query(SessionEntity).filter(SessionEntity.status == "OPEN").order_by(SessionEntity.id.desc()).all()
            return [(row.id, row.external_id, row.group_id) for row in rows]

    def create_progress_from_ui(self, student_id: int, source_id: int, source_version: str, surah_id: int, ayah_start: int, ayah_end: int, status: str, completion: int):
        status_map = {"مخطط": "PLANNED", "قيد التقدم": "IN_PROGRESS", "مراجع": "REVIEWED", "متقن": "MASTERED"}
        return ProgressService(self.factory).record_progress(
            self.context, student_id, source_id, source_version.strip(), surah_id, ayah_start, ayah_end,
            status_map.get(status, status), completion
        )

    def create_observation_from_ui(self, student_id: int, session_id: int, observation_type: str, observation_text: str):
        observation_text = observation_text.strip()
        if not observation_text:
            raise ValueError("نص الملاحظة مطلوب.")
        with self.factory() as session:
            author = session.query(UserAccount).filter(UserAccount.external_id == self.context.user_id).first()
            if author is None:
                author = session.query(UserAccount).filter(UserAccount.role == "TEACHER").order_by(UserAccount.id).first()
            if author is None:
                raise ValueError("لا يوجد مربي اصطناعي متاح للملاحظة.")
            author_id = author.id
        return ObservationService(self.factory).create_observation(self.context, student_id, session_id, author_id, observation_type.strip(), observation_text)

    def group_options(self):
        with self.factory() as session:
            rows = session.query(Group).order_by(Group.name, Group.id).all()
            return [(row.id, row.name, row.external_id, row.circle_id) for row in rows]

    def session_options(self):
        with self.factory() as session:
            rows = session.query(SessionEntity).order_by(SessionEntity.id.desc()).all()
            return [(row.id, row.external_id, row.session_date, row.status, row.group_id) for row in rows]

    def session_context(self, session_id: int):
        with self.factory() as session:
            item = session.get(SessionEntity, session_id)
            if item is None:
                return None
            group = session.get(Group, item.group_id)
            circle = session.get(Circle, group.circle_id) if group else None
            organization = session.get(Organization, circle.organization_id) if circle else None
            students = session.query(Student).filter(Student.group_id == item.group_id, Student.is_active.is_(True)).order_by(Student.display_name).all()
            attendance = session.query(Attendance).filter(Attendance.session_id == session_id).all()
            attendance_by_student = {row.student_id: row.status for row in attendance}
            return {"session": item, "group": group, "circle": circle, "organization": organization, "students": students, "attendance": attendance_by_student}

    def create_session_from_ui(self, group_id: int, external_id: str, session_date: str):
        external_id = external_id.strip()
        session_date = session_date.strip()
        if not external_id.startswith("TEST-"):
            raise ValueError("لا يُسمح إلا بمعرّف حصة اصطناعي يبدأ بـ TEST-.")
        if not session_date:
            raise ValueError("تاريخ الحصة مطلوب.")
        with self.factory() as session:
            teacher = session.query(UserAccount).filter(UserAccount.external_id == self.context.user_id).first()
            if teacher is None:
                teacher = session.query(UserAccount).filter(UserAccount.role == "TEACHER").order_by(UserAccount.id).first()
            if teacher is None:
                raise ValueError("لا يوجد مربي اصطناعي متاح للحصة.")
            teacher_id = teacher.id
        return SessionService(self.factory).create_session(self.context, group_id, teacher_id, external_id, session_date)

    def open_session_from_ui(self, session_id: int):
        return SessionService(self.factory).open_session(self.context, session_id)

    def close_session_from_ui(self, session_id: int):
        return SessionService(self.factory).close_session(self.context, session_id)

    def record_attendance_from_ui(self, session_id: int, student_id: int, status: str):
        status_map = {"حاضر": "PRESENT", "غائب": "ABSENT", "متأخر": "LATE", "بعذر": "EXCUSED"}
        normalized_status = status_map.get(status, status)
        return SessionService(self.factory).record_attendance(self.context, session_id, student_id, normalized_status)

    def student_context(self, student_id: int):
        """Read-only context assembled from existing relations; no synthetic rows are invented."""
        from quran_educator.infrastructure.db import StudentAssignment
        with self.factory() as session:
            student = session.get(Student, student_id)
            if student is None:
                return None
            group = session.get(Group, student.group_id)
            circle = session.get(Circle, group.circle_id) if group else None
            organization = session.get(Organization, circle.organization_id) if circle else None
            attendance = session.query(Attendance).filter(Attendance.student_id == student_id).order_by(Attendance.id.desc()).limit(20).all()
            progress = session.query(ProgressRecord).filter(ProgressRecord.student_id == student_id).order_by(ProgressRecord.id.desc()).limit(20).all()
            observations = session.query(MentorObservation).filter(MentorObservation.student_id == student_id).order_by(MentorObservation.id.desc()).limit(20).all()
            assignments = session.query(StudentAssignment).filter(StudentAssignment.student_id == student_id).order_by(StudentAssignment.id.desc()).limit(20).all()
            session_ids = [item.session_id for item in attendance]
            sessions = session.query(SessionEntity).filter(SessionEntity.id.in_(session_ids)).order_by(SessionEntity.id.desc()).all() if session_ids else []
            return {
                "student": student,
                "group": group,
                "circle": circle,
                "organization": organization,
                "attendance": attendance,
                "progress": progress,
                "observations": observations,
                "assignments": assignments,
                "sessions": sessions,
            }

    def audit_entries(self, limit: int = 100):
        """Return readable audit entries without inventing missing events."""
        bounded = max(1, min(limit, 500))
        with self.factory() as session:
            statement = select(AuditEntry).order_by(AuditEntry.id.desc()).limit(bounded)
            return list(session.scalars(statement))

    def report_filter_options(self):
        with self.factory() as session:
            organizations = session.query(Organization).order_by(Organization.name, Organization.id).all()
            circles = session.query(Circle).order_by(Circle.name, Circle.id).all()
            groups = session.query(Group).order_by(Group.name, Group.id).all()
            students = session.query(Student).filter(Student.is_active.is_(True)).order_by(Student.display_name, Student.id).all()
            sessions = session.query(SessionEntity).order_by(SessionEntity.id.desc()).all()
            return {
                "organizations": [(row.id, row.name, row.external_id) for row in organizations],
                "circles": [(row.id, row.name, row.external_id, row.organization_id) for row in circles],
                "groups": [(row.id, row.name, row.external_id, row.circle_id) for row in groups],
                "students": [(row.id, row.display_name, row.external_id, row.group_id) for row in students],
                "sessions": [(row.id, row.external_id, row.session_date, row.group_id) for row in sessions],
            }

    def contextual_report_context(self, organization_id=None, circle_id=None, group_id=None, student_id=None, session_id=None):
        options = self.report_filter_options()
        context = {}
        if organization_id:
            row = next((item for item in options["organizations"] if item[0] == organization_id), None)
            if row:
                context["المؤسسة"] = f"{row[1]} ({row[2]})"
        if circle_id:
            row = next((item for item in options["circles"] if item[0] == circle_id), None)
            if row:
                context["الحلقة"] = f"{row[1]} ({row[2]})"
        if group_id:
            row = next((item for item in options["groups"] if item[0] == group_id), None)
            if row:
                context["المجموعة"] = f"{row[1]} ({row[2]})"
        if student_id:
            row = next((item for item in options["students"] if item[0] == student_id), None)
            if row:
                context["الطالب"] = f"{row[1]} ({row[2]})"
        if session_id:
            row = next((item for item in options["sessions"] if item[0] == session_id), None)
            if row:
                context["الحصة"] = f"{row[1]} — {row[2]}"
        return context

    def create_report(self, output_path: Path, report_kind: str = "status", context: dict | None = None):
        if report_kind == "student":
            from quran_educator.presentation.reporting import create_student_report
            create_student_report(output_path, context=context)
        elif report_kind == "circle":
            from quran_educator.presentation.reporting import create_circle_report
            create_circle_report(output_path, context=context)
        elif report_kind == "session":
            from quran_educator.presentation.reporting import create_session_report
            create_session_report(output_path, context=context)
        else:
            create_synthetic_status_report(output_path, context=context)
        return output_path

    def search_students(self, query: str = "", group_id: int | None = None, limit: int = 100):
        return self.search_service.search_students(self.context, query, group_id, limit)

    def backup_restore_verify(self, backup_path: Path, restored_path: Path):
        create_manual_backup(self.database_path, backup_path, factory=self.factory, actor_id=self.context.user_id)
        restore_verified(backup_path, restored_path, factory=self.factory, actor_id=self.context.user_id)
        return verify_backup(backup_path, factory=self.factory, actor_id=self.context.user_id) and restored_path.read_bytes() == backup_path.read_bytes()

    def close(self):
        self.factory._quran_engine.dispose()
