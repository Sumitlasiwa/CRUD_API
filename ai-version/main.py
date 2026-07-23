"""
Simple To-Do List CRUD REST API built with FastAPI.

This is a beginner-friendly example that:
- Stores tasks in an in-memory Python list (no external database).
- Uses Pydantic models to validate request/response data.
- Exposes five CRUD endpoints: list, get, create, update, delete.

Run locally:
    uvicorn main:app --reload

Then open http://127.0.0.1:8000/docs to try the interactive Swagger UI.
"""

from typing import List, Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# FastAPI application instance
# ---------------------------------------------------------------------------
app = FastAPI(
    title="To-Do List API",
    description="A simple CRUD REST API for a To-Do List, built with FastAPI.",
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------
class Task(BaseModel):
    """Response model: how a task is shaped when returned to the client."""
    id: int
    title: str
    done: bool = False


class TaskCreate(BaseModel):
    """Request model for POST /tasks.
    The client provides only the title (and optionally `done`).
    The server assigns the `id` automatically.
    """
    # `min_length=1` rejects empty strings like "" -- FastAPI will return
    # a 422 Unprocessable Entity with a clear error message in that case.
    title: str = Field(..., min_length=1, description="Title cannot be empty")
    done: bool = False  # optional; defaults to False if the client omits it


class TaskUpdate(BaseModel):
    """Request model for PUT /tasks/{task_id}.
    The client must send the full updated task (title + done).
    The `id` is taken from the URL, not the body.
    """
    # Same validation as TaskCreate: empty titles are rejected.
    title: str = Field(..., min_length=1, description="Title cannot be empty")
    done: bool


# ---------------------------------------------------------------------------
# In-memory "database"
# ---------------------------------------------------------------------------
# A plain Python list that acts as our database. It resets every time the
# server restarts -- that is intentional and is exactly what the spec asks for.
tasks_db: List[Task] = [
    Task(id=1, title="Learn FastAPI", done=False),
    Task(id=2, title="Build CRUD API", done=True),
    Task(id=3, title="Write API documentation", done=False),
]

# A simple counter used to assign new unique IDs. Because it only ever goes up,
# we can never produce a duplicate ID.
next_id: int = 4  # one more than the largest existing ID


# ---------------------------------------------------------------------------
# Helper function
# ---------------------------------------------------------------------------
def find_task(task_id: int) -> Optional[Task]:
    """Return the task with the given ID, or None if it does not exist."""
    for task in tasks_db:
        if task.id == task_id:
            return task
    return None


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/tasks", response_model=List[Task], status_code=status.HTTP_200_OK)
def list_tasks():
    """Return every task currently stored in memory."""
    return tasks_db


@app.get("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def get_task(task_id: int):
    """Return a single task by its ID."""
    task = find_task(task_id)
    if task is None:
        # 404 with a clear, beginner-friendly message.
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    """Create a new task. The server assigns a unique `id` automatically."""
    global next_id

    new_task = Task(
        id=next_id,
        title=payload.title,
        done=payload.done,
    )
    tasks_db.append(new_task)
    next_id += 1  # prepare the ID for the next call
    return new_task


@app.put("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def update_task(task_id: int, payload: TaskUpdate):
    """Replace an existing task. The `id` from the URL is preserved."""
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")

    # Full replacement: overwrite `title` and `done` while keeping the original id.
    task.title = payload.title
    task.done = payload.done
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    """Delete a task. Returns 204 No Content on success."""
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")

    tasks_db.remove(task)
    # 204 responses must not have a body, so we simply return None.
    return None
