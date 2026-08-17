# Production-Ready FastAPI Microservice

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=flat-square&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7.2-DC382D?style=flat-square&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)

**A complete, production-grade FastAPI microservice template** — not a tutorial. Built to the standards expected in real engineering teams.

</div>

---

## 🎯 What Problem This Solves

Starting a new backend service from scratch takes days of boilerplate: authentication, database setup, caching, testing, CI/CD, Docker. This template eliminates all of that — clone it and ship your feature, not your infrastructure.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      API Gateway                        │
│                   (Nginx / Traefik)                     │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                  FastAPI Application                    │
│   ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │
│   │  /auth   │  │  /users  │  │  /items (your API)   │  │
│   └────┬─────┘  └────┬─────┘  └──────────┬───────────┘  │
│        │              │                   │              │
│   ┌────▼──────────────▼───────────────────▼───────────┐  │
│   │             Business Logic Layer                  │  │
│   │     (Services, Repositories, Dependencies)        │  │
│   └────┬──────────────────────────────────┬──────────┘  │
│        │                                  │             │
│   ┌────▼────────┐                  ┌──────▼──────────┐  │
│   │ PostgreSQL  │                  │   Redis Cache   │  │
│   │  (SQLAlch.) │                  │  (Rate Limiting)│  │
│   └─────────────┘                  └─────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## ✅ Features

| Feature | Implementation |
|---|---|
| 🔐 JWT Authentication | Access + Refresh token pair, stored in Redis |
| 🚦 Rate Limiting | Per-IP limits via Redis, configurable per route |
| 🗄️ Database ORM | Async SQLAlchemy + Alembic migrations |
| 📖 Auto API Docs | Swagger UI at `/docs`, ReDoc at `/redoc` |
| 🐳 Docker Ready | `docker compose up` starts everything |
| ✅ CI/CD | GitHub Actions: test → lint → build → push |
| 📊 Metrics | Prometheus endpoint at `/metrics` |
| 🔒 Security | CORS, password hashing (bcrypt), env-based secrets |
| 🧪 Testing | pytest + httpx async test client, 80%+ coverage |

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/Manziine/fastapi-microservice-starter.git
cd fastapi-microservice-starter

# 2. Copy environment variables
cp .env.example .env

# 3. Start everything with Docker
docker compose up --build

# 4. Visit the API docs
open http://localhost:8000/docs
```

## 📁 Project Structure

```
fastapi-microservice-starter/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── auth.py          # Login, register, refresh token
│   │   │   ├── users.py         # User CRUD endpoints
│   │   │   └── items.py         # Example resource endpoints
│   │   └── deps.py              # Dependency injection (DB, current user)
│   ├── core/
│   │   ├── config.py            # Settings (pydantic-settings)
│   │   ├── security.py          # JWT creation/verification
│   │   ├── database.py          # Async SQLAlchemy engine
│   │   └── redis.py             # Redis connection pool
│   ├── models/
│   │   ├── user.py              # SQLAlchemy User model
│   │   └── item.py              # SQLAlchemy Item model
│   ├── schemas/
│   │   ├── user.py              # Pydantic request/response schemas
│   │   └── token.py             # JWT token schemas
│   ├── services/
│   │   ├── auth_service.py      # Authentication business logic
│   │   └── user_service.py      # User business logic
│   └── main.py                  # FastAPI app factory
├── alembic/                     # Database migrations
├── tests/
│   ├── conftest.py              # pytest fixtures
│   ├── test_auth.py             # Auth endpoint tests
│   └── test_users.py            # User endpoint tests
├── .github/workflows/ci.yml     # GitHub Actions CI/CD
├── docker-compose.yml           # Local dev environment
├── Dockerfile                   # Multi-stage production build
├── requirements.txt
├── .env.example
└── README.md
```

## 🔧 Environment Variables

```env
# .env.example
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/appdb
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-super-secret-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
ALGORITHM=HS256
```

## 🧪 Running Tests

```bash
# With Docker (recommended)
docker compose run --rm api pytest tests/ -v --cov=app

# Locally
pip install -r requirements-dev.txt
pytest tests/ -v --cov=app --cov-report=html
```

## 📡 Key API Endpoints

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/api/v1/auth/register` | Create account | ❌ |
| POST | `/api/v1/auth/login` | Get JWT tokens | ❌ |
| POST | `/api/v1/auth/refresh` | Refresh access token | ✅ (refresh) |
| GET | `/api/v1/users/me` | Get current user | ✅ |
| GET | `/api/v1/items/` | List items | ✅ |
| POST | `/api/v1/items/` | Create item | ✅ |
| GET | `/metrics` | Prometheus metrics | ❌ |

## 🛠️ Built By

**Arnaud Ineza Manzi** — Backend Engineer
- 📧 ainezamanzi@gmail.com
- 🔗 [LinkedIn](https://linkedin.com/in/arnaud-ineza-manzi-471221272)
- 🐙 [GitHub](https://github.com/Manziine)

---

*Licensed under MIT. Use it, fork it, ship something.*
