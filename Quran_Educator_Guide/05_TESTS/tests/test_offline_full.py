import socket
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from quran_educator.infrastructure.db import Organization
from quran_educator.infrastructure.migrations import initialize_database


class OfflineFullTests(unittest.TestCase):
    def test_local_workflow_does_not_open_network_connections(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        db_path = Path(temp.name) / "offline.sqlite"
        factory = initialize_database(db_path)
        with patch.object(socket, "create_connection", side_effect=AssertionError("network disabled")):
            with factory() as session:
                org = Organization(external_id="TEST-OFF-ORG", name="TEST DATA ONLY", is_synthetic=True)
                session.add(org)
                session.commit()
                org_id = org.id
        factory._quran_engine.dispose()
        reopened_factory = initialize_database(db_path)
        self.addCleanup(reopened_factory._quran_engine.dispose)
        with reopened_factory() as session:
            self.assertIsNotNone(session.get(Organization, org_id))

    def test_database_is_sqlite_file(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        db_path = Path(temp.name) / "offline.sqlite"
        factory = initialize_database(db_path)
        factory._quran_engine.dispose()
        self.assertTrue(db_path.exists())
        self.assertEqual(db_path.suffix, ".sqlite")


if __name__ == "__main__":
    unittest.main()
