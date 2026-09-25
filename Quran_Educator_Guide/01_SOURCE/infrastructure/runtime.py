from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RuntimeLayout:
    project_root: Path
    runtime_data_root: Path
    database_path: Path
    backup_root: Path
    report_root: Path
    log_root: Path
    config_root: Path
    temp_root: Path

    @staticmethod
    def default_runtime_root(project_root: Path) -> Path:
        """Return a writable root without coupling packaged runs to the source tree."""
        if getattr(sys, "frozen", False):
            app_data = os.environ.get("LOCALAPPDATA") or os.environ.get("APPDATA")
            if app_data:
                return Path(app_data) / "QuranEducatorGuide" / "controlled-runtime"
            return Path.home() / ".quran-educator-guide" / "controlled-runtime"
        return project_root / "data" / "runtime"

    @classmethod
    def for_project(cls, project_root: Path, runtime_data_root: Path | None = None) -> "RuntimeLayout":
        project_root = project_root.resolve()
        root = (runtime_data_root or cls.default_runtime_root(project_root)).resolve()
        return cls(project_root, root, root / "database.sqlite", root / "backups", root / "reports", root / "logs", root / "config", root / "tmp")

    def ensure(self) -> "RuntimeLayout":
        for path in (self.runtime_data_root, self.backup_root, self.report_root, self.log_root, self.config_root, self.temp_root):
            path.mkdir(parents=True, exist_ok=True)
        return self

    def as_dict(self) -> dict[str, str]:
        return {name: str(value) for name, value in self.__dict__.items()}
