"""
SQLite database access layer.

This module is intentionally tiny: it knows how to open a SQLite connection
to the project-local ``tasks.db`` file and how to create the ``tasks`` table
the first time the application starts.

The repository layer (see ``app/repositories/task_repository.py``) is the only
place that issues raw SQL statements; this module only owns the *connection*
and the *schema bootstrap*.
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

# Path of this file: .../ai-version/app/db/database.py
# The SQLite database file lives in the ``ai-version`` folder.
_THIS_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _THIS_DIR.parent.parent  # .../ai-version
DB_PATH = _PROJECT_ROOT / "tasks.db"


def get_connection() -> sqlite3.Connection:
    """Return a new SQLite connection.

    A fresh connection is opened per call so that FastAPI's threadpool can
    safely share the database without extra locking. ``check_same_thread=False``
    is set because FastAPI's worker threads may differ from the one that
    first opened the file.
    """
    conn = sqlite3.connect(
        DB_PATH,
        check_same_thread=False,
        # ``isolation_level=None`` enables SQLite's "autocommit" mode so that
        # we control transactions explicitly with BEGIN/COMMIT when needed.
        isolation_level=None,
    )
    conn.row_factory = sqlite3.Row  # rows behave like dicts; column access by name
    # Enforce foreign keys (future-proofing; the schema doesn't currently use them).
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db() -> None:
    """Create the ``tasks`` table if it does not already exist.

    Called once at application startup. The statement is idempotent thanks to
    ``IF NOT EXISTS``.
    """
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS tasks (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        title      TEXT    NOT NULL,
        done       INTEGER NOT NULL DEFAULT 0 CHECK (done IN (0, 1)),
        created_at TEXT    NOT NULL,
        updated_at TEXT    NOT NULL
    );
    """
    conn = get_connection()
    try:
        conn.execute(create_table_sql)
    finally:
        conn.close()


# Allow ``python -m`` style usage during local debugging.
if __name__ == "__main__":  # pragma: no cover
    init_db()
    print(f"Database initialized at: {DB_PATH}")
