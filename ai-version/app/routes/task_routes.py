"""
HTTP routes for the To-Do List API.

The route layer is intentionally thin:

* parses the HTTP request,
* delegates the work to the service layer (never to the repository),
* shapes the response via the Pydantic models below.

No SQL or filesystem access is performed here -- the data lives in
``app/services/task_service.py``.
"""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Query, status
from pydantic import BaseModel, Field

from app.services import task_service


router = APIRouter()


# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------
class Task(BaseModel):
    """Response model: how a task is shaped when returned to the client.

    ``created_at`` and ``updated_at`` are surfaced as ISO 8601 strings, the
    same format used internally by the SQLite repository.
    """
    id: int
    title: str
    done: bool = False
    created_at: str
    updated_at: str


class TaskCreate(BaseModel):
    """Request model for ``POST /tasks``.

    The client provides only ``title`` (and optionally ``done``); the server
    assigns the ``id`` and timestamps.
    """
    # ``min_length=1`` rejects empty strings -- FastAPI returns 422.
    title: str = Field(..., min_length=1, description="Title cannot be empty")
    done: bool = False


class TaskUpdate(BaseModel):
    """Request model for ``PUT /tasks/{task_id}``.

    The client must send the full updated task (``title`` + ``done``). The
    ``id`` comes from the URL, never from the body.
    """
    title: str = Field(..., min_length=1, description="Title cannot be empty")
    done: bool


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@router.get(
    "/tasks",
    response_model=List[Task],
    status_code=status.HTTP_200_OK,
)
def list_tasks(
    title: Optional[str] = Query(
        default=None,
        description="Case-insensitive substring filter applied to the title.",
    ),
    done: Optional[str] = Query(
        default=None,
        description=(
            "Filter by completion status. Accepts 0, 1, true, false "
            "(case-insensitive)."
        ),
    ),
    order_by: Optional[str] = Query(
        default=None,
        description="Sort field. Supported values: 'title' (asc), '-title' (desc).",
    ),
):
    """Return tasks, optionally filtered and sorted."""
    return task_service.list_tasks(title=title, done=done, order_by=order_by)


@router.get(
    "/tasks/reset",
    include_in_schema=False,  # keep reset reachable but out of Swagger to avoid confusion
)
@router.post(
    "/tasks/reset",
    status_code=status.HTTP_200_OK,
)
def reset_tasks():
    """Wipe the table and re-insert the 3 seed tasks with fresh timestamps."""
    result = task_service.reset_tasks()
    return {"message": "tasks reset", **result}


@router.get(
    "/tasks/{task_id}",
    response_model=Task,
    status_code=status.HTTP_200_OK,
)
def get_task(task_id: int):
    """Return a single task by its ID, or 404 if it does not exist."""
    return task_service.get_task(task_id)


@router.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
)
def create_task(payload: TaskCreate):
    """Create a new task. The server assigns the ``id`` and timestamps."""
    return task_service.create_task(title=payload.title, done=payload.done)


@router.put(
    "/tasks/{task_id}",
    response_model=Task,
    status_code=status.HTTP_200_OK,
)
def update_task(task_id: int, payload: TaskUpdate):
    """Replace an existing task; ``created_at`` is preserved."""
    return task_service.update_task(
        task_id=task_id, title=payload.title, done=payload.done
    )


@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(task_id: int):
    """Delete a task. Returns 204 No Content on success."""
    task_service.delete_task(task_id)
    return None
