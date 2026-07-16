# TAO Director scene adapter

This is the generation stage for agency reels. One approved still and its matching
audio become one deterministic TAO LTX Director scene. HyperFrames remains the
assembly stage for captions, overlays, music, SFX, transitions, and final export.

The operator provides the live ComfyUI tunnel, an exported TAO API workflow, the
scene image/audio, prompt key, exact duration, and output path. The adapter uploads
the pair, creates a fixed-seed timeline, renders headlessly, downloads the video,
and writes a manifest containing hashes for every input and output.

Use `--dry-run` before GPU work. The validated pilot profile is 640x1152 at 24 fps;
raise resolution only after a scene passes motion, identity, audio, and lipsync QA.
Run folders (`*.tao/`) and rendered videos are production outputs and must not be
committed.
