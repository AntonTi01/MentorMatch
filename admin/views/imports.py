from __future__ import annotations

import os
import urllib.parse
from typing import Optional

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from ..clients.google_data_client import import_students, import_supervisors, sync_roles_sheet
from ..context import AdminContext


def register(router: APIRouter, ctx: AdminContext) -> None:
    @router.get('/import-sheet')
    def import_sheet(request: Request, target: Optional[str] = None, sheet_name: Optional[str] = None):
        spreadsheet_id = (os.getenv('SPREADSHEET_ID') or '').strip()
        if not spreadsheet_id:
            notice = urllib.parse.quote('Не указан идентификатор таблицы SPREADSHEET_ID')
            return RedirectResponse(url=f'/?tab=students&msg={notice}', status_code=303)

        desired = (target or 'students').strip().lower()
        try:
            if desired == 'supervisors':
                result = import_supervisors(spreadsheet_id, sheet_name)
                tab = 'supervisors'
            else:
                result = import_students(spreadsheet_id, sheet_name)
                tab = 'students'
        except Exception as exc:  # pragma: no cover - network failures
            detail = urllib.parse.quote(f'Ошибка импорта: {type(exc).__name__}: {exc}')
            return RedirectResponse(url=f'/?tab={tab}&msg={detail}', status_code=303)

        sync_roles_sheet()
        message = result.get('message') or 'Импорт завершён'
        quoted = urllib.parse.quote(message)
        return RedirectResponse(url=f'/?tab={tab}&msg={quoted}', status_code=303)
