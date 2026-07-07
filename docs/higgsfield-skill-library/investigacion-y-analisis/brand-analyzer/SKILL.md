---
name: brand-analyzer
title: "Brand Analyzer"
category: investigacion-y-analisis
url: https://higgsfield.ai/supercomputer/marketplace/skills/81c4f2af-74dc-4e42-8ab0-099cfcdbb84c
installs: n/d
source: https://higgsfield.ai/supercomputer/skills
---

# Brand Analyzer

Extracts brand assets from a client website URL: logo, color palette (hex), typography, hero imagery, tagline, target audience.
Output is the typed \`client\_brand\` JSON object plus a local folder with downloaded asset files (logo + hero photos),
ready to be uploaded as references in image/video generation.

Run in parallel with \`research-agent\` when a brief contains a client URL plus downstream
image/video persona generation. May also be invoked on-demand from \`image-generation\` / \`video-generation\` when their input
contains a client URL but no pre-extracted \`client\_brand\` payload.
