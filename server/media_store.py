from __future__ import annotations

import os
import mimetypes
import re
import uuid
from pathlib import Path
from typing import Optional, Tuple

import requests

MEDIA_ROOT = Path(os.getenv("MEDIA_ROOT", "/data/media")).resolve()


def _ensure_media_root() -> Path:
    """Выполняет функцию _ensure_media_root."""
    MEDIA_ROOT.mkdir(parents=True, exist_ok=True)
    return MEDIA_ROOT


def _normalize_drive_url(url: str) -> str:
    """Выполняет функцию _normalize_drive_url."""
    m = re.search(r"[?&]id=([A-Za-z0-9_-]+)", url)
    if m:
        return f"https://drive.google.com/uc?export=download&id={m.group(1)}"
    m = re.search(r"/file/d/([A-Za-z0-9_-]+)/", url)
    if m:
        return f"https://drive.google.com/uc?export=download&id={m.group(1)}"
    return url


def _guess_filename(url: str, content_disposition: Optional[str]) -> str:
    """Выполняет функцию _guess_filename."""
    if content_disposition:
        m = re.search(r"filename\\*=UTF-8''([^;]+)", content_disposition)
        if m:
            return m.group(1)
        m = re.search(r'filename="?([^";]+)"?', content_disposition)
        if m:
            return m.group(1)
    name = url.split("?")[0].rstrip("/").split("/")[-1]
    return name or "file"


def _safe_name(name: str) -> str:
    """Выполняет функцию _safe_name."""
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name)
    return name[:200]


def persist_media_from_url(conn, owner_user_id: Optional[int], url: str, category: str = "cv") -> Tuple[int, str]:
    """Выполняет функцию persist_media_from_url."""
    if not url or not url.strip():
        raise ValueError("empty url")
    url = url.strip()
    if "drive.google.com" in url:
        url = _normalize_drive_url(url)

    _ensure_media_root()

    resp = requests.get(url, stream=True, timeout=30)
    resp.raise_for_status()
    ctype = resp.headers.get("Content-Type") or "application/octet-stream"
    fname = _safe_name(_guess_filename(url, resp.headers.get("Content-Disposition")))
    if not os.path.splitext(fname)[1]:
        ext = mimetypes.guess_extension(ctype) or ""
        if ext:
            fname = fname + ext

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO media_files(owner_user_id, object_key, provider, mime_type, size_bytes, created_at)
            VALUES (%s, %s, 'local', %s, NULL, now())
            RETURNING id
            """,
            (owner_user_id, "", ctype),
        )
        media_id = cur.fetchone()[0]

    key = f"{category}/{media_id}_{fname}"
    path = _ensure_media_root() / key
    path.parent.mkdir(parents=True, exist_ok=True)

    size = 0
    with open(path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                size += len(chunk)

    with conn.cursor() as cur:
        cur.execute(
            "UPDATE media_files SET object_key=%s, size_bytes=%s WHERE id=%s",
            (key, size, media_id),
        )

    public = f"/media/{media_id}"
    return media_id, public
