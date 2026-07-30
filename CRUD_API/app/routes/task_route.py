"""Task route definitions and HTTP API endpoints."""

from fastapi import status, APIRouter
from app.schemas import task_schemas
from app.services import task_services
from app.db.database import SessionDep

task_router = APIRouter()

@task_router.post("/tasks", status_code=status.HTTP_201_CREATED, response_model=task_schemas.Output)
def create_task(input: task_schemas.Input, session: SessionDep):
    """Create a new task from the request body."""
    return task_services.create_task(input, session)

@task_router.get("/tasks", status_code=status.HTTP_200_OK, response_model=list[task_schemas.Output])
def get_tasks(session: SessionDep, done: int | None = None, search: str | None = None):
    """Return a list of tasks filtered by optional query params."""
    return task_services.get_tasks(session, done, search)

@task_router.get("/tasks/stats",status_code=status.HTTP_200_OK, response_model=task_schemas.Stats)
def get_stats(session: SessionDep):
    """Get task completion statistics."""
    return task_services.get_stats(session)

@task_router.get("/tasks/reset", status_code=status.HTTP_200_OK, response_model=dict)
def reset_tasks(session: SessionDep):
    """Reset tasks to the seeded initial state."""
    return task_services.reset_tasks(session)

@task_router.get("/tasks/{id}", status_code=status.HTTP_200_OK, response_model=task_schemas.Output)
def get_task(id: int, session: SessionDep):
    """Return a single task by ID."""
    return task_services.get_task(id, session)

@task_router.put("/tasks/{id}", status_code=status.HTTP_200_OK, response_model=task_schemas.Output)
def update_task(id: int, input: task_schemas.Input, session: SessionDep):
    return task_services.update_task(id, input, session)
    
@task_router.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_task(id: int, session: SessionDep):
    return task_services.delete_task(id, session)

@task_router.delete("/tasks", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_all_tasks(session: SessionDep):
    """Delete all tasks from the database."""
    return task_services.delete_all_tasks(session)