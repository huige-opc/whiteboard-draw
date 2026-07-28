---
name: whiteboard-draw
description: Generate smooth hand-drawn whiteboard explainer videos from text scripts, scene plans, SVGs, line art, or local images. Use when the user asks for SpeedPaint-like whiteboard videos, stroke/path drawing, SVG-first rendering, local image-to-line-art extraction, raster skeleton tracing, hand/pen-tip following, color fill, narration/TTS, FFmpeg composition, or script-to-video whiteboard workflows.
---

# Whiteboard Draw

Use this skill to create local-first whiteboard videos. The rendering engine is bundled in this skill's `whiteboard_skill/` directory. Uploaded photos and dense illustrations are converted to line art locally; do not use image2 to generate line art. The preferred stack is:

1. `Informative Drawings` local model, preferably `anime_style`.
2. `Anime2Sketch` local model for illustration/anime-like sources.
3. Optional `vtracer` SVG vectorization when installed.

There is no edge-detection fallback. If neither neural model is installed, `extract-lineart` and `render-photo` must fail instead of silently producing a weak outline.

## Quick Start

Run commands from the repo root (where `whiteboard_skill/` lives):

```bash
# Verify setup
python3 scripts/whiteboard_cli.py doctor

# SVG rendering
python3 scripts/whiteboard_cli.py render-image examples/apple.svg -o /tmp/apple-whiteboard.mp4 --duration 2 --fps 24 --width 640 --height 360 --hand asian

# Photo rendering
python3 scripts/whiteboard_cli.py render-photo photo.png -o /tmp/photo-whiteboard.mp4 --duration 15 --fps 30 --lineart-provider auto --stroke-detail rich --hand asian

# Script-driven demo
MOCK=1 python3 scripts/whiteboard_cli.py run examples/ten-second-demo.md -o /tmp/whiteboard-demo.mp4 --scenes 2 --fps 24 --width 640 --height 360

# List available hand styles
python3 scripts/whiteboard_cli.py list-hands
```

## Workflow

1. Use `render-photo` for uploaded photos or dense illustrations. It extracts local line art first, then renders with the original image as the color-fill source.
2. Use `extract-lineart` when you want to inspect or reuse the line-art PNG before rendering.
3. Use `render-image` when the user already has a clean SVG or line-art PNG.
4. Use `plan-script` and `run` for script-driven scenes. If a script requires a generated scene image, generate the color scene first, then use local line-art extraction on that color scene.
5. Use `analyze-image` to estimate stroke count and foreground density.
6. Use `compose` to concatenate rendered scene clips.
7. Use `--lineart-provider auto|informative|anime2sketch|anime|manga`. `auto` tries Informative Drawings first, then Anime2Sketch. `manga` is kept only as a compatibility alias for Anime2Sketch.
8. Configure external deep extractors through environment variables:
   - `WHITEBOARD_INFORMATIVE_DRAWINGS_CMD`
   - `WHITEBOARD_ANIME2SKETCH_CMD`
   Commands may include `{input}` and `{output}` placeholders; otherwise input and output are appended as positional arguments.
9. Use `--svg-output <line.svg>` with `extract-lineart` or `render-photo` when `vtracer` is installed and you want SVG paths instead of raster skeleton tracing.
10. Use `--hand asian|black|children|white|procedural|none` to select the hand cursor. Built-in PNG hands keep a fixed orientation and only translate with the pen tip.
11. Use a color source with the exact same pixel size/aspect/crop as the line art whenever possible, then render with `--source-image <source> --source-fit exact --size-from-image --color-fill contour-wipe`.
12. Before final color fill, the renderer snaps only darker missing line-art pixels back to the redrawn stroke canvas so small extracted-stroke omissions do not look unfinished. The default snap threshold is `170` to avoid turning soft gray model lines into solid black. Use `--no-lineart-snap` only for debugging.
13. Use `--stroke-detail rich` by default; use `--stroke-detail max` only when faces/logos/badges still lose too many short strokes.
14. Use `--draw-text "短标题"` for short hand-drawn title text. The text is converted into strokes and drawn after the image strokes.

Prefer `MOCK=1` for integration tests and low-cost previews. Real providers are lazy-loaded and require configured provider credentials only for script-to-scene image or narration generation, not for uploaded-photo line-art extraction.

## Local Line-Art Step

For uploaded photos:

```bash
python3 scripts/whiteboard_cli.py extract-lineart source.png \
  --provider auto \
  -o lineart.png
```

Then render:

```bash
python3 scripts/whiteboard_cli.py render-image lineart.png \
  --source-image source.png \
  --source-fit exact \
  --size-from-image \
  --color-fill contour-wipe \
  --stroke-detail rich \
  --line-thickness 1 \
  -o output.mp4 \
  --duration 15 --fps 30 --tail-color 4.5 --hand asian
```

Or use the one-step shortcut:

```bash
python3 scripts/whiteboard_cli.py render-photo source.png \
  -o output.mp4 \
  --duration 15 --fps 30 \
  --lineart-provider auto \
  --stroke-detail rich \
  --hand asian
```

## Quality Rules

- Do not use image2 for line-art conversion. Local line-art extraction is the source of truth.
- Prefer `Informative Drawings` `anime_style` for quality when installed.
- Prefer `Anime2Sketch` for illustration/anime-like inputs or when Informative Drawings is unavailable.
- Do not use Canny/XDoG/edge-only fallback for production outputs.
- Optional `vtracer` can convert extracted line-art bitmaps to SVG paths for smoother path sampling.
- Keep the original uploaded image as the color-fill source when dimensions match. Because the line art is extracted from that same image, no anti-shrink or source-alignment correction should be needed.
- Render quick previews at 640x360 and 12-24fps; use 30-60fps for final output.

## Implementation Notes

`scripts/whiteboard_cli.py` imports `whiteboard_skill.cli` from the bundled `whiteboard_skill/` directory in this repository.
