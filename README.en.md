# Whiteboard Draw

[中文](README.md) | [GitHub](https://github.com/huige-opc/whiteboard-draw)

**Hand-drawn whiteboard animation tool** — Convert images, SVGs, line art, photos, or text scripts into hand-drawn whiteboard MP4 videos. Engine is bundled, clone and use.

## Quick Start

```bash
# 1. Dependencies
pip install numpy Pillow pydantic

# 2. ffmpeg required on PATH
# Windows: winget install ffmpeg
# macOS:   brew install ffmpeg
# Linux:   apt install ffmpeg

# 3. Clone
git clone https://github.com/huige-opc/whiteboard-draw.git
cd whiteboard-draw

# 4. Verify
python3 scripts/whiteboard_cli.py doctor

# 5. Try it (SVG to whiteboard)
python3 scripts/whiteboard_cli.py render-image examples/apple.svg -o apple.mp4 --duration 3 --hand asian

# 6. Photo to whiteboard
python3 scripts/whiteboard_cli.py render-photo photo.jpg -o photo-whiteboard.mp4 --duration 15 --hand asian
```

## Usage

### 1. SVG / Line Art to Whiteboard

```bash
python3 scripts/whiteboard_cli.py render-image input.svg -o output.mp4 --duration 10 --fps 30 --hand asian
```

Options:
- `--duration`: video length in seconds
- `--fps`: frame rate (12-24 preview, 30-60 final)
- `--hand`: hand cursor style: `asian` / `black` / `children` / `white` / `procedural` / `none`
- `--width` `--height`: output resolution (default 1920x1080)

### 2. Photo to Whiteboard

Extracts line art locally then renders:

```bash
# One step
python3 scripts/whiteboard_cli.py render-photo photo.jpg -o out.mp4 --duration 15 --fps 30 --hand asian --stroke-detail rich

# Or step by step
python3 scripts/whiteboard_cli.py extract-lineart photo.jpg -o lineart.png --provider auto
python3 scripts/whiteboard_cli.py render-image lineart.png --source-image photo.jpg --color-fill contour-wipe -o out.mp4 --duration 15 --fps 30 --hand asian
```

Line-art providers:
- `auto` → automatic, prefers Informative Drawings, falls back to Anime2Sketch
- `informative` → best for photos
- `anime2sketch` → best for illustrations/anime

### 3. Script-Driven (Multi-Scene)

Write a Markdown script and run:

```bash
python3 scripts/whiteboard_cli.py run scenes.md -o final.mp4 --scenes 3 --fps 24
```

Script format (see `examples/ten-second-demo.md`):

```md
The sun rises, the city wakes up, streetlights fade out.

A person opens a notebook and writes down today's most important goal.
```

### 4. Color Fill Overlay

```bash
python3 scripts/whiteboard_cli.py render-image lineart.png \
  --source-image photo.png \
  --color-fill contour-wipe \
  -o out.mp4 --duration 15 --fps 30 --tail-color 4.5 --hand asian
```

- `--tail-color`: seconds the color trails behind the pen tip (higher = slower fill)
- `--color-fill`: fill mode, `contour-wipe` fills along contours

### 5. Hand-Drawn Text

```bash
python3 scripts/whiteboard_cli.py render-image input.svg --draw-text "Hello World" -o out.mp4 --duration 10
```

### 6. Other Commands

```bash
# List hand styles
python3 scripts/whiteboard_cli.py list-hands

# Analyze image complexity
python3 scripts/whiteboard_cli.py analyze-image input.png -o analysis.json

# Compose multiple clips
python3 scripts/whiteboard_cli.py compose -i clip1.mp4 clip2.mp4 -o final.mp4
```

## Local Line-Art Models (Advanced)

Line-art extraction requires neural network models. **Not included in this repository**.

Recommended layout (in your project directory, outside this repo):

```text
my-whiteboard-project/
  tools/
    lineart/
      run_informative_drawings.py
      run_anime2sketch.py
    informative-drawings/      # full upstream checkout
      checkpoints/model/anime_style/netG_A_latest.pth
    Anime2Sketch/               # full upstream checkout
      weights/netG.pth
```

Or via environment variables:

```bash
export WHITEBOARD_INFORMATIVE_DRAWINGS_CMD="python /path/to/run_informative_drawings.py {input} {output}"
export WHITEBOARD_ANIME2SKETCH_CMD="python /path/to/run_anime2sketch.py {input} {output}"
```

## Contents

| Directory/File | Description |
|----------------|-------------|
| `whiteboard_skill/` | Rendering engine (bundled) |
| `scripts/whiteboard_cli.py` | CLI entry point |
| `SKILL.md` | AI assistant skill instructions |
| `references/` | Workflow docs |
| `examples/` | Sample assets |
| `agents/openai.yaml` | Skill metadata (optional) |
| `docs/` | Documentation assets |

## Not Included

- Line-art model repos (download separately)
- Model weights (.pth / .pt etc.)
- Generated MP4 files
- User uploaded assets

## License

MIT
