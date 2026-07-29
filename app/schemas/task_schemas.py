from pydantic import BaseModel
from typing import Literal
from datetime import datetime

class Input(BaseModel):
    title: str
    done: Literal[0,1]

class Output(BaseModel):
    id: int
    title: str
    done: Literal[0,1]
    created_at: datetime
    updated_at: datetime

class Stats(BaseModel):
    total_tasks: int
    completed_tasks: int
    pending_tasks: int