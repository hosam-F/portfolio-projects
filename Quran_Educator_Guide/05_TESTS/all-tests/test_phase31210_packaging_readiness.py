import tempfile
import unittest
from pathlib import Path

from quran_educator.infrastructure.config import load_local_config
from quran_educator.infrastructure.productization import build_metadata
from quran_educator.infrastructure.runtime import RuntimeLayout


class PackagingReadinessTests(unittest.TestCase):
    def test_runtime_layout_works_from_space_and_unicode_path(self):
        with tempfile.TemporaryDirectory(prefix="Quran Educator test ") as tmp:
            root = Path(tmp) / "مجلد اختبار"
            layout = RuntimeLayout.for_project(root / "project", root / "runtime").ensure()
            self.assertTrue(layout.database_path.parent.exists())
            self.assertTrue(layout.backup_root.exists())
            self.assertTrue(layout.report_root.exists())

    def test_normal_user_writable_runtime_simulation(self):
        with tempfile.TemporaryDirectory() as tmp:
            layout = RuntimeLayout.for_project(Path(tmp) / "project", Path(tmp) / "runtime").ensure()
            probe = layout.report_root / "write-test.txt"
            probe.write_text("SYNTHETIC TEST DATA ONLY", encoding="utf-8")
            self.assertEqual(probe.read_text(encoding="utf-8"), "SYNTHETIC TEST DATA ONLY")

    def test_controlled_config_has_no_external_mode(self):
        config = load_local_config()
        self.assertTrue(config.synthetic_only)
        self.assertTrue(config.offline_only)

    def test_build_metadata_is_development_only(self):
        metadata = build_metadata()
        self.assertEqual(metadata["build_id"], "local-synthetic")
        self.assertEqual(metadata["status"], "controlled-development")

    def test_no_packaged_executable_is_claimed(self):
        self.assertFalse(Path("D:/quran/build/controlled/dist/QuranEducator.exe").exists())


if __name__ == "__main__":
    unittest.main()
