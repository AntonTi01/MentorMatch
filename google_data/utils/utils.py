from __future__ import annotations

from pathlib import Path
from typing import Optional


                                                        
def resolve_service_account_path(path: Optional[str]) -> Optional[str]:
    """Находит фактический путь к файлу сервисного аккаунта относительно проекта."""
    if not path:
        return None
    try:
        candidate = Path(path)
        if candidate.is_absolute() and candidate.exists():
            return str(candidate)
        potential_locations = [
            candidate,
            Path(__file__).parent / path,
            Path(__file__).parent.parent / path,
        ]
        for option in potential_locations:
            if option.exists():
                return str(option)
    except Exception:
        pass
    return path


__all__ = ["resolve_service_account_path"]
