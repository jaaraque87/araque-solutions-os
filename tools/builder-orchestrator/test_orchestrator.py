import importlib.util
import pathlib
import unittest

from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


mount = load("montar_proyecto")
render = load("render_headless")


class ProductionSettingsTests(unittest.TestCase):
    def test_preserves_models_and_fixes_seed(self):
        session = {"i2v_video_settings": {"unet_name": "model.gguf", "seed": 3}}
        mount.apply_production_settings(session)
        settings = session["i2v_video_settings"]
        self.assertEqual(settings["unet_name"], "model.gguf")
        self.assertEqual(settings["seed"], 69)
        self.assertEqual(settings["seed_mode"], "fixed")
        self.assertEqual((settings["width"], settings["height"], settings["fps"]), (1080, 1920, 24))

    def test_creates_missing_settings_object(self):
        session = {}
        mount.apply_production_settings(session, seed=101)
        self.assertEqual(session["i2v_video_settings"]["seed"], 101)
        self.assertEqual(session["video_model_mode"], "i2v")

    def test_fresh_segment_does_not_inherit_render_state_or_mutable_lists(self):
        mold = {**mount.FACTORY, "video_path": "/old/video_0005.mp4",
                "video_status": "done", "video_history": ["old.mp4"],
                "overlay_slot_number": 5}
        scene = {
            "n": 3, "dur": 6.64, "prompt": "speak naturally",
            "img_saved": "/project/zimage_approved/image_0003.png",
            "preview_saved": "/project/previews/image_0003.png",
            "aud_saved": "/project/audio/esc3.mp3", "aud": "esc3.mp3",
            "aud_dur_real": 6.64, "image_sha256": "image-hash",
            "audio_sha256": "audio-hash",
        }
        segment = mount.fresh_segment(mold, scene, 11.76)
        self.assertEqual(segment["overlay_slot_number"], 3)
        self.assertEqual(segment["video_path"], "")
        self.assertEqual(segment["video_status"], "none")
        self.assertEqual(segment["video_history"], [])
        self.assertEqual(segment["automation_contract"]["scene_number"], 3)
        segment["video_history"].append("new.mp4")
        self.assertEqual(mold["video_history"], ["old.mp4"])


class RenderPayloadTests(unittest.TestCase):
    def test_global_seed_wins_over_stale_scene_override(self):
        session = {"i2v_video_settings": {"seed": 69, "width": 1080, "height": 1920, "fps": 24}}
        segment = {
            "start": 0,
            "end": 4.6,
            "use_scene_i2v_video_settings": True,
            "i2v_video_settings": {"seed": 17, "pass1_sampler_name": "euler_ancestral"},
        }
        payload = render.settings_payload(session, segment)
        self.assertEqual(payload["seed"], 69)
        self.assertEqual(payload["seed_mode"], "fixed")
        self.assertEqual(payload["duration"], 4.6)
        self.assertEqual(payload["pass1_sampler_name"], "euler_ancestral")

    def test_payload_restores_builder_model_defaults_for_raw_session(self):
        payload = render.settings_payload(
            {"i2v_video_settings": {"seed": 69}},
            {"duration": 3},
        )
        self.assertEqual(payload["unet_name"], "LTX-2.3-22B-distilled-1.1-Q6_K.gguf")

    def test_history_error_is_extracted(self):
        history = {"abc": {"status": {"messages": [
            ["execution_error", {"exception_message": "boom"}],
        ]}}}
        self.assertEqual(render.prompt_failure(history, "abc"), "boom")

    def test_validate_scene_requires_three_inputs(self):
        with self.assertRaisesRegex(render.ApiError, "prompt I2V.*imagen aprobada.*audio"):
            render.validate_scene({}, 0)

    def test_queue_prompt_injects_non_null_workflow_metadata(self):
        class FakeApi:
            def __init__(self):
                self.body = None

            def get(self, route):
                self.assert_route = route
                return {"queue_running": [], "queue_pending": []}

            def post(self, route, body):
                self.body = body
                return {"prompt_id": "pid-1"}

        api = FakeApi()
        prompt_id = render.queue_prompt(api, {"1": {"class_type": "Test"}})
        self.assertEqual(prompt_id, "pid-1")
        self.assertEqual(api.assert_route, "/queue")
        workflow = api.body["extra_data"]["extra_pnginfo"]["workflow"]
        self.assertEqual(workflow, {"nodes": [], "extra": {}})
        self.assertIn("client_id", api.body)

    def test_recovery_rejects_unfingerprinted_or_wrong_slot_clips(self):
        class FakeApi:
            def post(self, route, payload):
                return {"videos": {"1": "/project/rendered/video_0005-audio.mp4"}}
        session = {"i2v_video_settings": {"seed": 69}}
        segment = {
            "id": "auto-esc1", "duration": 2.68, "i2v_prompt": "talk",
            "approved_image_path": "/project/image_0001.png",
            "custom_audio_path": "/project/esc1.mp3",
            "video_path": "/project/rendered/video_0005-audio.mp4",
            "video_status": "done",
        }
        render.recover_existing(FakeApi(), "/project", session, [segment])
        self.assertEqual(segment["video_path"], "")
        self.assertEqual(segment["video_status"], "none")

    def test_stitch_rejects_duplicate_paths(self):
        segments = [
            {"overlay_slot_number": 1, "video_path": "/project/video_0001.mp4"},
            {"overlay_slot_number": 2, "video_path": "/project/video_0001.mp4"},
        ]
        with self.assertRaisesRegex(render.ApiError, "duplicados"):
            render.validate_stitch_paths(segments)


class DryRunCliTests(unittest.TestCase):
    def test_dry_run_loads_and_validates_without_queueing(self):
        class FakeApi:
            instances = []

            def __init__(self, tunnel):
                self.tunnel = tunnel
                self.routes = []
                self.__class__.instances.append(self)

            def post(self, route, payload, **kwargs):
                self.routes.append(route)
                if route.endswith("/load_session"):
                    return {
                        "project_folder": "/comfyui/output/TEST",
                        "session": {
                            "i2v_video_settings": {"seed": 69},
                            "segments": [{
                                "duration": 2.5,
                                "i2v_prompt": "talking naturally",
                                "approved_image_path": "/comfyui/output/TEST/zimage_approved/image_0001.png",
                                "custom_audio_path": "/comfyui/output/TEST/audio/esc1.mp3",
                            }],
                        },
                    }
                if route.endswith("/scan_scene_videos"):
                    return {"videos": {}}
                raise AssertionError(f"Unexpected POST in dry-run: {route}")

        argv = [
            "render_headless.py",
            "--tunnel", "https://example.invalid",
            "--project", "/comfyui/output/TEST",
            "--dry-run",
        ]
        with mock.patch.object(render, "BuilderApi", FakeApi), mock.patch.object(render.sys, "argv", argv):
            self.assertEqual(render.main(), 0)
        self.assertEqual(FakeApi.instances[0].routes, [
            "/vrgdg/music_builder/load_session",
            "/vrgdg/music_builder/scan_scene_videos",

        ])

if __name__ == "__main__":
    unittest.main()
