"""
Service layer for tasks.

This module sits between the HTTP routes and the SQL repository. Its job is:

* parse / validate inputs that don't belong in the Pydantic request schemas
  (e.g. query-string flags like ``done=1`` or sort directives like ``-title``);
* orchestrate repository calls;
* raise ``HTTPException`` with the same status codes the original in-memory
  API used (404 for missing rows, 422 for invalid input).

No SQL is issued from this layer; that lives entirely in the repository.
"""

from __future__ import annotations

from typing import Optional

from fastapi import HTTPException, status

from CRUD_API.app.repositories import task_repository


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------
def _parse_done(raw: Optional[str]) -> Optional[bool]:
    """Translate the ``done`` query string into a real ``bool``.

    Accepts (case-insensitive): ``"0"``, ``"1"``, ``"true"``, ``"false"``.
    Returns ``None`` when the parameter was not supplied at all.
    Raises ``HTTPException(422)`` for anything else.
    """
    if raw is None:
        return None
    lowered = raw.strip().lower()
    if lowered in {"0", "false"}:
        return False
    if lowered in {"1", "true"}:
        return True
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=(
            "Invalid value for 'done'. Expected one of: 0, 1, true, false "
            "(case-insensitive)."
        ),
    )


def _validate_order_by(raw: Optional[str]) -> Optional[str]:
    """Allow-list check for the ``order_by`` query parameter.

    Only ``"title"`` (ascending) and ``"-title"`` (descending) are accepted.
    Anything else, including unknown column names, results in a 422 -- matching
    the validation style used elsewhere in the API.
    """
    if raw is None:
        return None
    if raw not in task_repository.SORT_COLUMN_MAP:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                "Invalid value for 'order_by'. "
                "Supported values: 'title', '-title'."
            ),
        )
    return raw


def _coerce_bool(value) -> bool:
    """Safely coerce ``value`` to ``bool``.

    SQLite stores booleans as integers (0/1), so this helper makes sure
    we never accidentally return ``0``/``1`` to the Pydantic response model.
    """
    return bool(value)


# ---------------------------------------------------------------------------
# Public service API used by the route layer
# ---------------------------------------------------------------------------
def list_tasks(
    *,
    title: Optional[str] = None,
    done: Optional[str] = None,
    order_by: Optional[str] = None,
) -> list[dict]:
    """Return tasks filtered/sorted according to the validated inputs."""
    parsed_done = _parse_done(done)
    validated_order_by = _validate_order_by(order_by)

    rows = task_repository.list_tasks(
        title=title,
        done=parsed_done,
        order_by=validated_order_by,
    )

    # Make sure ``done`` is a real Python bool so Pydantic accepts it cleanly.
    for row in rows:
        row["done"] = _coerce_bool(row["done"])
    return rows


def get_task(task_id: int) -> dict:
    """Return a single task or raise ``HTTPException(404)``."""
    row = task_repository.get_task(task_id)
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
    row["done"] = _coerce_bool(row["done"])
    return row


def create_task(*, title: str, done: bool) -> dict:
    """Persist a new task and return the freshly stored row."""
    row = task_repository.create_task(title=title, done=done)
    row["done"] = _coerce_bool(row["done"])
    return row


def update_task(*, task_id: int, title: str, done: bool) -> dict:
    """Persist an updated task or raise ``HTTPException(404)``."""
    row = task_repository.update_task(task_id=task_id, title=title, done=done)
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
    row["done"] = _coerce_bool(row["done"])
    return row


def delete_task(task_id: int) -> None:
    """Remove a task or raise ``HTTPException(404)``."""
    removed = task_repository.delete_task(task_id)
    if not removed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )


def reset_tasks() -> dict:
    """Wipe the table and re-insert the 3 seed rows with fresh timestamps.

    Returns a small payload describing what happened.
    """
    deleted = task_repository.delete_all_tasks()
    inserted = task_repository.seed_if_empty()
    return {"deleted": deleted, "inserted": inserted}
