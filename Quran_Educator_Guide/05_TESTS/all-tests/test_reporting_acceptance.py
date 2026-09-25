import tempfile
import unittest
from pathlib import Path

from quran_educator.presentation.reporting import (
    create_circle_report,
    create_session_report,
    create_student_report,
    create_synthetic_status_report,
)


class ReportingAcceptanceTests(unittest.TestCase):
    def assert_valid_pdf(self, output: Path, expected_title: bytes):
        self.assertTrue(output.exists())
        payload = output.read_bytes()
        self.assertTrue(payload.startswith(b"%PDF"))
        self.assertGreater(len(payload), 500)
        self.assertIn(expected_title, payload)

    def test_all_local_reports_are_valid(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        creators = [
            (create_synthetic_status_report, "status.pdf", b"Controlled Development Status"),
            (create_student_report, "student.pdf", b"Synthetic Student Report"),
            (create_circle_report, "circle.pdf", b"Synthetic Circle Report"),
            (create_session_report, "session.pdf", b"Synthetic Session Report"),
        ]
        for creator, name, title in creators:
            output = Path(temp.name) / name
            creator(output)
            self.assert_valid_pdf(output, title)

    def test_report_handles_custom_synthetic_label(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        output = Path(temp.name) / "custom.pdf"
        create_student_report(output, "Synthetic Student 001")
        self.assert_valid_pdf(output, b"Synthetic Student Report")


if __name__ == "__main__":
    unittest.main()
