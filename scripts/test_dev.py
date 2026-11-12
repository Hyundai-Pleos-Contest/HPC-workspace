"""Regression checks for local configuration/data preservation; no Docker required."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import dev


class LifecycleSafetyTest(unittest.TestCase):
    def test_init_preserves_existing_configuration(self):
        with tempfile.TemporaryDirectory() as directory:
            env_file = Path(directory) / ".env"
            dev.initialize(env_file)
            self.assertEqual(env_file.read_text(encoding="utf-8"), (dev.ROOT / ".env.example").read_text(encoding="utf-8"))
            env_file.write_bytes(b"BE_PORT=18081\r\n# developer settings\r\n")
            dev.initialize(env_file)
            self.assertEqual(env_file.read_bytes(), b"BE_PORT=18081\r\n# developer settings\r\n")

    def test_down_scopes_project_and_preserves_volumes(self):
        with tempfile.TemporaryDirectory() as directory:
            env_file = Path(directory) / ".env"
            env_file.touch()
            with patch("sys.argv", ["dev.py", "down", "--project", "hpc-test", "--env-file", str(env_file)]), patch("dev.run") as run:
                self.assertEqual(dev.main(), 0)
            command = run.call_args.args[0]
            self.assertEqual(command[command.index("--project-name") + 1], "hpc-test")
            self.assertEqual(command[command.index("--file") + 1], str(dev.ROOT / "compose.yaml"))
            self.assertEqual(command[-1], "down")
            self.assertNotIn("--volumes", command)
            self.assertNotIn("--remove-orphans", command)

    def test_missing_env_does_not_start_containers(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch("sys.argv", ["dev.py", "up", "--env-file", str(Path(directory) / "missing")]), patch("dev.run") as run:
                with self.assertRaisesRegex(RuntimeError, "Missing env"):
                    dev.main()
                run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
