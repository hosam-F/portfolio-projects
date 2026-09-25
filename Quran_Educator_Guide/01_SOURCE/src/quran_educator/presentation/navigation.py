from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QApplication, QButtonGroup, QStyle, QPushButton, QSizePolicy, QStackedWidget, QVBoxLayout, QWidget


@dataclass(frozen=True)
class NavigationItem:
    route: str
    title: str
    tooltip: str


class PersistentNavigation(QWidget):
    """تنقل RTL دائم؛ لا يعرف Controller أو Domain أو قاعدة البيانات."""

    routeSelected = Signal(str)

    def __init__(self, items: list[NavigationItem], parent: QWidget | None = None):
        super().__init__(parent)
        self.items = items
        self.setObjectName("persistentNavigation")
        self.setAccessibleName("التنقل الدائم في دليل المربي القرآني")
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setMinimumWidth(220)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self._buttons: dict[str, QPushButton] = {}
        self._group = QButtonGroup(self)
        self._group.setExclusive(True)
        self._group.idClicked.connect(self._emit_route)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(7)
        icon_roles = {
            "dashboard": QStyle.StandardPixmap.SP_ComputerIcon,
            "organization": QStyle.StandardPixmap.SP_DirHomeIcon,
            "students": QStyle.StandardPixmap.SP_FileDialogDetailedView,
            "curriculum": QStyle.StandardPixmap.SP_DirOpenIcon,
            "attendance": QStyle.StandardPixmap.SP_DialogApplyButton,
            "progress_observation": QStyle.StandardPixmap.SP_BrowserReload,
            "reports": QStyle.StandardPixmap.SP_FileIcon,
            "audit": QStyle.StandardPixmap.SP_MessageBoxInformation,
            "backup_restore": QStyle.StandardPixmap.SP_DriveHDIcon,
        }
        for index, item in enumerate(items):
            button = QPushButton(item.title)
            standard_icon = icon_roles.get(item.route)
            if standard_icon is not None:
                button.setIcon(QApplication.style().standardIcon(standard_icon))
            button.setObjectName(f"nav_{item.route}")
            button.setCheckable(True)
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            button.setMinimumHeight(42)
            button.setToolTip(item.tooltip)
            button.setAccessibleName(f"الانتقال إلى {item.title}")
            button.setAccessibleDescription(item.tooltip)
            button.setProperty("route", item.route)
            self._group.addButton(button, index)
            self._buttons[item.route] = button
            layout.addWidget(button)
        layout.addStretch(1)

    def _emit_route(self, index: int) -> None:
        if 0 <= index < len(self.items):
            self.routeSelected.emit(self.items[index].route)

    def select(self, route: str) -> None:
        button = self._buttons.get(route)
        if button is not None:
            button.setChecked(True)

    def button(self, route: str) -> QPushButton | None:
        return self._buttons.get(route)


class ViewRouter:
    """يسجل View في QStackedWidget ويربط route بالتنقل."""

    def __init__(self, stack: QStackedWidget, navigation: PersistentNavigation, focus_view: Callable[[str], None]):
        self.stack = stack
        self.navigation = navigation
        self.focus_view = focus_view
        self._routes: dict[str, int] = {}
        navigation.routeSelected.connect(self.go)

    def register(self, route: str, view: QWidget) -> None:
        self._routes[route] = self.stack.addWidget(view)

    def go(self, route: str) -> None:
        index = self._routes.get(route)
        if index is None:
            return
        self.stack.setCurrentIndex(index)
        self.navigation.select(route)
        self.focus_view(route)

    def index(self, route: str) -> int | None:
        return self._routes.get(route)

    def routes(self) -> tuple[str, ...]:
        return tuple(self._routes)
