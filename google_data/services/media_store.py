from __future__ import annotations

import mimetypes
import os
import re
from pathlib import Path
from typing import Optional, Tuple

import requests

MEDIA_ROOT = Path(os.getenv("MEDIA_ROOT", "/data/media")).resolve()


                                                           
def _ensure_media_root() -> Path:
    """Создаёт директорию хранения медиафайлов при первом обращении."""
    MEDIA_ROOT.mkdir(parents=True, exist_ok=True)
    return MEDIA_ROOT


                                                          
def _normalize_drive_url(url: str) -> str:
    """Преобразует ссылку Google Drive в прямой URL для скачивания."""
    match = re.search(r"[?&]id=([A-Za-z0-9_-]+)", url)
    if match:
        return f"https://drive.google.com/uc?export=download&id={match.group(1)}"
    match = re.search(r"/file/d/([A-Za-z0-9_-]+)/", url)
    if match:
        return f"https://drive.google.com/uc?export=download&id={match.group(1)}"
    return url


                                                             
def _guess_filename(url: str, content_disposition: Optional[str]) -> str:
    """Определяет имя скачиваемого файла по заголовку ответа или адресу."""
    if content_disposition:
        encoded = re.search(r"filename\\*=UTF-8''([^;]+)", content_disposition)
        if encoded:
            return encoded.group(1)
        quoted = re.search(r'filename="?([^";]+)"?', content_disposition)
        if quoted:
            return quoted.group(1)
    name = url.split("?")[0].rstrip("/").split("/")[-1]
    return name or "file"


                                            
def _safe_name(name: str) -> str:
    """Очищает имя файла от лишних символов и ограничивает длину."""
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", name)
    return safe[:200]


                                                         
def persist_media_from_url(conn, owner_user_id: Optional[int], url: str, category: str = "cv") -> Tuple[int, str]:
    """Скачивает файл, сохраняет его локально и регистрирует запись в базе."""
    if not url or not url.strip():
        raise ValueError("empty url")
    url = url.strip()
    if "drive.google.com" in url:
        url = _normalize_drive_url(url)

    _ensure_media_root()

    response = requests.get(url, stream=True, timeout=30)
    response.raise_for_status()
    content_type = response.headers.get("Content-Type") or "application/octet-stream"
    filename = _safe_name(_guess_filename(url, response.headers.get("Content-Disposition")))
    if not os.path.splitext(filename)[1]:
        extension = mimetypes.guess_extension(content_type) or ""
        if extension:
            filename = f"{filename}{extension}"

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO media_files(owner_user_id, object_key, provider, mime_type, size_bytes, created_at)
            VALUES (%s, %s, 'local', %s, NULL, now())
            RETURNING id
            """,
            (owner_user_id, "", content_type),
        )
        media_id = cur.fetchone()[0]

    key = f"{category}/{media_id}_{filename}"
    path = _ensure_media_root() / key
    path.parent.mkdir(parents=True, exist_ok=True)

    size = 0
    with open(path, "wb") as handle:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                handle.write(chunk)
                size += len(chunk)

    with conn.cursor() as cur:
        cur.execute(
            "UPDATE media_files SET object_key=%s, size_bytes=%s WHERE id=%s",
            (key, size, media_id),
        )

    public_path = f"/media/{media_id}"
    return media_id, public_path


__all__ = ["persist_media_from_url", "MEDIA_ROOT"]
