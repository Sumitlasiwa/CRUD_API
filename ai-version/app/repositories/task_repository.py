"""
Raw-SQL repository for the ``tasks`` table.

This module is the **only** place in the codebase that issues SQL statements.
All queries are written explicitly (no ORM, no query builder) and every
user-supplied value is passed via ``?`` parameter binding -- never via string
interpolation -- so that SQL injection is structurally impossible.

Each public function opens and closes its own connection so the layer is
safe to use from FastAPI's worker threads.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from CRUD_API.app.db.database import get_connection


# ---------------------------------------------------------------------------
# Allowed sort columns. Anything outside this map is rejected by the service
# layer, so a hostile client cannot inject an arbitrary ``ORDER BY`` clause.
# ---------------------------------------------------------------------------
SORT_COLUMN_MAP = {
    "title": "title ASC",
    "-title": "title DESC",
}

# Initial seed rows. Used by ``seed_if_empty`` and by the reset endpoint.
SEED_TASKS: list[tuple[str, bool]] = [
    ("Learn FastAPI", False),
    ("Build CRUD API", True),
    ("Write API documentation", False),
]


def _now_utc_iso() -> str:
    """Return the current UTC time formatted as an ISO 8601 string.

    Using UTC keeps timestamps stable regardless of where the server runs;
    ISO 8601 is a SQLite-friendly textual representation.
    """
    return datetime.now(timezone.utc).isoformat()


def _row_to_dict(row: Any) -> dict:
    """Convert a ``sqlite3.Row`` to a plain dict for the service / route layer."""
    return {key: row[key] for key in row.keys()}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def count_tasks() -> int:
    """Return the number of rows currently in ``tasks``."""
    conn = get_connection()
    try:
        cur = conn.execute("SELECT COUNT(*) AS n FROM tasks;")
        row = cur.fetchone()
        return int(row["n"])
    finally:
        conn.close()


def seed_if_empty() -> int:
    """Insert the 3 seed rows *only* if the table is currently empty.

    Returns the number of rows inserted (0 or 3). Existing data is left
    untouched -- this is what makes startup seeding safe to run on every boot.
    """
    if count_tasks() > 0:
        return 0

    now = _now_utc_iso()
    insert_sql = (
        "INSERT INTO tasks (title, done, created_at, updated_at) "
        "VALUES (?, ?, ?, ?);"
    )
    conn = get_connection()
    try:
        for title, done in SEED_TASKS:
            conn.execute(insert_sql, (title, 1 if done else 0, now, now))
    finally:
        conn.close()
    return len(SEED_TASKS)


def list_tasks(
    *,
    title: Optional[str] = None,
    done: Optional[bool] = None,
    order_by: Optional[str] = None,
) -> list[dict]:
    """Return tasks matching the given filters, sorted as requested.

    Parameters
    ----------
    title:
        When provided, only tasks whose title contains this substring
        (case-insensitive) are returned.
    done:
        When provided, only tasks whose ``done`` flag matches this boolean.
    order_by:
        One of ``"title"`` (ascending) or ``"-title"`` (descending).
        The service layer validates this value before we reach here.

    All filtering values are bound with ``?`` placeholders.
    """
    sql = "SELECT id, title, done, created_at, updated_at FROM tasks"
    where_clauses: list[str] = []
    params: list[Any] = []

    if title is not None:
        # ``LOWER(title) LIKE LOWER(?)`` gives case-insensitive substring matching.
        where_clauses.append("LOWER(title) LIKE LOWER(?)")
        params.append(f"%{title}%")

    if done is not None:
        where_clauses.append("done = ?")
        params.append(1 if done else 0)

    if where_clauses:
        sql += " WHERE " + " AND ".join(where_clauses)

    # ``order_by`` was validated upstream; the lookup is safe.
    if order_by is not None:
        sql += " ORDER BY " + SORT_COLUMN_MAP[order_by]

    sql += ";"

    conn = get_connection()
    try:
        cur = conn.execute(sql, params)
        rows = cur.fetchall()
    finally:
        conn.close()

    return [_row_to_dict(r) for r in rows]


def get_task(task_id: int) -> Optional[dict]:
    """Return a single task by id, or ``None`` if it does not exist."""
    conn = get_connection()
    try:
        cur = conn.execute(
            "SELECT id, title, done, created_at, updated_at FROM tasks WHERE id = ?;",
            (task_id,),
        )
        row = cur.fetchone()
    finally:
        conn.close()

    return _row_to_dict(row) if row is not None else None


def create_task(*, title: str, done: bool) -> dict:
    """Insert a new task and return the persisted row.

    ``created_at`` and ``updated_at`` are set to the same timestamp at the
    moment of creation; ``updated_at`` will be refreshed on every update.
    """
    now = _now_utc_iso()
    insert_sql = (
        "INSERT INTO tasks (title, done, created_at, updated_at) "
        "VALUES (?, ?, ?, ?);"
    )
    conn = get_connection()
    try:
        cur = conn.execute(insert_sql, (title, 1 if done else 0, now, now))
        new_id = cur.lastrowid
    finally:
        conn.close()

    # ``lastrowid`` is guaranteed to be set after a successful INSERT.
    return {
        "id": int(new_id),
        "title": title,
        "done": done,
        "created_at": now,
        "updated_at": now,
    }


def update_task(*, task_id: int, title: str, done: bool) -> Optional[dict]:
    """Replace ``title`` and ``done`` for the given task.

    ``updated_at`` is refreshed to the current time; ``created_at`` is left
    alone. Returns the new row, or ``None`` if no row matched.
    """
    now = _now_utc_iso()
    update_sql = (
        "UPDATE tasks "
        "SET title = ?, done = ?, updated_at = ? "
        "WHERE id = ?;"
    )
    conn = get_connection()
    try:
        cur = conn.execute(update_sql, (title, 1 if done else 0, now, task_id))
        if cur.rowcount == 0:
            return None
        # Re-read so the response includes the freshly persisted timestamps.
        cur = conn.execute(
            "SELECT id, title, done, created_at, updated_at FROM tasks WHERE id = ?;",
            (task_id,),
        )
        row = cur.fetchone()
    finally:
        conn.close()

    return _row_to_dict(row) if row is not None else None


def delete_task(task_id: int) -> bool:
    """Delete a single task. Returns ``True`` if a row was removed."""
    conn = get_connection()
    try:
        cur = conn.execute("DELETE FROM tasks WHERE id = ?;", (task_id,))
        return cur.rowcount > 0
    finally:
        conn.close()


def delete_all_tasks() -> int:
    """Delete every row from ``tasks``. Returns the number of rows removed."""
    conn = get_connection()
    try:
        cur = conn.execute("DELETE FROM tasks;")
        return cur.rowcount
    finally:
        conn.close()
