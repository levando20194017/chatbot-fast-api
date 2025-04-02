import logging
import os
from app.api.api_v1.api import api_router
from app.api.openapi.api import router as openapi_router
from app.core.config import settings
# from app.core.minio import init_minio
from app.startup.migarate import DatabaseMigrator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

origins = [
    "http://localhost:3000",  # Nếu FE chạy trên React/Next.js cổng 3000
    os.getenv(
        "BACKEND_CORS_ORIGINS"
    ),  # Thay thế bằng domain thật của FE
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Cho phép các domain này gọi API
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả phương thức (GET, POST, PUT, DELETE, ...)
    allow_headers=["*"],  # Cho phép tất cả headers
)

# Include routers
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(openapi_router, prefix="/openapi")


# @app.on_event("startup")
# async def startup_event():
#     # Initialize MinIO
#     init_minio()
#     # Run database migrations
#     migrator = DatabaseMigrator(settings.get_database_url)
#     migrator.run_migrations()


@app.get("/")
def root():
    return {"message": "Welcome to RAG Web UI API"}


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.VERSION,
    }
