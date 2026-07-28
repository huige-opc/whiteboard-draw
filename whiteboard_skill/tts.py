"""Narration synthesis helpers."""

from __future__ import annotations

from pathlib import Path

from .models import Scene
from .providers import TTSProvider


def synthesize_scene_audio(scenes: list[Scene], provider: TTSProvider, audio_dir: Path, voice: str, resume: bool = False) -> list[Scene]:
    """Generate or reuse narration audio for every scene."""

    audio_dir.mkdir(parents=True, exist_ok=True)
    for scene in scenes:
        out_path = audio_dir / f"scene_{scene.id:02d}.wav"
        if resume and out_path.exists():
            scene.audio_path = out_path
            continue
        duration = provider.synthesize(scene.narration, out_path, voice)
        scene.audio_path = out_path
        if not scene.duration_sec:
            scene.duration_sec = duration
    return scenes
