from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from ..utils.parse_gform import fetch_normalized_rows, fetch_supervisor_rows
from ..utils.utils import resolve_service_account_path


# Проверяет существование файла сервисного аккаунта и возвращает путь
def ensure_service_account_file(path: str) -> str:
    resolved = resolve_service_account_path(path)
    if not Path(resolved).exists():
        raise FileNotFoundError(f"SERVICE_ACCOUNT_FILE not found: {resolved}")
    return resolved


# Выполняет быстрый запрос к Google API для прогрева TLS
def google_tls_preflight() -> None:
    try:
        import requests

        requests.get("https://www.googleapis.com/generate_204", timeout=5)
    except Exception:
        return


# Загружает строки со студентами из таблицы Google Sheets
def load_student_rows(
    spreadsheet_id: str,
    *,
    sheet_name: Optional[str],
    service_account_file: str,
) -> List[Dict[str, Any]]:
    return fetch_normalized_rows(
        spreadsheet_id=spreadsheet_id,
        sheet_name=sheet_name,
        service_account_file=service_account_file,
    )


# Загружает строки с наставниками из таблицы Google Sheets
def load_supervisor_rows(
    spreadsheet_id: str,
    *,
    sheet_name: Optional[str],
    service_account_file: str,
) -> List[Dict[str, Any]]:
    return fetch_supervisor_rows(
        spreadsheet_id=spreadsheet_id,
        sheet_name=sheet_name,
        service_account_file=service_account_file,
    )


__all__ = [
    "ensure_service_account_file",
    "google_tls_preflight",
    "load_student_rows",
    "load_supervisor_rows",
]
