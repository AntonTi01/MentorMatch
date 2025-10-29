from __future__ import annotations

import os
from typing import Optional

import psycopg2
from psycopg2.extensions import connection


def build_db_dsn() -> str:
    dsn = os.getenv("DATABASE_URL")
    if dsn:
        return dsn
    user = os.getenv("POSTGRES_USER", "mentormatch")
    password = os.getenv("POSTGRES_PASSWORD", "secret")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "mentormatch")
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"


def get_conn() -> connection:
    return psycopg2.connect(build_db_dsn())


__all__ = ["build_db_dsn", "get_conn"]
