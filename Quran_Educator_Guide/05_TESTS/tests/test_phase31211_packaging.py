from __future__ import annotations

import json
import os
import unittest
from pathlib import Path


ROOT = Path(os.environ.get("QURAN_PROJECT_ROOT", r"D:\quran"))
BUILD = ROOT / "build" / "phase-3.12.11"
PACKAGE = BUILD / "dist" / "QuranEducatorGuide"
EXE = PACKAGE / "QuranEducatorGuide.exe"
SMOKE = BUILD / "smoke-test" / "UserData" / "QuranEducatorGuide" / "controlled-runtime"


class Phase31211PackagingAcceptanceTests(unittest.TestCase):
    def test_pkg01_package_directory_exists(self):
        self.assertTrue(PACKAGE.is_dir())

    def test_pkg02_executable_exists(self):
        self.assertTrue(EXE.is_file())
        self.assertGreater(EXE.stat().st_size, 1_000_000)

    def test_pkg03_one_folder_has_internal_runtime(self):
        self.assertTrue((PACKAGE / "_internal").is_dir())

    def test_pkg04_smoke_result_exists(self):
        self.assertTrue((SMOKE / "reports" / "packaged_smoke_result.json").is_file())

    def test_pkg05_smoke_result_is_controlled_and_passed(self):
        result = json.loads((SMOKE / "reports" / "packaged_smoke_result.json").read_text(encoding="utf-8"))
        self.assertEqual(result["status"], "PASS")
        self.assertTrue(result["synthetic_only"])
        self.assertTrue(result["offline_only"])
        self.assertTrue(result["backup_restore_verified"])

    def test_pkg06_report_and_database_exist(self):
        self.assertTrue((SMOKE / "reports" / "packaged_smoke_report.pdf").is_file())
        self.assertTrue((SMOKE / "database.sqlite").is_file())

    def test_pkg07_runtime_data_is_outside_package(self):
        self.assertNotEqual(SMOKE.resolve(), PACKAGE.resolve())
        self.assertNotIn(str(PACKAGE.resolve()).lower(), str(SMOKE.resolve()).lower())

    def test_pkg08_package_excludes_development_directories(self):
        forbidden = {"tests", "checkpoints", "artifacts", ".venv", ".git", "docs"}
        names = {p.name.lower() for p in PACKAGE.rglob("*")}
        self.assertTrue(forbidden.isdisjoint(names))

    def test_pkg09_package_has_no_obvious_secret_files(self):
        forbidden_suffixes = {".env", ".pem", ".key", ".pfx", ".secret"}
        found = [p for p in PACKAGE.rglob("*") if p.is_file() and (p.name.lower() in forbidden_suffixes or p.suffix.lower() in forbidden_suffixes)]
        self.assertEqual(found, [])

    def test_pkg10_smoke_path_has_spaces_and_unicode(self):
        smoke_copy = BUILD / "smoke-test" / "Quran Package اختبار"
        self.assertTrue(smoke_copy.is_dir())
        self.assertIn(" ", str(smoke_copy))
        self.assertIn("اختبار", str(smoke_copy))


if __name__ == "__main__":
    unittest.main()
