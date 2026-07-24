from pydantic import BaseModel

class Input(BaseModel):
    title: str
    done: bool = False

class Output(BaseModel):
    id: int
    title: str
    done: bool

class Stats(BaseModel):
    total_tasks: int
    completed_tasks: int
    pending_tasks: int