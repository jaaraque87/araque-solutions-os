from __future__ import annotations

import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from pipeline.flows.realistic_ugc.core import (
    approve_stage,
    initialize_run,
    load_run,
    make_run_slug,
    require_gate,
    set_stage,
)
from pipeline.flows.realistic_ugc.providers import dry_run_payload


class RealisticUgcFlowTests(unittest.TestCase):
    def test_slug_is_contracted(self) -> None:
        slug = make_run_slug("Café Nuevo / Lanzamiento", datetime(2026, 8, 17, 9, 30, 0))
        self.assertEqual(slug, "caf-nuevo-lanzamiento-20260817-093000")

    def test_run_and_approval_gates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            product = root / "product.png"
            product.write_bytes(b"fake-image")
            run_dir = initialize_run(
                brand="Client",
                campaign="Launch",
                description="Premium UGC",
                product_image=product,
                outputs_root=root / "outputs" / "ugc",
                run_slug="premium-ugc-20260817-093000",
            )
            state = load_run(run_dir)
            with self.assertRaises(PermissionError):
                require_gate(state, "script")
            artifact = run_dir / "research" / "strategy.md"
            artifact.write_text("strategy", encoding="utf-8")
            set_stage(run_dir, "research", status="ready_for_review", artifacts=["research/strategy.md"])
            approve_stage(run_dir, "research", "Paul")
            require_gate(load_run(run_dir), "script")

    def test_video_dry_run_preserves_reference_order(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prompt = root / "prompt.txt"
            prompt.write_text("[Generation Goal]\nA phone-shot UGC clip.", encoding="utf-8")
            images = []
            for name in ("sheet.png", "location.png", "product.png", "look.png"):
                image = root / name
                image.write_bytes(b"ref")
                images.append(image)
            payload = dry_run_payload(
                prompt_file=prompt,
                images=images,
                duration=30,
                aspect_ratio="9:16",
                resolution="720p",
            )
            self.assertEqual(payload["reference_images_in_order"], [str(path) for path in images])
            self.assertEqual(payload["model"], "bytedance/seedance-2-5")


if __name__ == "__main__":
    unittest.main()
