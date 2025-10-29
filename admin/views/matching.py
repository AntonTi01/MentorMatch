from __future__ import annotations

import urllib.parse
from typing import Optional

from fastapi import APIRouter, Form
from fastapi.responses import RedirectResponse

from ..clients.matching_client import match_role, match_student, match_supervisor, match_topic
from ..context import AdminContext


def _status_message(result) -> str:
    if result.get('status') == 'ok':
        return '?????? ????????'
    return result.get('message') or '?????? ???????'


def register(router: APIRouter, ctx: AdminContext) -> None:  # ctx kept for interface consistency
    @router.post('/do-match-role')
    def do_match_role(role_id: int = Form(...)):
        result = match_role(role_id)
        notice = urllib.parse.quote(_status_message(result))
        return RedirectResponse(url=f'/role/{role_id}?msg={notice}', status_code=303)

    @router.post('/do-match-topic')
    def do_match_topic(topic_id: int = Form(...), target_role: Optional[str] = Form(None)):
        result = match_topic(topic_id, target_role=target_role)
        notice = urllib.parse.quote(_status_message(result))
        return RedirectResponse(url=f'/topic/{topic_id}?msg={notice}', status_code=303)

    @router.post('/do-match-student')
    def do_match_student(student_user_id: int = Form(...)):
        result = match_student(student_user_id)
        notice = urllib.parse.quote(_status_message(result))
        return RedirectResponse(url=f'/user/{student_user_id}?msg={notice}', status_code=303)

    @router.post('/do-match-supervisor')
    def do_match_supervisor(supervisor_user_id: int = Form(...)):
        result = match_supervisor(supervisor_user_id)
        notice = urllib.parse.quote(_status_message(result))
        return RedirectResponse(url=f'/supervisor/{supervisor_user_id}?msg={notice}', status_code=303)
