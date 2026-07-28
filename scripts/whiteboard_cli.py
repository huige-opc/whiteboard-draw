#!/usr/bin/env python3
"""Run the bundled whiteboard-video-engine CLI.

Engine source is bundled in this repository under whiteboard_skill/.
External dependencies: numpy, Pillow, pydantic, ffmpeg.
"""

from __future__ import annotations

import sys


MISSING_DEPS_HELP = """
Missing required dependency: {dep}

Install it with:
  python3 -m pip install {dep}

Or install all at once:
  python3 -m pip install numpy Pillow pydantic
""".strip()

FFMPEG_HELP = """
ffmpeg is required but not found on PATH.

Install ffmpeg:
  Windows:  winget install ffmpeg
  macOS:    brew install ffmpeg
  Linux:    apt install ffmpeg
""".strip()


def check_deps() -> bool:
    ok = True
    try:
        import numpy  # noqa: F401
    except ImportError:
        print(MISSING_DEPS_HELP.format(dep="numpy"), file=sys.stderr)
        ok = False
    try:
        import PIL  # noqa: F401
    except ImportError:
        print(MISSING_DEPS_HELP.format(dep="Pillow"), file=sys.stderr)
        ok = False
    try:
        import pydantic  # noqa: F401
    except ImportError:
        print(MISSING_DEPS_HELP.format(dep="pydantic"), file=sys.stderr)
        ok = False
    return ok


def main() -> int:
    if not check_deps():
        return 1

    try:
        from whiteboard_skill.cli import main as engine_main
    except ModuleNotFoundError:
        print(
            "Engine module not found. Make sure whiteboard_skill/ is in the same "
            "directory as this script.",
            file=sys.stderr,
        )
        return 1

    return int(engine_main())


if __name__ == "__main__":
    raise SystemExit(main())
