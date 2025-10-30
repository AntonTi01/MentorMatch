from __future__ import annotations

from typing import Any, Optional

def parse_optional_int(value: Optional[Any]) -> Optional[int]:
    """Пытается привести значение к целому числу, возвращая ``None`` при пустом вводе."""
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    s = str(value).strip()
    if not s:
        return None
    try:
        return int(s)
    except (TypeError, ValueError):
        return None


def normalize_optional_str(value: Optional[Any]) -> Optional[str]:
    """Очищает строку от пробелов и преобразует пустые значения в ``None``."""
    if value is None:
        return None
    if isinstance(value, str):
        stripped = value.strip()
    else:
        stripped = str(value).strip()
    return stripped or None

