from __future__ import annotations

import os
from typing import Callable, Optional

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from psycopg2.extensions import connection

from ..services.google_sheets import (
    ensure_service_account_file,
    google_tls_preflight,
    load_supervisor_rows,
)
from ..workflows.topic_import import import_supervisors


class ImportSupervisorsPayload(BaseModel):
    spreadsheet_id: str
    sheet_name: Optional[str] = None
    service_account_file: Optional[str] = None


# Создает и настраивает роутер для импорта данных наставников
def create_supervisors_import_router(get_conn: Callable[[], connection]) -> APIRouter:
    router = APIRouter()

    # Обрабатывает запрос на импорт наставников из Google Sheets
    @router.post("/api/import/supervisors", response_class=JSONResponse)
    def import_supervisors_endpoint(payload: ImportSupervisorsPayload):
        try:
            service_account_file = ensure_service_account_file(
                payload.service_account_file or os.getenv("SERVICE_ACCOUNT_FILE", "service-account.json")
            )
        except FileNotFoundError as exc:
            return JSONResponse({"status": "error", "message": str(exc)}, status_code=400)

        google_tls_preflight()
        rows = load_supervisor_rows(
            spreadsheet_id=payload.spreadsheet_id,
            sheet_name=payload.sheet_name,
            service_account_file=service_account_file,
        )

        rows_list = list(rows)
        with get_conn() as conn:
            result = import_supervisors(conn, rows_list)
        result.setdefault("stats", {})["total_rows_in_sheet"] = len(rows_list)
        return JSONResponse(result)

    return router


__all__ = ["create_supervisors_import_router", "ImportSupervisorsPayload"]
