from __future__ import annotations

import logging
import os
from typing import Any, Dict, Optional

import httpx

GOOGLE_DATA_SERVICE_URL = os.getenv("GOOGLE_DATA_SERVICE_URL", "http://google_data:8200")
logger = logging.getLogger(__name__)


def _post(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    url = f"{GOOGLE_DATA_SERVICE_URL.rstrip('/')}{path}"
    try:
        response = httpx.post(url, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()
    except Exception as exc:  # pragma: no cover
        logger.warning("Google Data service POST %s failed: %s", url, exc)
        return {"status": "error", "message": str(exc)}


def sync_roles_sheet(*, spreadsheet_id: Optional[str] = None, service_account_file: Optional[str] = None) -> bool:
    payload: Dict[str, Any] = {}
    if spreadsheet_id:
        payload["spreadsheet_id"] = spreadsheet_id
    if service_account_file:
        payload["service_account_file"] = service_account_file
    result = _post("/api/export/pairs", payload)
    return result.get("status") == "ok"


__all__ = ["sync_roles_sheet"]
