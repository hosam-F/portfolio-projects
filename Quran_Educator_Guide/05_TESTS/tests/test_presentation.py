import tempfile
import unittest
from pathlib import Path
from PySide6.QtWidgets import QApplication, QStackedWidget
from quran_educator.presentation.app import MainWindow


class PresentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_main_window_has_operational_tabs_and_gate_banner(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        window = MainWindow(Path(temp.name) / "ui.sqlite")
        self.addCleanup(window.close)
        self.assertIn("بيئة التطوير المضبوطة", window.status.text())
        tabs = window.findChild(QStackedWidget)
        self.assertIsNotNone(tabs)
        self.assertEqual(tabs.count(), 9)

    def test_ui_controller_runs_synthetic_slice(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        window = MainWindow(Path(temp.name) / "ui.sqlite")
        self.addCleanup(window.close)
        ids = window.controller.seed_demo()
        self.assertTrue(ids["student_id"] > 0)
        session_id = window.controller.run_vertical_slice()
        self.assertGreater(session_id, 0)


if __name__ == "__main__":
    unittest.main()
