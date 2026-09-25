"""Application services for controlled, synthetic-data-only workflows."""
from sqlalchemy import select
from quran_educator.domain.models import AuthorizationContext
from quran_educator.infrastructure.db import AuditEntry, Circle, Group, Organization, SyntheticStudentRecord


class AuthorizationError(PermissionError):
    pass


class StudentService:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def create_synthetic_student(self, context: AuthorizationContext, identifier: str, display_name: str):
        if not context.can("student:create"):
            raise AuthorizationError("Missing permission: student:create")
        if not identifier.startswith("TEST-"):
            raise ValueError("Only synthetic identifiers are accepted in controlled development.")
        with self.session_factory() as session:
            organization = Organization(external_id="TEST_ORG_SERVICE", name="Synthetic Service Org", is_synthetic=True)
            session.add(organization)
            session.flush()
            circle = Circle(external_id="TEST_CIRCLE_SERVICE", name="Synthetic Service Circle", organization_id=organization.id)
            session.add(circle)
            session.flush()
            group = Group(external_id="TEST_GROUP_SERVICE", name="Synthetic Service Group", circle_id=circle.id)
            session.add(group)
            session.flush()
            record = SyntheticStudentRecord(
                external_id=identifier,
                display_name=display_name,
                group_id=group.id,
                is_synthetic=True,
            )
            session.add(record)
            session.add(AuditEntry(
                actor_id=context.user_id,
                action="CREATE_SYNTHETIC_STUDENT",
                entity_type="SyntheticStudentRecord",
                entity_id=identifier,
                outcome="SUCCESS",
            ))
            session.commit()
            return record.id

    def list_students(self, context: AuthorizationContext):
        if not context.can("student:read"):
            raise AuthorizationError("Missing permission: student:read")
        with self.session_factory() as session:
            return list(session.scalars(select(SyntheticStudentRecord)).all())


class ExportService:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def export_local(self, context: AuthorizationContext, output_path):
        if not context.can("export:local"):
            raise AuthorizationError("Missing permission: export:local")
        if not context.can("audit:write"):
            raise AuthorizationError("Export requires audit permission.")
        output_path.write_text("CONTROLLED DEVELOPMENT EXPORT\nSYNTHETIC DATA ONLY\n", encoding="utf-8")
        with self.session_factory() as session:
            session.add(AuditEntry(
                actor_id=context.user_id,
                action="LOCAL_EXPORT",
                entity_type="Export",
                entity_id=str(output_path),
                outcome="SUCCESS",
            ))
            session.commit()
