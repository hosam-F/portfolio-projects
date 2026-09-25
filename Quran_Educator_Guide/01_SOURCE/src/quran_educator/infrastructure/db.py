"""Controlled V1 data layer: local SQLite, synthetic-data-only foundation."""
from pathlib import Path
from datetime import datetime, timezone
from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Index, Integer, String, DateTime, create_engine, event
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class Organization(Base):
    __tablename__ = "organizations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    external_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    is_synthetic: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class Circle(Base):
    __tablename__ = "circles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id", ondelete="RESTRICT"), nullable=False)
    external_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    is_synthetic: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    __table_args__ = (Index("ix_circles_organization_id", "organization_id"),)


class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    circle_id: Mapped[int] = mapped_column(ForeignKey("circles.id", ondelete="RESTRICT"), nullable=False)
    external_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    is_synthetic: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class UserAccount(Base):
    __tablename__ = "user_accounts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    external_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(160), nullable=False)
    role: Mapped[str] = mapped_column(String(32), nullable=False)
    is_synthetic: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    __table_args__ = (CheckConstraint("role IN ('ADMIN','TEACHER','TRAINEE_TEACHER')", name="ck_user_role"),)


class RoleAssignment(Base):
    __tablename__ = "role_assignments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_accounts.id", ondelete="RESTRICT"), nullable=False)
    scope_type: Mapped[str] = mapped_column(String(32), nullable=False)
    scope_id: Mapped[str] = mapped_column(String(64), nullable=False)
    __table_args__ = (Index("ix_role_assignments_user_id", "user_id"),)


class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id", ondelete="RESTRICT"), nullable=False)
    external_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(160), nullable=False)
    is_synthetic: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    __table_args__ = (Index("ix_students_group_id", "group_id"),)


class Session(Base):
    __tablename__ = "sessions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id", ondelete="RESTRICT"), nullable=False)
    teacher_id: Mapped[int | None] = mapped_column(ForeignKey("user_accounts.id", ondelete="RESTRICT"), nullable=True)
    external_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    session_date: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="DRAFT")
    is_synthetic: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    __table_args__ = (CheckConstraint("status IN ('DRAFT','OPEN','CLOSED')", name="ck_session_status"),)


class Attendance(Base):
    __tablename__ = "attendance"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id", ondelete="RESTRICT"), nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="RESTRICT"), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    __table_args__ = (
        CheckConstraint("status IN ('PRESENT','ABSENT','LATE','EXCUSED')", name="ck_attendance_status"),
        Index("ux_attendance_session_student", "session_id", "student_id", unique=True),
    )


class Curriculum(Base):
    __tablename__ = "curricula"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    external_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    version: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="DRAFT")
    is_synthetic: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    __table_args__ = (CheckConstraint("status IN ('DRAFT','ACTIVE','ARCHIVED')", name="ck_curriculum_status"),)


class EducationalDomain(Base):
    __tablename__ = "educational_domains"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    curriculum_id: Mapped[int] = mapped_column(ForeignKey("curricula.id", ondelete="RESTRICT"), nullable=False)
    external_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class CurriculumUnit(Base):
    __tablename__ = "curriculum_units"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    domain_id: Mapped[int] = mapped_column(ForeignKey("educational_domains.id", ondelete="RESTRICT"), nullable=False)
    external_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class Project(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="RESTRICT"), nullable=False)
    external_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="PLANNED")
    __table_args__ = (CheckConstraint("status IN ('PLANNED','ACTIVE','COMPLETED','ARCHIVED')", name="ck_project_status"),)


class Source(Base):
    __tablename__ = "sources"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    external_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    provider: Mapped[str] = mapped_column(String(160), nullable=False)
    version: Mapped[str] = mapped_column(String(64), nullable=False)
    review_status: Mapped[str] = mapped_column(String(24), nullable=False, default="PENDING_REVIEW")
    is_synthetic: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    __table_args__ = (CheckConstraint("review_status IN ('UNKNOWN','PENDING_REVIEW','APPROVED','SUSPENDED','EXCLUDED')", name="ck_source_review_status"),)


