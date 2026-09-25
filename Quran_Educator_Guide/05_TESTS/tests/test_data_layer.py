import tempfile
import unittest
from pathlib import Path
from sqlalchemy import event, inspect, select
from sqlalchemy.exc import IntegrityError

from quran_educator.application.seed import seed_synthetic_dataset
from quran_educator.infrastructure.db import Attendance, Base, Circle, Student, UserAccount
from quran_educator.infrastructure.migrations import CURRENT_SCHEMA_VERSION, SchemaVersion, initialize_database


class DataLayerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.factory = initialize_database(self.root / "fresh.sqlite")

    def tearDown(self):
        self.factory._quran_engine.dispose()
        self.temp.cleanup()

    def test_fresh_schema_and_migration_version(self):
        tables = set(inspect(self.factory._quran_engine).get_table_names())
        self.assertIn("students", tables)
        self.assertIn("schema_versions", tables)
        with self.factory() as session:
            self.assertIsNotNone(session.scalar(select(SchemaVersion).where(SchemaVersion.version == CURRENT_SCHEMA_VERSION)))

    def test_seed_relations_and_rebuild(self):
        seed_synthetic_dataset(self.factory)
        with self.factory() as session:
            student = session.scalar(select(Student).where(Student.external_id == "TEST-STUDENT-001"))
            self.assertIsNotNone(student)
            attendance = session.scalar(select(Attendance).where(Attendance.student_id == student.id))
            self.assertEqual(attendance.status, "PRESENT")
        self.factory._quran_engine.dispose()
        rebuilt = initialize_database(self.root / "rebuild.sqlite")
        seed_synthetic_dataset(rebuilt)
        with rebuilt() as session:
            self.assertEqual(session.query(Student).count(), 1)
        rebuilt._quran_engine.dispose()
        self.factory = initialize_database(self.root / "fresh.sqlite")

    def test_foreign_key_rejects_missing_group(self):
        with self.factory() as session:
            with self.assertRaises(IntegrityError):
                session.add(Student(external_id="TEST-BAD-STUDENT", display_name="Synthetic", group_id=99999))
                session.commit()
            session.rollback()

    def test_unique_and_check_constraints(self):
        with self.factory() as session:
            session.add(UserAccount(external_id="TEST-USER-001", display_name="Synthetic", role="TEACHER"))
            session.commit()
            session.add(UserAccount(external_id="TEST-USER-001", display_name="Duplicate", role="TEACHER"))
            with self.assertRaises(IntegrityError):
                session.commit()
            session.rollback()
            session.add(UserAccount(external_id="TEST-BAD-ROLE", display_name="Synthetic", role="OWNER"))
            with self.assertRaises(IntegrityError):
                session.commit()


if __name__ == "__main__":
    unittest.main()
