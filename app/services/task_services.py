"""Service layer for task business logic and validation."""

from random import randrange
from fastapi import HTTPException, status
from app.schemas.task_schemas import Input
from app.repositories import task_repository


def create_task(input: Input):
    """Validate task input and create a new task."""
    if not input.title:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="title should not be empty!")

    input_dict = input.model_dump()
    input_dict["id"] = randrange(0, 1000000)

    return task_repository.create_task(input_dict)


def get_tasks(done: str | None = None, search: str | None = None):
    """Return tasks filtered by done status or title search."""
    if done is not None and search is None:
        done_bool = done.lower() == "true"
        return task_repository.get_tasks_by_done(done_bool)

    if search is not None and done is None:
        return task_repository.get_tasks_by_search(search)

    if done is not None and search is not None:
        done_bool = done.lower() == "true"
        return task_repository.get_tasks_by_done_and_search(done_bool, search)

    return task_repository.get_tasks()


def get_stats():
    """Compute summary statistics for tasks."""
    total_tasks = task_repository.get_total_tasks()
    completed_tasks = task_repository.get_completed_tasks()
    pending_tasks = total_tasks - completed_tasks
    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks
    }


def reset_tasks():
    """Reset stored tasks to the initial seeded set."""
    return task_repository.reset_tasks()


def get_task(id: int):
    """Get a task by ID or raise 404 if not found."""
    result = task_repository.search_task(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={ "error": f"Task {id} not found" })

    _, task = result
    return task


def update_task(id: int, input: Input):
    """Update an existing task by ID."""
    result = task_repository.search_task(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={ "error": f"Task {id} not found" })

    updated_task = input.model_dump()
    updated_task["id"] = id
    return task_repository.update_task(result[0], updated_task)


def delete_task(id: int):
    """Delete a task by ID and return a confirmation."""
    result = task_repository.search_task(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {id} not found!")

    task_repository.delete_task(result[0])
    return f"successfully deleted task {id} !"
