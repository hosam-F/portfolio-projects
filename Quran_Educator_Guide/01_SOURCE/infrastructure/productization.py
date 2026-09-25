from __future__ import annotations

import logging
from pathlib import Path

from quran_educator import __version__
from quran_educator.infrastructure.migrations import CURRENT_SCHEMA_VERSION
from quran_educator.infrastructure.runtime import RuntimeLayout


BUILD_STATUS = "controlled-development"
BUILD_ID = "local-synthetic"


def build_metadata() -> dict[str, str]:
    return {
        "application_name": "دليل المربي القرآني",
        "application_version": __version__,
        "schema_version": CURRENT_SCHEMA_VERSION,
        "build_id": BUILD_ID,
        "status": BUILD_STATUS,
    }


def configure_local_logging(layout: RuntimeLayout) -> logging.Logger:
    layout.ensure()
    logger = logging.getLogger("quran_educator")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.FileHandler(layout.log_root / "application.log", encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
        logger.addHandler(handler)
    return logger


def startup_contract(project_root: Path, runtime_root: Path | None = None) -> tuple[RuntimeLayout, dict[str, str]]:
    layout = RuntimeLayout.for_project(project_root, runtime_root).ensure()
    return layout, build_metadata()
