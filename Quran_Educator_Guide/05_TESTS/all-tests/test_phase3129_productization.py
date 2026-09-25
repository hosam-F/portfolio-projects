import json
import tempfile
import unittest
from pathlib import Path

from quran_educator.infrastructure.config import LocalConfig, load_local_config, save_local_config
from quran_educator.infrastructure.productization import build_metadata, startup_contract
from quran_educator.infrastructure.runtime import RuntimeLayout


class ProductizationTests(unittest.TestCase):
    def test_default_configuration_is_controlled(self):
        config = load_local_config()
        self.assertTrue(config.synthetic_only)
        self.assertTrue(config.offline_only)
        self.assertEqual(config.environment, "controlled-development")

    def test_configuration_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "config.json"
            save_local_config(path)
            self.assertEqual(load_local_config(path), LocalConfig())

    def test_invalid_configuration_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text(json.dumps({"synthetic_only": False}), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_local_config(path)

    def test_runtime_layout_is_explicit_and_creates_directories(self):
        with tempfile.TemporaryDirectory() as tmp:
            layout = RuntimeLayout.for_project(Path(tmp) / "project", Path(tmp) / "runtime").ensure()
            self.assertEqual(layout.project_root, (Path(tmp) / "project").resolve())
            self.assertTrue(layout.log_root.exists())
            self.assertTrue(layout.config_root.exists())
            self.assertNotEqual(layout.runtime_data_root, layout.project_root)

    def test_startup_contract_reports_version_and_schema(self):
        with tempfile.TemporaryDirectory() as tmp:
            layout, metadata = startup_contract(Path(tmp) / "project", Path(tmp) / "runtime")
            self.assertTrue(layout.database_path.parent.exists())
            self.assertEqual(metadata["status"], "controlled-development")
            self.assertIn("schema_version", metadata)
            self.assertIn("application_version", metadata)

    def test_metadata_is_not_release_claim(self):
        metadata = build_metadata()
        self.assertEqual(metadata["build_id"], "local-synthetic")
        self.assertNotIn("release", metadata["status"].lower())


if __name__ == "__main__":
    unittest.main()
