"""Helpers for resolving CV text content."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from psycopg2.extensions import connection

from .text_extract import extract_text_from_file

MEDIA_ROOT = Path(
    os.getenv("MEDIA_ROOT", str(Path(__file__).resolve().parents[1] / "data" / "media"))
).resolve()
MEDIA_ROOT.mkdir(parents=True, exist_ok=True)


def resolve_cv_text(conn: connection, cv_value: Optional[str]) -> Optional[str]:
    value = (cv_value or "").strip()
    if not value:
        return None
    if not value.startswith("/media/"):
        return value

    try:
        media_id = int(value.split("/")[-1])
    except Exception:
        return value

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT object_key, mime_type FROM media_files WHERE id=%s", (media_id,))
            row = cur.fetchone()
    except Exception:
        return value

    if not row:
        return value

    object_key, mime_type = row
    file_path = (MEDIA_ROOT / object_key).resolve()
    try:
        text = extract_text_from_file(file_path, mime_type)
    except Exception:
        return value

    if not text:
        return value

    header = f"CV (из файла {Path(file_path).name}):\n"
    return (header + text)[:20000]


__all__ = ["resolve_cv_text"]
