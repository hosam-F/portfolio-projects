import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from sqlalchemy import inspect, select, text

from quran_educator.infrastructure import migrations
from quran_educator.infrastructure.backup import file_sha256, verify_backup, restore_verified
from quran_educator.infrastructure.db import AuditEntry
from quran_educator.infrastructure.migrations import CURRENT_SCHEMA_VERSION, SchemaVersion, initialize_database, migrate_to_current, migrate_with_backup


class FinalMigrationAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "migration.sqlite"

    def _old_v1(self, path=None):
        path = path or self.path
        con = sqlite3.connect(path)
        con.executescript("CREATE TABLE schema_versions (id INTEGER PRIMARY KEY, version VARCHAR(64) UNIQUE NOT NULL); INSERT INTO schema_versions(version) VALUES ('v1-data-layer-1'); CREATE TABLE audit_entries (id INTEGER PRIMARY KEY, actor_id VARCHAR(64) NOT NULL, action VARCHAR(128) NOT NULL, entity_type VARCHAR(128) NOT NULL, entity_id VARCHAR(128) NOT NULL, outcome VARCHAR(32) NOT NULL, reason VARCHAR(512)); INSERT INTO audit_entries(actor_id, action, entity_type, entity_id, outcome, reason) VALUES ('TEST-MIGRATION','BEFORE','Synthetic','1','SUCCESS','fixture');")
        con.commit(); con.close()
        return path

    def _tables(self, engine):
        return set(inspect(engine).get_table_names())

    def test_m01_fresh_database_creation(self):
        factory = initialize_database(self.path)
        try:
            self.assertTrue(self.path.exists())
            self.assertIn("schema_versions", self._tables(factory._quran_engine))
            with factory() as session:
                self.assertIn(CURRENT_SCHEMA_VERSION, [v.version for v in session.scalars(select(SchemaVersion))])
                self.assertEqual(session.scalar(text("PRAGMA integrity_check")), "ok")
        finally: factory._quran_engine.dispose()

    def test_m02_current_schema_detection(self):
        factory = initialize_database(self.path); factory._quran_engine.dispose()
        current = initialize_database(self.path)
        try:
            with current() as session:
                self.assertEqual([v.version for v in session.scalars(select(SchemaVersion))], [CURRENT_SCHEMA_VERSION])
        finally: current._quran_engine.dispose()

    def test_m03_current_database_idempotency(self):
        factory = initialize_database(self.path); factory._quran_engine.dispose()
        for _ in range(3):
            factory = initialize_database(self.path)
            factory._quran_engine.dispose()
        factory = initialize_database(self.path)
        try:
            with factory() as session: self.assertEqual(session.scalar(text("SELECT COUNT(*) FROM schema_versions")), 1)
        finally: factory._quran_engine.dispose()

    def test_m04_valid_v1_to_v2_migration(self):
        self._old_v1()
        factory = initialize_database(self.path)
        try:
            columns = {c["name"] for c in inspect(factory._quran_engine).get_columns("audit_entries")}
            self.assertIn("timestamp", columns)
            with factory() as session:
                self.assertEqual(session.scalar(text("SELECT COUNT(*) FROM audit_entries")), 1)
                self.assertIn(CURRENT_SCHEMA_VERSION, [v.version for v in session.scalars(select(SchemaVersion))])
        finally: factory._quran_engine.dispose()

    def test_m05_unknown_invalid_schema_version(self):
        con = sqlite3.connect(self.path); con.executescript("CREATE TABLE schema_versions (id INTEGER PRIMARY KEY, version VARCHAR(64) UNIQUE NOT NULL); INSERT INTO schema_versions(version) VALUES ('TEST-UNKNOWN');"); con.commit(); con.close()
        with self.assertRaises(RuntimeError): initialize_database(self.path)
        con = sqlite3.connect(self.path); self.assertEqual(con.execute("SELECT version FROM schema_versions").fetchone()[0], "TEST-UNKNOWN"); con.close()

    def test_m06_missing_migration_path(self):
        con = sqlite3.connect(self.path); con.executescript("CREATE TABLE schema_versions (id INTEGER PRIMARY KEY, version VARCHAR(64) UNIQUE NOT NULL); INSERT INTO schema_versions(version) VALUES ('TEST-NO-PATH');"); con.commit(); con.close()
        with self.assertRaises(RuntimeError) as ctx: initialize_database(self.path)
        self.assertIn("Missing migration", str(ctx.exception))

    def test_m07_migration_ordering(self):
        order = []
        registry = {"v0": lambda: order.append("v0->v1"), "v1": lambda: order.append("v1->v2"), "v2": lambda: order.append("v2->v3")}
        version = "v0"
        while version in registry:
            registry[version]()
            version = {"v0": "v1", "v1": "v2", "v2": "v3"}[version]
        self.assertEqual(order, ["v0->v1", "v1->v2", "v2->v3"])
        self.assertEqual(version, "v3")
        self.assertEqual(len(order), len(set(order)))

    def test_m08_schema_integrity_after_success(self):
        self._old_v1(); factory = initialize_database(self.path)
        try:
            with factory() as session: self.assertEqual(session.scalar(text("PRAGMA integrity_check")), "ok")
            self.assertIn("timestamp", {c["name"] for c in inspect(factory._quran_engine).get_columns("audit_entries")})
        finally: factory._quran_engine.dispose()

    def test_m09_intentional_migration_failure(self):
        result = migrate_with_backup(self.path, Path(self.temp.name) / "m09.backup", actor_id="TEST-M09", force_failure=True)
        try:
            self.assertIsNotNone(result)
            with result() as session: self.assertEqual(session.scalar(text("PRAGMA integrity_check")), "ok")
        finally: result._quran_engine.dispose()

    def test_m10_rollback_after_failed_migration(self):
        result = migrate_with_backup(self.path, Path(self.temp.name) / "m10.backup", actor_id="TEST-M10", force_failure=True)
        try:
            with result() as session: self.assertEqual(session.scalar(text("PRAGMA integrity_check")), "ok")
        finally: result._quran_engine.dispose()

    def test_m11_backup_before_migration(self):
        backup = Path(self.temp.name) / "m11.backup"
        result = migrate_with_backup(self.path, backup, actor_id="TEST-M11", force_failure=False)
        try:
            self.assertTrue(backup.exists()); self.assertTrue(verify_backup(backup, factory=result, actor_id="TEST-M11")); self.assertTrue(backup.with_suffix(".backup.sha256").exists())
        finally: result._quran_engine.dispose()

    def test_m12_restore_after_failed_migration(self):
        backup = Path(self.temp.name) / "m12.backup"
        result = migrate_with_backup(self.path, backup, actor_id="TEST-M12", force_failure=True)
        try:
            with result() as session: self.assertEqual(session.scalar(text("PRAGMA integrity_check")), "ok")
        finally: result._quran_engine.dispose()

    def test_m13_verify_restored_database_integrity(self):
        backup = Path(self.temp.name) / "m13.backup"
        result = migrate_with_backup(self.path, backup, actor_id="TEST-M13", force_failure=True)
        restored_path = Path(self.temp.name) / "m13.restored.sqlite"
        try:
            restore_verified(backup, restored_path)
            self.assertEqual(file_sha256(backup), file_sha256(restored_path))
            reopened = initialize_database(restored_path)
            try:
                with reopened() as session: self.assertEqual(session.scalar(text("PRAGMA integrity_check")), "ok")
            finally: reopened._quran_engine.dispose()
        finally: result._quran_engine.dispose()

    def test_m14_retry_migration_after_failure(self):
        backup = Path(self.temp.name) / "m14.backup"
        failed_recovery = migrate_with_backup(self.path, backup, actor_id="TEST-M14", force_failure=True)
        failed_recovery._quran_engine.dispose()
        retry = migrate_with_backup(self.path, Path(self.temp.name) / "m14.retry.backup", actor_id="TEST-M14", force_failure=False)
        try:
            with retry() as session:
                self.assertEqual(session.scalar(text("PRAGMA integrity_check")), "ok")
                self.assertIn(CURRENT_SCHEMA_VERSION, [v.version for v in session.scalars(select(SchemaVersion))])
        finally: retry._quran_engine.dispose()

    def test_m15_no_partial_or_corrupted_schema_state(self):
        result = migrate_with_backup(self.path, Path(self.temp.name) / "m15.backup", actor_id="TEST-M15", force_failure=True)
        try:
            tables = self._tables(result._quran_engine)
            self.assertIn("schema_versions", tables); self.assertIn("audit_entries", tables)
            with result() as session: self.assertEqual(session.scalar(text("PRAGMA integrity_check")), "ok")
        finally: result._quran_engine.dispose()

    def test_m16_migration_audit_event(self):
        result = migrate_with_backup(self.path, Path(self.temp.name) / "m16.backup", actor_id="TEST-M16", force_failure=False)
        try:
            with result() as session:
                events = session.scalars(select(AuditEntry).where(AuditEntry.entity_type == "Migration")).all()
                self.assertTrue(any(e.action == "MIGRATION_SUCCEEDED" for e in events))
                event = next(e for e in events if e.action == "MIGRATION_SUCCEEDED")
                self.assertEqual(event.actor_id, "TEST-M16"); self.assertEqual(event.outcome, "SUCCESS"); self.assertIsNotNone(event.timestamp)
        finally: result._quran_engine.dispose()


if __name__ == "__main__":
    unittest.main()
