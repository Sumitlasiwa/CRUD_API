from pydantic import BaseModel
from typing import Literal

class Input(BaseModel):
    title: str
    done: Literal[0,1]

class Output(BaseModel):
    id: int
    title: str
    done: Literal[0,1]

class Stats(BaseModel):
    total_tasks: int
    completed_tasks: int
    pending_tasks: int