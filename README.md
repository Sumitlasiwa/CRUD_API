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