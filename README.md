<div align="center">

# Todo API

REST API for task management with the ability to configure deadlines, priorities, and JWT authentication.

[![GitHub](https://img.shields.io/github/license/fastapi-practices/fastapi_best_architecture)](https://github.com/rustle4/todo-project/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.14-blue)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141-009688)](https://fastapi.tiangolo.com/)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16.0%2B-%23336791)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-%23778877)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
![Docker](https://img.shields.io/badge/Docker-%232496ED?logo=docker&logoColor=white)

</div>

## Public access

- **API**: [https://todo-project.relaxdev.ru](https://todo-project.relaxdev.ru)
- **Swagger UI**: [https://todo-project.relaxdev.ru/docs](https://todo-project.relaxdev.ru/docs)

## Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.14 |
| Framework | FastAPI 0.141 |
| ORM | SQLAlchemy 2.0 (async) |
| Database | PostgreSQL 16 |
| Migrations | Alembic |
| Authentication | JWT (python-jose) |
| Hashing | Pwdlib (bcrypt) |
| Testing | Pytest + pytest-asyncio |
| Containerization | Docker + docker-compose |
| Deployment | RelaxDev |

## Quick start with Docker

```bash
docker compose up -d --build
```

Services:

- **API**: http://localhost:8000
- **PostgreSQL**: available inside the network on port 5432

## If you wwant to run this app without Docker

- Clone the repository

```bash
git clone https://github.com/your-username/todo-project.git
cd todo-project
```

- Install uv

```bash
pip install uv
```

- Install dependencies

```bash
uv sync
```

- Set up environment variables

Create a .env file in the project root:

```env
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/todo_db
SECRET_KEY=supersecretkey1234567890
```

You can also use SQLite for local development:

```env
DATABASE_URL=sqlite+aiosqlite:///./test.db
```

- Run migrations

```bash
uv run alembic upgrade head
```

- Start the server

```bash
uv run fastapi dev
```

The server will be available at: http://127.0.0.1:8000
Swagger UI: http://127.0.0.1:8000/docs