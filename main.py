from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()

tasks = [
    {"id": 1, "title": "read harry potter", "done": True },
    {"id": 2, "title": "learn api dev 1 hr", "done": False },
    {"id": 3, "title": "upper body workout", "done": False }
]

class Input(BaseModel):
    title: str
    done: bool = False

    
@app.get("/")
async def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
def health_check():
    return { "status": "ok"}

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(input: Input):

    if not input.title:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="title should not be empty!")
    
    input_dict = input.model_dump()
    input_dict["id"] = randrange(0, 1000000)
    tasks.append(input_dict)
    return {"data": input_dict}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{id}")
def get_task(id: int):

    for task in tasks:
        if id == task["id"]:
            return task

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= { "error": f"Task {id} not found" })