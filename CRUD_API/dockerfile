# Stage 1: Build dependencies
FROM python:3.14 AS builder

WORKDIR /app

RUN pip install uv

COPY requirements.txt .

RUN uv pip install --system -r requirements.txt


# Stage 2: Runtime image
FROM python:3.14-slim

WORKDIR /app

COPY --from=builder /usr/local /usr/local

COPY . .

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]