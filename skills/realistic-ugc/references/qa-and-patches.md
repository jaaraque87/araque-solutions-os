# QA and shot patches

Review in order: protagonist identity; duplicates; object counts; real procedure; label/package integrity; dialogue; room tone/unwanted music; loudness; dimensions; duration; audio stream.

The CLI writes `qa/report.json` and `qa/contact-sheet.png`. `--transcribe` adds `qa/transcript.json` through OpenAI Whisper API.

Use `cuts` to find probable boundaries and `prepare-patch --shot <n> --start <s> --end <s>` to extract anchors. A patch prompt needs one continuous shot, anchor/product roles, specific correction and prohibition, full action with states, one camera behavior, corrected audio, and continuity constraints. Generate about one second longer than the hole. Check transcript timing because speech may cross a visual cut.
