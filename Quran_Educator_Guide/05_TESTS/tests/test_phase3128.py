import sqlite3
import tempfile
import unittest
from pathlib import Path

from sqlalchemy import inspect, select

from quran_educator.application.query_services import SearchService
from quran_educator.domain.models import AuthorizationContext
from quran_educator.infrastructure.backup import create_manual_backup, restore_verified, verify_backup
from quran_educator.infrastructure.db import AuditEntry, Circle, Group, Organization, Student
from quran_educator.infrastructure.migrations import CURRENT_SCHEMA_VERSION, initialize_database


class Phase3128Tests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "phase3128.sqlite"
        self.factory = initialize_database(self.path)
        self.context = AuthorizationContext("TEST-USER-3128", "TEACHER", frozenset({"student:read"}))
        with self.factory() as session:
            org = Organization(external_id="TEST-ORG-3128", name="TEST DATA ONLY", is_synthetic=True)
            session.add(org)
            session.flush()
            circle = Circle(organization_id=org.id, external_id="TEST-CIRCLE-3128", name="TEST DATA ONLY", is_synthetic=True)
            session.add(circle)
            session.flush()
            group = Group(circle_id=circle.id, external_id="TEST-GROUP-3128", name="TEST DATA ONLY", is_synthetic=True)
            session.add(group)
            session.flush()
            session.add_all([
                Student(group_id=group.id, external_id="TEST-STUDENT-ALPHA", display_name="Synthetic Alpha", is_synthetic=True),
                Student(group_id=group.id, external_id="TEST-STUDENT-BETA", display_name="Synthetic Beta", is_synthetic=True),
            ])
            session.commit()
            self.group_id = group.id

    def tearDown(self):
        self.factory._quran_engine.dispose()

    def test_search_empty_partial_exact_filter_and_bound(self):
        service = SearchService(self.factory)
        self.assertEqual(len(service.search_students(self.context)), 2)
        self.assertEqual(len(service.search_students(self.context, "alpha")), 1)
        self.assertEqual(len(service.search_students(self.context, "TEST-STUDENT-BETA", self.group_id, 1)), 1)
        self.assertEqual(len(service.search_students(self.context, "no-result")), 0)
        self.assertLessEqual(len(service.search_students(self.context, limit=500)), 100)

    def test_search_unauthorized_role_is_denied(self):
        service = SearchService(self.factory)
        denied = AuthorizationContext("TEST-TRAINEE-3128", "TRAINEE_TEACHER", frozenset())
        with self.assertRaises(Exception):
            service.search_students(denied, "Synthetic")

    def test_audit_timestamp_is_generated(self):
        with self.factory() as session:
            entry = AuditEntry(actor_id="TEST-ACTOR-3128", action="CREATE", entity_type="Synthetic", entity_id="1", outcome="SUCCESS")
            session.add(entry)
            session.commit()
            loaded = session.get(AuditEntry, entry.id)
            self.assertIsNotNone(loaded.timestamp)

    def test_backup_restore_verification_events_are_audited(self):
        backup = Path(self.temp.name) / "backup.sqlite"
        restored = Path(self.temp.name) / "restored.sqlite"
        create_manual_backup(self.path, backup, factory=self.factory, actor_id="TEST-ACTOR-3128")
        self.assertTrue(verify_backup(backup, factory=self.factory, actor_id="TEST-ACTOR-3128"))
        restore_verified(backup, restored, factory=self.factory, actor_id="TEST-ACTOR-3128")
        with self.factory() as session:
            actions = {row.action for row in session.scalars(select(AuditEntry)).all()}
            timestamps = [row.timestamp for row in session.scalars(select(AuditEntry)).all()]
        self.assertTrue({"BACKUP_STARTED", "BACKUP_SUCCEEDED", "VERIFY_SUCCEEDED", "RESTORE_STARTED", "RESTORE_SUCCEEDED"}.issubset(actions))
        self.assertTrue(all(item is not None for item in timestamps))

    def test_upgrade_from_previous_synthetic_schema(self):
        old_path = Path(self.temp.name) / "old.sqlite"
        connection = sqlite3.connect(old_path)
        connection.executescript("""
        CREATE TABLE schema_versions (id INTEGER PRIMARY KEY, version VARCHAR(64) UNIQUE NOT NULL);
        INSERT INTO schema_versions(version) VALUES ('v1-data-layer-1');
        CREATE TABLE audit_entries (id INTEGER PRIMARY KEY, actor_id VARCHAR(64) NOT NULL, action VARCHAR(128) NOT NULL, entity_type VARCHAR(128) NOT NULL, entity_id VARCHAR(128) NOT NULL, outcome VARCHAR(32) NOT NULL, reason VARCHAR(512));
        """)
        connection.commit()
        connection.close()
        upgraded = initialize_database(old_path)
        try:
            columns = {item["name"] for item in inspect(upgraded._quran_engine).get_columns("audit_entries")}
            self.assertIn("timestamp", columns)
            with upgraded() as session:
                versions = [row.version for row in session.scalars(select(__import__("quran_educator.infrastructure.migrations", fromlist=["SchemaVersion"]).SchemaVersion))]
                self.assertIn(CURRENT_SCHEMA_VERSION, versions)
        finally:
            upgraded._quran_engine.dispose()


if __name__ == "__main__":
    unittest.main()