class Provenance(Base):
    __tablename__ = "provenance"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id", ondelete="RESTRICT"), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(64), nullable=False)
    evidence: Mapped[str] = mapped_column(String(512), nullable=False)


class StudentAssignment(Base):
    __tablename__ = "student_assignments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="RESTRICT"), nullable=False)
    unit_id: Mapped[int] = mapped_column(ForeignKey("curriculum_units.id", ondelete="RESTRICT"), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="ASSIGNED")
    __table_args__ = (
        CheckConstraint("status IN ('ASSIGNED','STARTED','COMPLETED','CANCELLED')", name="ck_assignment_status"),
        Index("ux_student_unit_assignment", "student_id", "unit_id", unique=True),
    )


class MentorObservation(Base):
    __tablename__ = "mentor_observations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="RESTRICT"), nullable=False)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id", ondelete="RESTRICT"), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user_accounts.id", ondelete="RESTRICT"), nullable=False)
    observation_type: Mapped[str] = mapped_column(String(32), nullable=False)
    observation_text: Mapped[str] = mapped_column(String(512), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="ACTIVE")
    is_synthetic: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    __table_args__ = (CheckConstraint("status IN ('ACTIVE','ARCHIVED')", name="ck_observation_status"),)


class ProgressRecord(Base):
    __tablename__ = "progress_records"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="RESTRICT"), nullable=False)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id", ondelete="RESTRICT"), nullable=False)
    source_version: Mapped[str] = mapped_column(String(64), nullable=False)
    surah_id: Mapped[int] = mapped_column(Integer, nullable=False)
    ayah_start: Mapped[int] = mapped_column(Integer, nullable=False)
    ayah_end: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    completion: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    __table_args__ = (
        CheckConstraint("surah_id > 0 AND ayah_start > 0 AND ayah_end >= ayah_start", name="ck_progress_range"),
        CheckConstraint("completion >= 0 AND completion <= 100", name="ck_progress_completion"),
        CheckConstraint("status IN ('PLANNED','IN_PROGRESS','REVIEWED','MASTERED')", name="ck_progress_status"),
    )


class TeacherEvidence(Base):
    __tablename__ = "teacher_evidence"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("user_accounts.id", ondelete="RESTRICT"), nullable=False)
    evidence_type: Mapped[str] = mapped_column(String(32), nullable=False)
    description: Mapped[str] = mapped_column(String(512), nullable=False)
    review_status: Mapped[str] = mapped_column(String(24), nullable=False, default="PENDING_REVIEW")
    is_synthetic: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class AuditEntry(Base):
    __tablename__ = "audit_entries"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    actor_id: Mapped[str] = mapped_column(String(64), nullable=False)
    action: Mapped[str] = mapped_column(String(128), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(128), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(128), nullable=False)
    outcome: Mapped[str] = mapped_column(String(32), nullable=False)
    reason: Mapped[str | None] = mapped_column(String(512), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))


class BackupRecord(Base):
    __tablename__ = "backup_records"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    path: Mapped[str] = mapped_column(String(512), nullable=False)
    sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    verification_status: Mapped[str] = mapped_column(String(16), nullable=False)
    __table_args__ = (CheckConstraint("verification_status IN ('VERIFIED','REJECTED','PENDING')", name="ck_backup_status"),)


def create_session_factory(database_path: Path):
    database_path.parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(f"sqlite:///{database_path}", future=True, connect_args={"timeout": 30})

    @event.listens_for(engine, "connect")
    def _enable_foreign_keys(dbapi_connection, _connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    # SQLite schema creation is serialized across processes.  The exclusive
    # transaction prevents concurrent CREATE TABLE races during startup while
    # preserving the existing schema and model definitions.
    with engine.connect() as connection:
        connection.exec_driver_sql("BEGIN EXCLUSIVE")
        try:
            Base.metadata.create_all(connection)
            connection.commit()
        except Exception:
            connection.rollback()
            raise
    factory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    factory._quran_engine = engine
    return factory


# Historical compatibility alias: Student is the current authority; the old name is superseded.
SyntheticStudentRecord = Student

