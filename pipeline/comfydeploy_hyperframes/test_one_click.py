import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import one_click
import run


class OneClickTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.image = self.root / "araque-product.png"
        self.image.write_bytes(b"\x89PNG\r\n\x1a\n")

    def tearDown(self):
        self.temp.cleanup()

    def test_selects_three_scored_hooks_and_builds_preview_without_network(self):
        hooks_file = one_click.REPO_ROOT / "tools" / "hook-lab" / "clients" / "araque-solutions" / "hooks.json"
        with patch.object(one_click, "call_comfydeploy") as network:
            run_dir, brief, hooks, hf_dir = one_click.create_preview_run(
                self.image,
                hooks_file=hooks_file,
                run_id="test-preview",
                runs_dir=self.root / "runs",
            )

        network.assert_not_called()
        self.assertEqual(len(hooks), 3)
        self.assertEqual(hooks[0]["id"], "h03")
        self.assertEqual(brief["selected_hook_id"], "h03")
        self.assertTrue((run_dir / "hooks.scored.json").is_file())
        self.assertTrue((run_dir / "brief.auto.json").is_file())
        self.assertTrue((hf_dir / "index.html").is_file())
        manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["network_calls"], 0)
        self.assertFalse(manifest["gpu_started"])

    def test_real_execution_is_fail_closed(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "confirm-cost"):
                one_click.assert_real_execution_allowed(None, None)
            with self.assertRaisesRegex(RuntimeError, one_click.REAL_ENV_GATE):
                one_click.assert_real_execution_allowed(one_click.REAL_CONFIRMATION, "https://example.com/a.png")

    def test_legacy_runner_real_gate_also_requires_environment(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, run.REAL_ENV_GATE):
                run.assert_real_execution_allowed(run.REAL_CONFIRMATION)


if __name__ == "__main__":
    unittest.main()
