import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("render_scene.py")
SPEC = importlib.util.spec_from_file_location("render_scene", MODULE_PATH)
render_scene = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(render_scene)


class TaoSceneAdapterTests(unittest.TestCase):
    def template(self):
        return {
            "30": {"inputs": {"noise_seed": 0}},
            "37": {"inputs": {"filename_prefix": "video/old"}},
            "131": {"inputs": {}},
        }

    def test_build_workflow_keeps_visual_audio_pair_exact(self):
        workflow, frames = render_scene.build_workflow(
            self.template(),
            image_file="whatdreamscost/esc3.png",
            audio_file="whatdreamscost/esc3.mp3",
            prompt="serious talking head",
            seconds=6.64,
            seed=1234,
            width=640,
            height=1152,
            scene_id="esc3",
        )
        self.assertEqual(frames, 160)
        director = workflow["131"]["inputs"]
        timeline = json.loads(director["timeline_data"])
        self.assertEqual(timeline["segments"][0]["imageFile"], "whatdreamscost/esc3.png")
        self.assertEqual(timeline["audioSegments"][0]["audioFile"], "whatdreamscost/esc3.mp3")
        self.assertEqual(timeline["segments"][0]["length"], frames)
        self.assertEqual(timeline["audioSegments"][0]["length"], frames)
        self.assertEqual(workflow["30"]["inputs"]["noise_seed"], 1234)
        self.assertTrue(director["use_custom_audio"])

    def test_template_is_not_mutated(self):
        template = self.template()
        original = json.loads(json.dumps(template))
        render_scene.build_workflow(
            template,
            image_file="i.png",
            audio_file="a.mp3",
            prompt="p",
            seconds=1,
            seed=1,
            width=640,
            height=1152,
            scene_id="s1",
        )
        self.assertEqual(template, original)

    def test_prompt_key_is_required(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "prompts.txt"
            path.write_text("I2V1=hello\n", encoding="utf-8")
            self.assertEqual(render_scene.prompt_text(path, "I2V1"), "hello")
            with self.assertRaises(KeyError):
                render_scene.prompt_text(path, "I2V2")


if __name__ == "__main__":
    unittest.main()
