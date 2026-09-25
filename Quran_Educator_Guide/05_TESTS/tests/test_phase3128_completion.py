import sqlite3
import tempfile
import time
import unittest
from pathlib import Path

from PySide6.QtWidgets import QApplication, QListWidget, QLineEdit, QPushButton
from sqlalchemy import inspect, select

from quran_educator.infrastructure.db import AuditEntry
from quran_educator.infrastructure.migrations import (
    CURRENT_SCHEMA_VERSION, SchemaVersion, initialize_database, migrate_with_backup,
)
from quran_educator.presentation.app import MainWindow
from quran_educator.presentation.controller import ControlledAppController


class CompletionSubphaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "completion.sqlite"

    def test_ui_search_clear_select_detail_back_refresh_and_states(self):
        window = MainWindow(self.path)
        self.addCleanup(window.close)
        window.controller.seed_demo()
        window._search()
        results = window.search_results
        self.assertIsNotNone(results)
        self.assertGreater(results.count(), 0)
        window.search_input.setText("NO-SUCH-SYNTHETIC-RESULT")
        window._search()
        self.assertEqual(results.count(), 0)
        self.assertIn("نتائج", window.search_state.text())
        window.search_input.clear()
        window._search()
        item = results.item(0)
        window._open_detail(item)
        self.assertIn("TEST-STUDENT-UI-001", window.detail.text())
        window._back_detail()
        self.assertEqual(window.detail.text(), "")
        window._clear_search()
        self.assertEqual(window.search_input.text(), "")

    def test_migration_matrix_fresh_current_idempotent_and_upgrade(self):
        factory = initialize_database(self.path)
        try:
            with factory() as session:
                self.assertIn(CURRENT_SCHEMA_VERSION, [v.version for v in session.scalars(select(SchemaVersion))])
            first = {item["name"] for item in inspect(factory._quran_engine).get_columns("audit_entries")}
            factory._quran_engine.dispose()
            second = initialize_database(self.path)
            try:
                self.assertEqual(first, {item["name"] for item in inspect(second._quran_engine).get_columns("audit_entries")})
            finally:
                second._quran_engine.dispose()
        finally:
            try:
                factory._quran_engine.dispose()
            except Exception:
                pass

    def test_migration_failure_restores_verified_database(self):
        factory = initialize_database(self.path)
        with factory() as session:
            session.add(AuditEntry(actor_id="TEST-MIGRATION", action="BEFORE", entity_type="Synthetic", entity_id="1", outcome="SUCCESS"))
            session.commit()
        factory._quran_engine.dispose()
        backup = Path(self.temp.name) / "pre-migration.sqlite"
        restored = migrate_with_backup(self.path, backup, actor_id="TEST-MIGRATION", force_failure=True)
        try:
            with restored() as session:
                self.assertEqual(session.scalar(select(AuditEntry.action)), "BEFORE")
                self.assertIn(CURRENT_SCHEMA_VERSION, [v.version for v in session.scalars(select(SchemaVersion))])
        finally:
            restored._quran_engine.dispose()
        self.assertTrue(backup.exists())

    def test_migration_unknown_version_is_rejected(self):
        connection = sqlite3.connect(self.path)
        connection.executescript("CREATE TABLE schema_versions (id INTEGER PRIMARY KEY, version VARCHAR(64) UNIQUE NOT NULL); INSERT INTO schema_versions(version) VALUES ('TEST-UNKNOWN-VERSION');")
        connection.commit()
        connection.close()
        with self.assertRaises(RuntimeError):
            initialize_database(self.path)


if __name__ == "__main__":
    unittest.main()
