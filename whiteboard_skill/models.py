"""Project data models."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


STYLE_SUFFIX = (
    ", whiteboard line art, pure black ink on white background, "
    "single subject, simple composition, no shading, no gradient, no text, no letters"
)


class Scene(BaseModel):
    """One storyboard scene."""

    id: int
    narration: str
    image_prompt: str
    duration_sec: float | None = None
    image_path: Path | None = None
    audio_path: Path | None = None
    video_path: Path | None = None


class Project(BaseModel):
    """Whiteboard project state persisted under work/<project_id>/."""

    title: str
    voice: str = "zh-CN-XiaoxiaoNeural"
    fps: int = 60
    width: int = 1920
    height: int = 1080
    tail_color_seconds: float = 2.0
    bgm_path: Path | None = None
    scenes: list[Scene] = Field(default_factory=list)

    @property
    def resolution(self) -> tuple[int, int]:
        """Return width and height as a tuple.

        Example:
            >>> Project(title="demo", width=640, height=360).resolution
            (640, 360)
        """

        return (self.width, self.height)
