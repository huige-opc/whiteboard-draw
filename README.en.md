# Whiteboard Draw

[中文](README.md)

**Hand-drawn whiteboard animation tool** — Convert images, SVGs, line art, or scripts into whiteboard explainer videos. Engine is bundled, clone and use.

## Architecture

```
whiteboard-draw/
  scripts/whiteboard_cli.py  ← CLI entry point
  whiteboard_skill/          ← rendering engine (bundled)
  SKILL.md                   ← AI assistant skill instructions
```

## Installation

### Dependencies

```bash
pip install numpy Pillow pydantic
```

ffmpeg must be on PATH:

```bash
winget install ffmpeg          # Windows
brew install ffmpeg             # macOS
apt install ffmpeg              # Linux
```

### Clone

```bash
git clone https://github.com/huige-opc/whiteboard-draw.git
cd whiteboard-draw
```

### Verify

```bash
python3 scripts/whiteboard_cli.py doctor
```

## Usage

```bash
# SVG hand-drawn rendering
python3 scripts/whiteboard_cli.py render-image input.svg -o output.mp4 --duration 10 --fps 30 --hand asian

# Photo to hand-drawn
python3 scripts/whiteboard_cli.py render-photo photo.jpg -o output.mp4 --duration 15 --fps 30 --lineart-provider auto --stroke-detail rich --hand asian

# Line art + color fill overlay
python3 scripts/whiteboard_cli.py render-image lineart.png --source-image photo.png --color-fill contour-wipe -o output.mp4 --duration 15 --fps 30 --tail-color 4.5 --hand asian

# Script-driven workflow
python3 scripts/whiteboard_cli.py run scenes.md -o output.mp4 --scenes 3 --fps 24
```

## Local Models

Line-art extraction requires local neural network models:

```text
my-whiteboard-project/
  tools/
    lineart/
      run_informative_drawings.py
      run_anime2sketch.py
    informative-drawings/      # full upstream checkout
    Anime2Sketch/               # full upstream checkout
```

Or via environment variables:

```bash
export WHITEBOARD_INFORMATIVE_DRAWINGS_CMD="python /path/to/run_informative_drawings.py {input} {output}"
export WHITEBOARD_ANIME2SKETCH_CMD="python /path/to/run_anime2sketch.py {input} {output}"
```

## Contents

| File/Dir | Description |
|----------|-------------|
| `SKILL.md` | AI assistant skill instructions |
| `scripts/whiteboard_cli.py` | CLI entry point |
| `whiteboard_skill/` | Rendering engine (bundled) |
| `references/` | Workflow docs |
| `examples/` | Sample assets |
| `agents/openai.yaml` | Skill metadata (optional) |

## Not Included

- Line-art model repos (download separately)
- Model weights
- Generated videos
- User uploads

## License

MIT. Upstream model code and weights keep their own licenses.
