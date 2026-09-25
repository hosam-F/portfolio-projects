from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass(frozen=True)
class LocalConfig:
    app_name: str = "Quran Educator Guide"
    environment: str = "controlled-development"
    synthetic_only: bool = True
    offline_only: bool = True
    database_filename: str = "database.sqlite"

    def validate(self) -> None:
        if self.environment != "controlled-development":
            raise ValueError("Only controlled-development configuration is permitted")
        if not self.synthetic_only or not self.offline_only:
            raise ValueError("Controlled configuration must remain synthetic-only and offline-only")
        if Path(self.database_filename).name != self.database_filename:
            raise ValueError("Database filename must be a safe local filename")


def load_local_config(path: Path | None = None) -> LocalConfig:
    if path is None or not path.exists():
        config = LocalConfig()
        config.validate()
        return config
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        config = LocalConfig(**{k: raw[k] for k in LocalConfig.__dataclass_fields__ if k in raw})
        config.validate()
        return config
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        raise ValueError(f"Invalid local configuration: {type(exc).__name__}") from exc


def save_local_config(path: Path, config: LocalConfig | None = None) -> Path:
    config = config or LocalConfig()
    config.validate()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(config), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path
