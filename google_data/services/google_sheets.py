from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from ..utils.parse_gform import fetch_normalized_rows, fetch_supervisor_rows
from ..utils.utils import resolve_service_account_path


                                                                     
def ensure_service_account_file(path: str) -> str:
    """Проверяет доступность файла сервисного аккаунта и возвращает его путь."""
    resolved = resolve_service_account_path(path)
    if not Path(resolved).exists():
        raise FileNotFoundError(f"SERVICE_ACCOUNT_FILE not found: {resolved}")
    return resolved


                                                        
def google_tls_preflight() -> None:
    """Проверяет возможность HTTPS-подключения к API Google."""
    try:
        import requests

        requests.get("https://www.googleapis.com/generate_204", timeout=5)
    except Exception:
        return


                                                         
def load_student_rows(
    spreadsheet_id: str,
    *,
    sheet_name: Optional[str],
    service_account_file: str,
) -> List[Dict[str, Any]]:
    """Загружает строки студентов из Google Sheet с нормализацией полей."""
    return fetch_normalized_rows(
        spreadsheet_id=spreadsheet_id,
        sheet_name=sheet_name,
        service_account_file=service_account_file,
    )


                                                          
def load_supervisor_rows(
    spreadsheet_id: str,
    *,
    sheet_name: Optional[str],
    service_account_file: str,
) -> List[Dict[str, Any]]:
    """Возвращает нормализованные данные наставников из таблицы."""
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
