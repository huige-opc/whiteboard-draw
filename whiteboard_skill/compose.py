"""FFmpeg-based video and audio composition."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path


def ffmpeg_path() -> str:
    """Return ffmpeg path or raise a clear error."""

    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found on PATH")
    return ffmpeg


def ffprobe_duration(path: Path) -> float:
    """Return media duration in seconds via ffprobe."""

    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        return 0.0
    result = subprocess.run(
        [ffprobe, "-v", "error", "-show_entries", "format=duration", "-of", "default=nokey=1:noprint_wrappers=1", str(path)],
        check=True,
        text=True,
        capture_output=True,
    )
    try:
        return float(result.stdout.strip())
    except ValueError:
        return 0.0


def compose_project(video_paths: list[Path], audio_paths: list[Path], out_path: Path) -> Path:
    """Concatenate scene videos and optionally mux concatenated narration."""

    if not video_paths:
        raise ValueError("No scene videos to compose")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="whiteboard-compose-") as tmp:
        tmp_dir = Path(tmp)
        concat_video = tmp_dir / "video.mp4"
        _concat_videos(video_paths, concat_video)
        usable_audio = [p for p in audio_paths if p and p.exists()]
        if usable_audio:
            concat_audio = tmp_dir / "audio.m4a"
            _concat_audio(usable_audio, concat_audio)
            subprocess.run([ffmpeg_path(), "-y", "-i", str(concat_video), "-i", str(concat_audio), "-c:v", "copy", "-c:a", "aac", "-movflags", "+faststart", str(out_path)], check=True)
        else:
            shutil.copyfile(concat_video, out_path)
    return out_path


def _concat_videos(video_paths: list[Path], out_path: Path) -> None:
    if len(video_paths) == 1:
        shutil.copyfile(video_paths[0], out_path)
        return
    list_file = out_path.with_suffix(".txt")
    list_file.write_text("".join(f"file '{p.resolve()}'\n" for p in video_paths), encoding="utf-8")
    subprocess.run([ffmpeg_path(), "-y", "-f", "concat", "-safe", "0", "-i", str(list_file), "-c", "copy", str(out_path)], check=True)


def _concat_audio(audio_paths: list[Path], out_path: Path) -> None:
    if len(audio_paths) == 1:
        subprocess.run([ffmpeg_path(), "-y", "-i", str(audio_paths[0]), "-c:a", "aac", str(out_path)], check=True)
        return
    cmd = [ffmpeg_path(), "-y"]
    for path in audio_paths:
        cmd.extend(["-i", str(path)])
    inputs = "".join(f"[{idx}:a]" for idx in range(len(audio_paths)))
    filter_complex = f"{inputs}concat=n={len(audio_paths)}:v=0:a=1[a]"
    cmd.extend(["-filter_complex", filter_complex, "-map", "[a]", "-c:a", "aac", str(out_path)])
    subprocess.run(cmd, check=True)
