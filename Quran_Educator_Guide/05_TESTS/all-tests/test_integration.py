import tempfile
import unittest
from pathlib import Path
from quran_educator.presentation.controller import ControlledAppController


class IntegrationTests(unittest.TestCase):
    def test_application_controller_end_to_end(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        controller = ControlledAppController(Path(temp.name) / "integration.sqlite")
        self.addCleanup(controller.close)
        ids = controller.seed_demo()
        session_id = controller.run_vertical_slice()
        self.assertGreater(ids["student_id"], 0)
        self.assertGreater(session_id, 0)
        backup = Path(temp.name) / "backup.sqlite"
        restored = Path(temp.name) / "restored.sqlite"
        self.assertTrue(controller.backup_restore_verify(backup, restored))


if __name__ == "__main__":
    unittest.main()
