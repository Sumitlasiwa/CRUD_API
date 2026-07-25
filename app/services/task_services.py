"""Service layer for task business logic and validation."""

from fastapi import HTTPException, status
from app.schemas.task_schemas import Input
from app.repositories import task_repository
from sqlmodel import Session
from typing import Literal


def create_task(input: Input, session: Session):
    """Validate task input and create a new task."""
    if not input.title:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="title should not be empty!")

    new_input = Input(**input.model_dump())

    return task_repository.create_task(new_input, session)


def get_tasks(session: Session, done: int | None = None, search: str | None = None):
    """Return tasks filtered by done status or title search."""
    if done is not None and search is None:
        return task_repository.get_tasks_by_done(done, session)

    if search is not None and done is None:
        return task_repository.get_tasks_by_search(search, session)

    if done is not None and search is not None:
        return task_repository.get_tasks_by_done_and_search(done, search, session)

    return task_repository.get_tasks(session)


def get_stats(session: Session):
    """Compute summary statistics for tasks."""
    total_tasks = task_repository.get_total_tasks(session)
    completed_tasks = task_repository.get_completed_tasks(session)
    pending_tasks = total_tasks - completed_tasks
    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks
    }


def reset_tasks(session: Session):
    """Reset stored tasks to the initial seeded set."""
    task_repository.reset_tasks(session)
    return {"message": "All tasks have been reset!"}

def get_task(id: int, session: Session):
    """Get a task by ID or raise 404 if not found."""
    result = task_repository.search_task(id, session)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={ "error": f"Task {id} not found" })
    return task_repository.search_task(id, session)


def update_task(id: int, input: Input, session: Session):
    """Update an existing task by ID."""
    result = task_repository.search_task(id, session)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={ "error": f"Task {id} not found" })

    updated_task = Input(**input.model_dump())
    return task_repository.update_task(id, updated_task, session)


def delete_task(id: int, session: Session):
    """Delete a task by ID and return a confirmation."""
    result = task_repository.search_task(id, session)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {id} not found!")

    task_repository.delete_task(id, session)
    # Return no body; route is configured with 204 No Content
    return None

def delete_all_tasks(session: Session):
    """Delete all tasks from the database."""
    task_repository.delete_all_tasks(session)
    # Return no body; route is configured with 204 No Content
    return None

def populate_seed_tasks(session: Session):
    """Populate the database with initial seed tasks if no tasks exist initially."""
    total = task_repository.get_total_tasks(session)
    # Log so you can see in the startup output whether seeding actually ran.
    print(f"[seed] tasks in DB at startup: {total}")
    if total == 0:
        task_repository.reset_tasks(session)
        return {"message": "Seeded initial tasks."}
    return {"message": "Tasks already exist. No seeding performed."}