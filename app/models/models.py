from sqlmodel import SQLModel, Field
from typing import Literal

class Task(SQLModel, table=True):
    """Database model for a task."""
    __tablename__ = "task"
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(..., nullable=False)
    done: Literal[0, 1] = Field(default=0, nullable=False)