from __future__ import annotations

from typing import Dict, List, Tuple

from clients.matching_client import (
    refresh_role_embedding,
    refresh_student_embedding,
    refresh_supervisor_embedding,
    refresh_topic_embedding,
)

_queue_store: Dict[int, List[Tuple[str, int]]] = {}


def _drain_queue(conn) -> List[Tuple[str, int]]:
    return list(_queue_store.pop(id(conn), []))


def enqueue_refresh(conn, kind: str, entity_id: int) -> None:
    queue = _queue_store.setdefault(id(conn), [])
    queue.append((kind, entity_id))


def commit_with_refresh(conn) -> None:
    conn.commit()
    queue = _drain_queue(conn)
    for kind, entity_id in queue:
        if kind == "student":
            refresh_student_embedding(entity_id)
        elif kind == "supervisor":
            refresh_supervisor_embedding(entity_id)
        elif kind == "topic":
            refresh_topic_embedding(entity_id)
        elif kind == "role":
            refresh_role_embedding(entity_id)


__all__ = ["enqueue_refresh", "commit_with_refresh"]
