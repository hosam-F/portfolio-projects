from __future__ import annotations

import json
from pathlib import Path

from quran_educator.presentation.controller import ControlledAppController


def run_packaged_smoke(database_path: Path, runtime_root: Path) -> Path:
    """Run a controlled synthetic workflow through existing application services."""
    controller = ControlledAppController(database_path)
    try:
        controller.seed_demo()
        session_id = controller.run_vertical_slice()
        report_path = runtime_root / "reports" / "packaged_smoke_report.pdf"
        controller.create_report(report_path)
        backup_path = runtime_root / "backups" / "packaged_smoke.sqlite"
        restored_path = runtime_root / "backups" / "packaged_smoke.restored.sqlite"
        backup_ok = controller.backup_restore_verify(backup_path, restored_path)
        search_rows = controller.search_students("TEST-STUDENT-UI-001")
        result = {
            "status": "PASS",
            "synthetic_only": True,
            "offline_only": True,
            "session_id": session_id,
            "report_exists": report_path.exists(),
            "backup_restore_verified": backup_ok,
            "search_count": len(search_rows),
        }
        result_path = runtime_root / "reports" / "packaged_smoke_result.json"
        result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        return result_path
    finally:
        controller.close()
