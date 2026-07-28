"""Provider interfaces and factory helpers."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from ..config import settings


class LLMProvider(Protocol):
    """Split raw scripts into storyboard scene dictionaries."""

    def split_scenes(self, script: str, scene_count: int) -> list[dict[str, object]]:
        """Return scene dictionaries containing narration and image_prompt."""


class ImageProvider(Protocol):
    """Generate line-art images for a scene prompt."""

    def generate(self, prompt: str, out_path: Path, size: tuple[int, int]) -> Path:
        """Write an image file and return its path."""


class TTSProvider(Protocol):
    """Synthesize narration audio."""

    def synthesize(self, text: str, out_path: Path, voice: str) -> float:
        """Write audio and return estimated or measured duration in seconds."""


@dataclass(frozen=True)
class ProviderBundle:
    """Concrete providers used by a pipeline run."""

    llm: LLMProvider
    image: ImageProvider
    tts: TTSProvider


def _truthy(value: str | None) -> bool:
    return bool(value and value.lower() in {"1", "true", "yes", "on"})


def get_providers(mock: bool | None = None) -> ProviderBundle:
    """Return provider implementations.

    If `mock` is true, or `MOCK=1` is set, the returned providers run fully
    offline and produce deterministic assets. Otherwise the OpenAI and Edge TTS
    providers are selected lazily so missing optional dependencies fail only
    when a real run is requested.
    """

    use_mock = settings.mock if mock is None else mock
    use_mock = use_mock or _truthy(os.getenv("MOCK"))
    if use_mock:
        from .image_mock import MockImageProvider
        from .llm_mock import MockLLMProvider
        from .tts_mock import MockTTSProvider

        return ProviderBundle(llm=MockLLMProvider(), image=MockImageProvider(), tts=MockTTSProvider())

    from .image_openai import OpenAIImageProvider
    from .llm_openai import OpenAILLMProvider
    from .tts_edge import EdgeTTSProvider

    return ProviderBundle(llm=OpenAILLMProvider(), image=OpenAIImageProvider(), tts=EdgeTTSProvider())
