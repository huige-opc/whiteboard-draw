"""Scene image generation and quality checks."""

from __future__ import annotations

from pathlib import Path

from .logging_setup import logger
from .models import Scene
from .preprocess import quality_check
from .providers import ImageProvider


def generate_scene_images(scenes: list[Scene], provider: ImageProvider, images_dir: Path, size: tuple[int, int], resume: bool = False) -> list[Scene]:
    """Generate or reuse line-art images for every scene."""

    images_dir.mkdir(parents=True, exist_ok=True)
    for scene in scenes:
        out_path = images_dir / f"scene_{scene.id:02d}.png"
        if resume and out_path.exists():
            scene.image_path = out_path
            continue
        for attempt in range(1, 4):
            provider.generate(scene.image_prompt, out_path, size)
            ratio = quality_check(out_path, size)
            if 0.003 <= ratio <= 0.32:
                break
            logger.warning("scene {} image foreground ratio {:.3f} outside target range on attempt {}", scene.id, ratio, attempt)
        scene.image_path = out_path
    return scenes
