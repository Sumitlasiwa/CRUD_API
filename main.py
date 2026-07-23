from fastapi import FastAPI, status, HTTPException

app = FastAPI()

tasks = [
    {"id": 1, "title": "read harry potter", "done": True },
    {"id": 2, "title": "learn api dev 1 hr", "done": False },
    {"id": 3, "title": "upper body workout", "done": False }
]

@app.get("/")
async def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
def health_check():
    return { "status": "ok"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{id}")
def get_task(id: int):

    for task in tasks:
        if id == task["id"]:
            return task

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= { "error": f"Task {id} not found" })