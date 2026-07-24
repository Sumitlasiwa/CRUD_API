"""Application entrypoint and router registration for the Task API."""

from fastapi import FastAPI
from app.routes.task import task_router

app = FastAPI()

# Register task routes under the main FastAPI application.
app.include_router(task_router)


@app.get("/")
async def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
def health_check():
    return { "status": "ok"}



