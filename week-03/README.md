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

This starts the Task API and PostgreSQL together. The API is available at `http://localhost:8000`, and PostgreSQL data is saved in the `taskdata` Docker volume. The volume keeps database data outside the PostgreSQL container's temporary filesystem. This means tasks remain available when the container is stopped and started again.

To stop the stack, press `Ctrl+C`, then run:

```bash
docker compose down
```


A load balancer periodically calls the /health endpoint and sends traffic only to healthy API instances.


slim only uses required dependencies at run

IMAGE                   ID             DISK USAGE   CONTENT SIZE   
task-api-before:slim   7ec26b85d6f7       2.05GB          528MB       
task-api-after:slim    7fac5a69f58f        648MB          154MB 