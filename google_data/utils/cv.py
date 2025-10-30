from __future__ import annotations

from pathlib import Path
from typing import Optional

from psycopg2.extensions import connection

from ..services.media_store import MEDIA_ROOT
from .text_extract import extract_text_from_file


                                                                    
def resolve_cv_text(conn: connection, cv_value: Optional[str]) -> Optional[str]:
    """Возвращает текстовое содержимое резюме по ссылке из базы."""
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

    header = f"CV (D,D� �,D�D1D�D� {Path(file_path).name}):\n"
    return (header + text)[:20000]


__all__ = ["resolve_cv_text"]
