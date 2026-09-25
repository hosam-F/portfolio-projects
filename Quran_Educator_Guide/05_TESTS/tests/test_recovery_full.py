import tempfile
import unittest
from pathlib import Path

from quran_educator.infrastructure.backup import BackupIntegrityError, create_manual_backup, restore_verified, verify_backup
from quran_educator.infrastructure.db import Organization
from quran_educator.infrastructure.migrations import initialize_database


class RecoveryFullTests(unittest.TestCase):
    def test_healthy_backup_restore_and_restart(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        source = Path(temp.name) / "source.sqlite"
        backup = Path(temp.name) / "backup.sqlite"
        restored = Path(temp.name) / "restored.sqlite"
        factory = initialize_database(source)
        with factory() as session:
            org = Organization(external_id="TEST-REC-ORG", name="TEST DATA ONLY", is_synthetic=True)
            session.add(org)
            session.commit()
            org_id = org.id
        factory._quran_engine.dispose()
        create_manual_backup(source, backup)
        self.assertTrue(verify_backup(backup))
        restore_verified(backup, restored)
        reopened = initialize_database(restored)
        self.addCleanup(reopened._quran_engine.dispose)
        with reopened() as session:
            self.assertIsNotNone(session.get(Organization, org_id))

    def test_tampered_backup_is_rejected(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        source = Path(temp.name) / "source.sqlite"
        backup = Path(temp.name) / "backup.sqlite"
        restored = Path(temp.name) / "restored.sqlite"
        factory = initialize_database(source)
        with factory() as session:
            session.add(Organization(external_id="TEST-TAMPER-ORG", name="TEST DATA ONLY", is_synthetic=True))
            session.commit()
        factory._quran_engine.dispose()
        create_manual_backup(source, backup)
        backup.write_bytes(backup.read_bytes() + b"tamper")
        self.assertFalse(verify_backup(backup))
        with self.assertRaises(BackupIntegrityError):
            restore_verified(backup, restored)

    def test_missing_manifest_is_rejected(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        backup = Path(temp.name) / "missing.sqlite"
        backup.write_bytes(b"synthetic invalid backup")
        self.assertFalse(verify_backup(backup))

    def test_missing_backup_is_rejected(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.assertFalse(verify_backup(Path(temp.name) / "does-not-exist.sqlite"))

    def test_wrong_hash_is_rejected(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        backup = Path(temp.name) / "wrong-hash.sqlite"
        backup.write_bytes(b"synthetic backup")
        backup.with_suffix(backup.suffix + ".sha256").write_text("0" * 64, encoding="ascii")
        self.assertFalse(verify_backup(backup))


if __name__ == "__main__":
    unittest.main()
