from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QScrollArea, QVBoxLayout, QWidget


@dataclass(frozen=True)
class ViewSpec:
    route: str
    title: str
    tooltip: str
    view_name: str


class BaseView(QFrame):
    """حاوية View مستقلة منطقيًا؛ لا تملك منطق المجال أو التخزين."""

    def __init__(self, host: QWidget, spec: ViewSpec, builder: Callable[[str], QWidget]):
        super().__init__(host)
        self.host = host
        self.spec = spec
        self.setObjectName(f"view_{spec.route}")
        self.setAccessibleName(f"واجهة {spec.title}")
        self.setProperty("route", spec.route)
        self.setProperty("viewName", spec.view_name)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        content = builder(spec.title)
        content.setObjectName(f"content_{spec.route}")
        content_scroll = QScrollArea()
        content_scroll.setObjectName("viewScroll")
        content_scroll.setProperty("route", spec.route)
        content_scroll.setAccessibleName(f"محتوى واجهة {spec.title} القابل للتمرير")
        content_scroll.setWidgetResizable(True)
        content_scroll.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        content_scroll.setFrameShape(QFrame.Shape.NoFrame)
        content_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        content_scroll.setWidget(content)
        layout.addWidget(content_scroll)

    def content_scroll_area(self) -> QScrollArea | None:
        return self.findChild(QScrollArea)

    def focus_initial(self) -> None:
        scroll = self.content_scroll_area()
        if scroll is not None:
            scroll.setFocus(Qt.FocusReason.OtherFocusReason)
            return
        self.setFocus(Qt.FocusReason.OtherFocusReason)


class DashboardView(BaseView):
    pass


class OrganizationView(BaseView):
    pass


class StudentsView(BaseView):
    pass


class CurriculumView(BaseView):
    pass


class AttendanceView(BaseView):
    pass


class ProgressObservationView(BaseView):
    pass


class ReportsView(BaseView):
    pass


class AuditView(BaseView):
    pass


class BackupRestoreView(BaseView):
    pass
