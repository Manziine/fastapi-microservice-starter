from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app, Counter, Histogram
import time

from app.api.v1 import auth, users, items
from app.core.config import settings

# Prometheus metrics
REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"])
REQUEST_DURATION = Histogram("http_request_duration_seconds", "HTTP request duration")

def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        description="Production-ready FastAPI microservice with JWT auth, Redis caching, and PostgreSQL.",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Request timing middleware
    @application.middleware("http")
    async def add_metrics(request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        REQUEST_DURATION.observe(duration)
        return response

    # Include routers
    application.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
    application.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
    application.include_router(items.router, prefix="/api/v1/items", tags=["Items"])

    # Mount Prometheus metrics endpoint
    metrics_app = make_asgi_app()
    application.mount("/metrics", metrics_app)

    @application.get("/health", tags=["Health"])
    async def health_check():
        return {"status": "healthy", "service": settings.PROJECT_NAME}

    return application

app = create_application()
