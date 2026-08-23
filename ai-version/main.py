"""
To-Do List CRUD REST API -- FastAPI entry point.

This file is intentionally tiny:

* It creates the ``FastAPI`` application instance.
* It runs one-time bootstrap (schema creation + initial seed) on startup.
* It mounts the HTTP router that lives in ``app/routes/task_routes.py``.

All SQL is in ``app/repositories/task_repository.py``; all business logic is in
``app/services/task_service.py``.

Run locally:
    uvicorn main:app --reload

Then open http://127.0.0.1:8000/docs for the interactive Swagger UI.
"""

from fastapi import FastAPI

from CRUD_API.app.db import database
from CRUD_API.app.repositories import task_repository
from app.routes import task_routes


app = FastAPI(
    title="To-Do List API",
    description="A simple CRUD REST API for a To-Do List, built with FastAPI.",
    version="1.1.0",
)


@app.on_event("startup")
def on_startup() -> None:
    """Create the schema (if needed) and seed the database on first boot.

    ``seed_if_empty`` is a no-op once any row exists, so calling it on every
    startup is safe and idempotent.
    """
    database.init_db()
    task_repository.seed_if_empty()


# Mount all the HTTP routes under the default prefix.
app.include_router(task_routes.router)
