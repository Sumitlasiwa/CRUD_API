"""Task repository for database operations."""

from app.schemas.task_schemas import Input
from sqlmodel import Session
from sqlalchemy import text


SEED_TASKS = [
    {"title": "Learn FastAPI", "done": 0},
    {"title": "Build CRUD API", "done": 1},
    {"title": "Learn SQLModel", "done": 0},
]


def search_task(id: int, session: Session):
    """Find a task by ID and return its index and object."""
    sql = text("SELECT * FROM task WHERE id = :id")
    result = session.exec(sql, {"id": id}).fetchone()
    if result:
        return result
    return None

def create_task(input: Input, session: Session):
    """Add a new task to the in-memory task list."""
    sql = text("INSERT INTO task (title, done) VALUES (:title, :done) RETURNING *")
    result = session.exec(sql, {"title": input.title, "done": input.done}).fetchone()
    session.commit()
    return result

def get_tasks_by_done(done: int, session: Session):
    sql = text("SELECT * FROM task WHERE done = :done")
    return session.exec(sql, {"done": done}).fetchall()

def get_tasks_by_search(search: str, session: Session):
    sql = text("SELECT * FROM task WHERE title LIKE :search")
    return session.exec(sql, {"search": f"%{search}%"}).fetchall()

def get_tasks_by_done_and_search(done: int, search: str, session: Session):
    sql = text("SELECT * FROM task WHERE done = :done AND title LIKE :search")
    return session.exec(sql, {"done": done, "search": f"%{search}%"}).fetchall()


def get_tasks(session: Session):
    sql = text("SELECT * FROM task")
    return session.exec(sql).all()

def get_total_tasks(session: Session):
    sql = text("SELECT COUNT(*) FROM task")
    return session.exec(sql).fetchone()[0]

def get_completed_tasks(session: Session):
    sql = text("SELECT COUNT(*) FROM task WHERE done = :done")
    return session.execute(sql, {"done": 1}).fetchone()[0]

def reset_tasks(session: Session):
    session.exec(text("DELETE FROM task"))
    for task in SEED_TASKS:
        session.execute(text("INSERT INTO task (title, done) VALUES (:title, :done)"), task)
    session.commit()
    

def update_task(id: int, input: Input, session: Session):
    sql = text("UPDATE task SET title = :title, done = :done WHERE id = :id RETURNING *")
    result = session.exec(sql, {"title": input.title, "done": input.done, "id": id}).fetchone()
    session.commit()
    return result

def delete_task(id: int, session: Session):
    sql = text("DELETE FROM task WHERE id = :id")
    session.exec(sql, {"id": id})
    session.commit()

def delete_all_tasks(session: Session):
    sql = text("DELETE FROM task")
    session.exec(sql)
    session.commit()