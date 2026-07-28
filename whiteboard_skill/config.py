"""Runtime configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _truthy(value: str | None) -> bool:
    return bool(value and value.lower() in {"1", "true", "yes", "on"})


@dataclass(frozen=True)
class Settings:
    """Environment-backed settings.

    Example:
        >>> Settings(mock=True).mock
        True
    """

    openai_api_key: str | None = None
    openai_base_url: str = "https://api.openai.com/v1"
    llm_model: str = "gpt-4.1-mini"
    image_model: str = "gpt-image-1"
    work_dir: Path = Path("./work")
    mock: bool = False
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            llm_model=os.getenv("LLM_MODEL", "gpt-4.1-mini"),
            image_model=os.getenv("IMAGE_MODEL", "gpt-image-1"),
            work_dir=Path(os.getenv("WORK_DIR", "./work")),
            mock=_truthy(os.getenv("MOCK")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )


settings = Settings.from_env()
