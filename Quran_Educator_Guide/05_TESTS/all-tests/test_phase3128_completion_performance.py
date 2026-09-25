import json
import tempfile
import time
import unittest
from pathlib import Path

from quran_educator.application.query_services import SearchService
from quran_educator.domain.models import AuthorizationContext
from quran_educator.infrastructure.db import Circle, Group, Organization, Student
from quran_educator.infrastructure.migrations import CURRENT_SCHEMA_VERSION, initialize_database


class CompletionPerformanceTests(unittest.TestCase):
    def test_search_filter_migration_baseline(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            path = root / "performance.sqlite"
            start = time.perf_counter()
            factory = initialize_database(path)
            migration_seconds = time.perf_counter() - start
            try:
                with factory() as session:
                    organizations = [Organization(external_id=f"TEST-COMP-ORG-{i}", name="TEST DATA ONLY", is_synthetic=True) for i in range(2)]
                    session.add_all(organizations)
                    session.flush()
                    circles = [Circle(organization_id=organizations[i % 2].id, external_id=f"TEST-COMP-CIRCLE-{i}", name="TEST DATA ONLY", is_synthetic=True) for i in range(10)]
                    session.add_all(circles)
                    session.flush()
                    groups = [Group(circle_id=circles[i % 10].id, external_id=f"TEST-COMP-GROUP-{i}", name="TEST DATA ONLY", is_synthetic=True) for i in range(20)]
                    session.add_all(groups)
                    session.flush()
                    students = [Student(group_id=groups[i % 20].id, external_id=f"TEST-COMP-STUDENT-{i:04d}", display_name="TEST DATA ONLY", is_synthetic=True) for i in range(500)]
                    session.add_all(students)
                    session.commit()
                    group_id = groups[0].id
                context = AuthorizationContext("TEST-COMP-ACTOR", "TEACHER", frozenset({"student:read"}))
                service = SearchService(factory)
                start = time.perf_counter()
                all_rows = service.search_students(context, "TEST-COMP-STUDENT")
                search_seconds = time.perf_counter() - start
                start = time.perf_counter()
                filtered_rows = service.search_students(context, "TEST-COMP-STUDENT", group_id=group_id)
                filter_seconds = time.perf_counter() - start
                self.assertEqual(len(all_rows), 100)
                self.assertGreater(len(filtered_rows), 0)
                artifact = {
                    "dataset": {"organizations": 2, "circles": 10, "groups": 20, "students": 500},
                    "measurements_seconds": {"migration": migration_seconds, "search": search_seconds, "filter": filter_seconds},
                    "result_counts": {"search_bounded": len(all_rows), "filter": len(filtered_rows)},
                    "schema_version": CURRENT_SCHEMA_VERSION,
                    "note": "Synthetic regression baseline only; no production SLA or scalability claim.",
                }
                artifact_path = Path(__file__).parents[1] / "artifacts" / "phase3128_completion_performance.json"
                artifact_path.parent.mkdir(parents=True, exist_ok=True)
                artifact_path.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
            finally:
                factory._quran_engine.dispose()


if __name__ == "__main__":
    unittest.main()
