# To-Do List CRUD API (FastAPI)

A simple RESTful To-Do List API built with **FastAPI** that uses an **in-memory database**. It supports all basic CRUD (Create, Read, Update, Delete) operations for managing tasks.

## Features

- Create a new task
- Retrieve all tasks
- Calculate tasks stats
- Reset to inital tasks
- Retrieve a task by ID
- Update an existing task
- Delete a task
- Interactive Swagger UI documentation
- In-memory storage (no external database required)

---

## Installation

### Clone the repository

```bash
git clone https://github.com/Sumitlasiwa/FlyRank_Backend.git
cd CRUD_API
```

### Create and activate a virtual environment (Linux)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the development server:

```bash
fastapi dev main.py
```

or, if using Uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at:

- **API:** http://127.0.0.1:8000/
- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

---

## Example Request

### Create a Task

```bash
curl -X POST http://localhost:8000/tasks \
-H "Content-Type: application/json" \
-d '{"title":"Buy milk"}'
```

### Example Response

```json
{
  "data": {
    "id": 769639,
    "title": "Buy milk",
    "done": false
  }
}
```

---

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/tasks` | Create a new task |
| GET | `/tasks` | Retrieve all tasks |
| GET | `/tasks/stats` | Give tasks stats |
| GET | `/tasks/reset` | Reset to inital tasks |
| GET | `/tasks/{id}` | Retrieve a task by ID |
| PUT | `/tasks/{id}` | Update an existing task |
| DELETE | `/tasks/{id}` | Delete a task |



---

## API Documentation

After starting the server, open the interactive Swagger UI:

**http://127.0.0.1:8000/docs**

This interface allows you to test all CRUD endpoints directly from your browser.

---

## Screenshots

### Swagger UI

![Swagger UI](image.png)

---

## Tech Stack

- Python 3
- FastAPI
- Uvicorn
- Pydantic

---

## Notes

- This project uses an **in-memory database**, so all tasks are lost when the server is restarted.
- It is intended for learning and demonstration purposes.


## AI vs Me

 - clean comments and documentations
 - More Schemas with strong field validation
 - database created as List of pydantic objects rather than dictionaries

## Prompt used:
Create a simple and beginner-friendly CRUD REST API for a To-Do List application using FastAPI.

Requirements:
- Use FastAPI and Pydantic.
- Do NOT use any external database (SQLite, PostgreSQL, MongoDB, etc.).
- Store data in an in-memory Python list that acts as the database.
- Initialize the database with these three sample tasks:

[
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build CRUD API", "done": True},
    {"id": 3, "title": "Write API documentation", "done": False}
]

Task model:
- id: int
- title: str
- done: bool

API Endpoints:
1. GET /tasks
   - Return all tasks.
   - Status code: 200 OK

2. GET /tasks/{task_id}
   - Return a single task by ID.
   - Return 404 Not Found if the task does not exist.

3. POST /tasks
   - Create a new task.
   - The client should provide only:
       - title
       - done (optional, default=False)
   - The server should automatically generate a unique integer ID.
   - Return the created task.
   - Status code: 201 Created.

4. PUT /tasks/{task_id}
   - Replace the entire task except for its ID.
   - Return the updated task.
   - Return 404 if the task is not found.
   - Status code: 200 OK.

5. DELETE /tasks/{task_id}
   - Delete the specified task.
   - Return 204 No Content.
   - Return 404 if the task does not exist.

Implementation requirements:
- Create separate Pydantic schemas for:
  - Task (response model)
  - TaskCreate (request model for POST)
  - TaskUpdate (request model for PUT)
- Use response_model for appropriate endpoints.
- Use HTTPException with meaningful error messages.
- Use appropriate HTTP status codes throughout.
- Keep the code clean, readable, and well-commented.
- Avoid unnecessary abstractions or complex patterns.
- Write everything in a single `main.py` file.
- Ensure the code follows FastAPI best practices and is easy for beginners to understand.
 