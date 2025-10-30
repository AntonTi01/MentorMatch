from __future__ import annotations

import re
from typing import Optional

from psycopg2.extensions import connection

from media_store import persist_media_from_url


def normalize_telegram_link(raw: Optional[str]) -> Optional[str]:
    """Выполняет функцию normalize_telegram_link."""
    if not raw:
        return None
    value = str(raw).strip()
    if value.startswith("@"):
        value = value[1:]
    if value.lower().startswith(("http://t.me/", "https://t.me/", "http://telegram.me/", "https://telegram.me/")):
        return value
    match = re.search(r"(?:https?://)?t(?:elegram)?\\.me/([A-Za-z0-9_]+)", value)
    if match:
        return f"https://t.me/{match.group(1)}"
    username = re.sub(r"[^A-Za-z0-9_]", "", value)
    return f"https://t.me/{username}" if username else None


def extract_telegram_username(raw: Optional[str]) -> Optional[str]:
    """Выполняет функцию extract_telegram_username."""
    if not raw:
        return None
    value = str(raw).strip()
    if value.startswith("@"):
        value = value[1:]
    match = re.search(r"(?:https?://)?t(?:elegram)?\\.me/([A-Za-z0-9_]+)", value)
    if match:
        return match.group(1)
    username = re.sub(r"[^A-Za-z0-9_]", "", value)
    return username or None


def _is_http_url(value: Optional[str]) -> bool:
    """Выполняет функцию _is_http_url."""
    return bool(value) and str(value).strip().lower().startswith(("http://", "https://"))


def process_cv(conn: connection, user_id: int, cv_value: Optional[str]) -> Optional[str]:
    """Выполняет функцию process_cv."""
    value = (cv_value or "").strip()
    if not value:
        return None
    if value.startswith("/media/"):
        return value
    if _is_http_url(value):
        try:
            _, public_url = persist_media_from_url(conn, user_id, value, category="cv")
            return public_url
        except Exception:
            return cv_value
    return cv_value


__all__ = ["normalize_telegram_link", "extract_telegram_username", "process_cv"]
