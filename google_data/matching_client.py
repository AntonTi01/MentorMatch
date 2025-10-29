from __future__ import annotations

import logging
import os
from typing import Any, Dict

import httpx

MATCHING_SERVICE_URL = os.getenv("MATCHING_SERVICE_URL", "http://matching:8300")
logger = logging.getLogger(__name__)


def _post(path: str, payload: Dict[str, Any]) -> None:
    url = f"{MATCHING_SERVICE_URL.rstrip('/')}{path}"
    try:
        response = httpx.post(url, json=payload, timeout=30)
        response.raise_for_status()
    except Exception as exc:  # pragma: no cover - network failure logged
        logger.warning("Matching service call to %s failed: %s", url, exc)


def refresh_student_embedding(student_user_id: int) -> None:
    _post("/api/embeddings/student/refresh", {"student_user_id": student_user_id})


def refresh_supervisor_embedding(supervisor_user_id: int) -> None:
    _post("/api/embeddings/supervisor/refresh", {"supervisor_user_id": supervisor_user_id})


def refresh_topic_embedding(topic_id: int) -> None:
    _post("/api/embeddings/topic/refresh", {"topic_id": topic_id})


def refresh_role_embedding(role_id: int) -> None:
    _post("/api/embeddings/role/refresh", {"role_id": role_id})


__all__ = [
    "refresh_student_embedding",
    "refresh_supervisor_embedding",
    "refresh_topic_embedding",
    "refresh_role_embedding",
]
