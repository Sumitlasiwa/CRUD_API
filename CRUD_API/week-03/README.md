# Week 03 — Containerize Your Stack

This week, the Task API was connected to a real PostgreSQL database and containerized with Docker.

## What was done

- Added a Docker image for the FastAPI Task API.
- Added PostgreSQL as a Docker service with persistent storage.
- Configured the API to connect to PostgreSQL through `DATABASE_URL`.
- Added Docker Compose so the API and database start together.

## Run the stack

From the project root, create your local environment file and start the full stack:

```bash
cp .env.example .env && docker compose up
```

This starts the Task API and PostgreSQL together. The API is available at `http://localhost:8000`, and PostgreSQL data is saved in the `taskdata` Docker volume.

To stop the stack, press `Ctrl+C`, then run:

```bash
docker compose down
```
