from __future__ import annotations

from dataclasses import dataclass

from quran_educator.domain.models import AuthorizationContext
from quran_educator.infrastructure.auth import AuthenticatedSession


PERMISSIONS_BY_ROLE: dict[str, frozenset[str]] = {
    "ADMIN": frozenset({
        "accounts.manage", "organization.manage", "students.manage", "attendance.manage",
        "progress.manage", "reports.view", "audit.view", "backup.manage", "settings.manage",
    }),
    "SUPERVISOR": frozenset({
        "organization.manage", "students.manage", "attendance.manage", "progress.manage",
        "reports.view", "audit.view", "backup.manage",
    }),
    "TEACHER": frozenset({
        "students.manage", "attendance.manage", "progress.manage", "reports.view", "backup.manage",
    }),
    "REPORT_VIEWER": frozenset({"reports.view", "audit.view"}),
}


@dataclass(frozen=True)
class AuthorizationPolicy:
    """سياسة صلاحيات محلية صريحة؛ لا تمنح أي دور صلاحية غير معلنة."""

    def context_for(self, session: AuthenticatedSession) -> AuthorizationContext:
        permissions = PERMISSIONS_BY_ROLE.get(session.role, frozenset())
        return AuthorizationContext(user_id=str(session.account_id), role=session.role, permissions=permissions)

    def require(self, context: AuthorizationContext, permission: str) -> None:
        if not context.can(permission):
            raise PermissionError(f"لا يملك الحساب الدور المطلوب للعملية: {permission}")
