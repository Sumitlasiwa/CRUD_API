"""Application entrypoint and router registration for the Task API."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import Session

from app.db.database import create_db_and_tables, engine
from app.routes.task_route import task_router
from app.services import task_services



@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run once on application startup, before serving any request.

    We open a Session manually here because FastAPI's `Depends` system
    only resolves session injection for HTTP request handlers -- not for
    application startup events. The old `@app.on_event("startup")` API
    would silently receive no real session, which is why seeding never
    reliably ran. The lifespan context manager is the supported way.
    """
    # 1. Make sure the tables exist.
    create_db_and_tables()

    # 2. Seed initial data if the table is empty.
    with Session(engine) as session:
        task_services.populate_seed_tasks(session)

    yield  # <-- application is now ready and starts serving requests


app = FastAPI(lifespan=lifespan)

# Register task routes under the main FastAPI application.
app.include_router(task_router)

@app.get("/")
async def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }




