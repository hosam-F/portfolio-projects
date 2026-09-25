"""Local deterministic search and filtering; authorization remains in the service layer."""
from sqlalchemy import or_, select
from quran_educator.application.domain_services import DomainAuthorizationError
from quran_educator.infrastructure.db import Curriculum, CurriculumUnit, Group, Student


class SearchService:
    def __init__(self, factory):
        self.factory = factory

    def _require_read(self, context):
        if "student:read" not in context.permissions and context.role not in {"ADMIN", "TEACHER"}:
            raise DomainAuthorizationError("Search is not authorized for this user.")

    def search_students(self, context, query: str = "", group_id: int | None = None, limit: int = 100):
        self._require_read(context)
        normalized = (query or "").strip()
        bounded = max(1, min(limit, 100))
        with self.factory() as session:
            statement = select(Student).order_by(Student.id).limit(bounded)
            if group_id is not None:
                statement = statement.where(Student.group_id == group_id)
            if normalized:
                pattern = f"%{normalized}%"
                statement = statement.where(or_(Student.external_id.ilike(pattern), Student.display_name.ilike(pattern)))
            return list(session.scalars(statement))

    def search_curricula(self, context, query: str = "", status: str | None = None, limit: int = 100):
        if context.role not in {"ADMIN", "TEACHER"} and "curriculum:read" not in context.permissions:
            raise DomainAuthorizationError("Curriculum search is not authorized for this user.")
        normalized = (query or "").strip()
        bounded = max(1, min(limit, 100))
        with self.factory() as session:
            statement = select(Curriculum).order_by(Curriculum.id).limit(bounded)
            if normalized:
                pattern = f"%{normalized}%"
                statement = statement.where(or_(Curriculum.external_id.ilike(pattern), Curriculum.name.ilike(pattern)))
            if status:
                statement = statement.where(Curriculum.status == status)
            return list(session.scalars(statement))

    def search_units(self, context, query: str = "", limit: int = 100):
        if context.role not in {"ADMIN", "TEACHER"} and "curriculum:read" not in context.permissions:
            raise DomainAuthorizationError("Unit search is not authorized for this user.")
        normalized = (query or "").strip()
        bounded = max(1, min(limit, 100))
        with self.factory() as session:
            statement = select(CurriculumUnit).order_by(CurriculumUnit.id).limit(bounded)
            if normalized:
                statement = statement.where(or_(CurriculumUnit.external_id.ilike(f"%{normalized}%"), CurriculumUnit.name.ilike(f"%{normalized}%")))
            return list(session.scalars(statement))
