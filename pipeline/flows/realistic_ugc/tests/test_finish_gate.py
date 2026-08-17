from __future__ import annotations

import argparse
import tempfile
import unittest
from pathlib import Path

from pipeline.flows.realistic_ugc.core import approve_stage, initialize_run, set_stage
from pipeline.flows.realistic_ugc.run import command_main


class FinishGateTests(unittest.TestCase):
    def test_final_promotion_requires_explicit_finishing_approval(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            product = root / "product.png"
            product.write_bytes(b"product")
            master = root / "master.mp4"
            master.write_bytes(b"video")
            run_dir = initialize_run(
                brand="Client",
                campaign="Launch",
                description="Final Gate",
                product_image=product,
                outputs_root=root / "outputs" / "ugc",
                run_slug="final-gate-20260817-120000",
            )
            set_stage(run_dir, "qa", status="ready_for_review")
            approve_stage(run_dir, "qa", "Paul")
            set_stage(run_dir, "finishing", status="ready_for_review", artifacts=[])
            args = argparse.Namespace(command="finish", run_dir=run_dir, final_video=master)
            with self.assertRaises(PermissionError):
                command_main(args)
            approve_stage(run_dir, "finishing", "Client")
            self.assertEqual(command_main(args), 0)
            self.assertTrue((run_dir / "final.mp4").is_file())


if __name__ == "__main__":
    unittest.main()
