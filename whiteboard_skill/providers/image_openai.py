"""OpenAI image provider."""

from __future__ import annotations

import base64
from pathlib import Path

from ..config import settings


class OpenAIImageProvider:
    """Generate PNG line art through an OpenAI-compatible image model."""

    def __init__(self) -> None:
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is required when MOCK is not enabled")
        try:
            from openai import OpenAI
        except Exception as exc:  # pragma: no cover - optional dependency branch
            raise RuntimeError("Install optional dependency `openai` or run with MOCK=1") from exc
        self._client = OpenAI(api_key=settings.openai_api_key, base_url=settings.openai_base_url)

    def generate(self, prompt: str, out_path: Path, size: tuple[int, int]) -> Path:
        """Generate an image and write it to `out_path`."""

        out_path.parent.mkdir(parents=True, exist_ok=True)
        image_size = _openai_size(size)
        result = self._client.images.generate(model=settings.image_model, prompt=prompt, size=image_size)
        item = result.data[0]
        b64 = getattr(item, "b64_json", None)
        if not b64:
            raise RuntimeError("Image provider returned no base64 PNG data")
        out_path.write_bytes(base64.b64decode(b64))
        return out_path


def _openai_size(size: tuple[int, int]) -> str:
    width, height = size
    if width == height:
        return "1024x1024"
    return "1536x1024" if width > height else "1024x1536"
