import json
import tempfile
import time
import unittest
from pathlib import Path

from sqlalchemy import select

from quran_educator.infrastructure.db import Circle, Group, Organization, Student
from quran_educator.infrastructure.migrations import initialize_database
from quran_educator.presentation.reporting import create_student_report


class PerformanceBaselineTests(unittest.TestCase):
    def test_synthetic_dataset_baseline(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        db_path = Path(temp.name) / "performance.sqlite"
        factory = None
        try:
            start_open = time.perf_counter()
            factory = initialize_database(db_path)
            open_seconds = time.perf_counter() - start_open
            start_seed = time.perf_counter()
            with factory() as session:
                organizations = [Organization(external_id=f"TEST-PERF-ORG-{i:02d}", name="TEST DATA ONLY", is_synthetic=True) for i in range(2)]
                session.add_all(organizations)
                session.flush()
                circles = [Circle(organization_id=organizations[i % 2].id, external_id=f"TEST-PERF-CIRCLE-{i:02d}", name="TEST DATA ONLY", is_synthetic=True) for i in range(10)]
                session.add_all(circles)
                session.flush()
                groups = [Group(circle_id=circles[i % len(circles)].id, external_id=f"TEST-PERF-GROUP-{i:03d}", name="TEST DATA ONLY", is_synthetic=True) for i in range(20)]
                session.add_all(groups)
                session.flush()
                students = [Student(group_id=groups[i % len(groups)].id, external_id=f"TEST-PERF-STUDENT-{i:04d}", display_name="TEST DATA ONLY", is_synthetic=True) for i in range(500)]
                session.add_all(students)
                session.commit()
            seed_seconds = time.perf_counter() - start_seed
            start_query = time.perf_counter()
            with factory() as session:
                loaded = session.scalars(select(Student).where(Student.display_name == "TEST DATA ONLY")).all()
                self.assertEqual(len(loaded), 500)
            query_seconds = time.perf_counter() - start_query
            output = Path(temp.name) / "large_synthetic_student_report.pdf"
            start_report = time.perf_counter()
            create_student_report(output, "TEST DATA ONLY — 500 synthetic students")
            report_seconds = time.perf_counter() - start_report
            self.assertTrue(output.exists())
            artifact = {
                "dataset": {"organizations": 2, "circles": 10, "groups": 20, "students": 500},
                "measurements_seconds": {"database_open": open_seconds, "seed": seed_seconds, "student_query": query_seconds, "report_generation": report_seconds},
                "note": "Observed synthetic baseline only; no acceptance thresholds were imposed.",
            }
            artifact_path = Path(__file__).parents[1] / "artifacts" / "phase3127_performance_baseline.json"
            artifact_path.parent.mkdir(parents=True, exist_ok=True)
            artifact_path.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
        finally:
            if factory is not None:
                factory._quran_engine.dispose()


if __name__ == "__main__":
    unittest.main()
