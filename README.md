# Todo API

Production-grade MVP Todo API built with FastAPI, PostgreSQL, SQLAlchemy, and JWT authentication.

## Features

- **Authenticated User System** — register, login, create/read/update/delete private todos
- **Guest System** — create and view public todos without authentication
- JWT Bearer authentication (60-minute expiry)
- bcrypt password hashing
- Alembic migrations
- Dockerized with Gunicorn + Uvicorn workers

---

## Stack

| Layer         | Technology              |
|---------------|-------------------------|
| Framework     | FastAPI                 |
| Database      | PostgreSQL 16           |
| ORM           | SQLAlchemy 2            |
| Migrations    | Alembic                 |
| Auth          | JWT (python-jose)       |
| Hashing       | bcrypt (passlib)        |
| Validation    | Pydantic v2             |
| Server        | Gunicorn + Uvicorn      |
| Container     | Docker + docker-compose |

---

## Getting Started

### 1. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and set a strong `JWT_SECRET_KEY` for production.

### 2. Start services

```bash
docker compose up --build
```

This will:
- Start PostgreSQL
- Wait for it to be healthy
- Run Alembic migrations automatically
- Start the API on `http://localhost:8000`

### 3. Explore the API

Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## API Reference

### Base URL

```
http://localhost:8000/api/v1
```

### Authentication Endpoints

| Method | Path             | Auth     | Description         |
|--------|------------------|----------|---------------------|
| POST   | /auth/register   | Public   | Register new user   |
| POST   | /auth/login      | Public   | Login, get JWT      |

### User Todo Endpoints (Protected)

| Method | Path               | Auth     | Description              |
|--------|--------------------|----------|--------------------------|
| POST   | /todos             | Required | Create a todo            |
| GET    | /todos             | Required | Get your todos           |
| PUT    | /todos/{todo_id}   | Required | Update your todo         |
| DELETE | /todos/{todo_id}   | Required | Delete your todo         |

### Guest Todo Endpoints (Public)

| Method | Path               | Auth     | Description              |
|--------|--------------------|----------|--------------------------|
| POST   | /guest/todos       | Public   | Create a guest todo      |
| GET    | /guest/todos       | Public   | View all guest todos     |

---

## Example Usage

### Register

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Jane", "last_name": "Doe", "email": "jane@example.com", "password": "secret123"}'
```

### Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "jane@example.com", "password": "secret123"}'
```

### Create Todo (Authenticated)

```bash
curl -X POST http://localhost:8000/api/v1/todos \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "body": "Milk, eggs, bread"}'
```

### Create Guest Todo

```bash
curl -X POST http://localhost:8000/api/v1/guest/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Public note", "body": "This is visible to everyone"}'
```

---

## Todo Status

Todos support two statuses, defaulting to `PENDING`:

- `PENDING`
- `COMPLETED`

Update a todo's status via the `PUT /todos/{todo_id}` endpoint.

---

## Project Structure

```
todo-api/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── routes/
│   │       │   ├── auth.py       # Auth endpoints
│   │       │   ├── todos.py      # Protected todo endpoints
│   │       │   └── guest.py      # Public guest endpoints
│   │       └── __init__.py       # Router aggregator
│   ├── core/
│   │   ├── config.py             # Environment settings
│   │   └── security.py           # JWT + bcrypt utilities
│   ├── db/
│   │   └── session.py            # DB engine + session + Base
│   ├── dependencies/
│   │   └── auth.py               # JWT auth dependency
│   ├── models/
│   │   ├── user.py               # User ORM model
│   │   └── todo.py               # Todo + GuestTodo ORM models
│   ├── schemas/
│   │   ├── auth.py               # Auth request/response schemas
│   │   └── todo.py               # Todo request/response schemas
│   ├── services/
│   │   ├── auth.py               # Auth business logic
│   │   └── todo.py               # Todo business logic
│   └── main.py                   # FastAPI app + router mount
├── migrations/
│   ├── versions/
│   │   └── 0001_initial_schema.py
│   ├── env.py
│   └── script.py.mako
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh
├── requirements.txt
└── .env.example
```

---

## Running Migrations Manually

```bash
# Inside the container
docker compose exec api alembic upgrade head

# Generate a new migration after model changes
docker compose exec api alembic revision --autogenerate -m "description"
```
