from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.base import engine, Base, SessionLocal
from app.db.init_db import init_db
# 已修改於 2025-11-30，原因：新增所有履歷資料相關的 API 端點
from app.api.endpoints import (
    auth,
    personal_info,
    work_experience,
    projects,
    education,
    certifications,
    languages,
    publications,
    github_projects
)

# 已新增於 2025-11-30，原因：新增匯入履歷資料相關的 API 端點
from app.api.endpoints import import_data

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize database
db = SessionLocal()
try:
    init_db(db)
finally:
    db.close()

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
# 已修改於 2025-11-30，原因：新增所有履歷資料相關的路由
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
app.include_router(personal_info.router, prefix=f"{settings.API_V1_STR}/personal-info", tags=["Personal Info"])
app.include_router(work_experience.router, prefix=f"{settings.API_V1_STR}/work-experience", tags=["Work Experience"])
app.include_router(projects.router, prefix=f"{settings.API_V1_STR}/projects", tags=["Projects"])
app.include_router(education.router, prefix=f"{settings.API_V1_STR}/education", tags=["Education"])
app.include_router(certifications.router, prefix=f"{settings.API_V1_STR}/certifications", tags=["Certifications"])
app.include_router(languages.router, prefix=f"{settings.API_V1_STR}/languages", tags=["Languages"])
app.include_router(publications.router, prefix=f"{settings.API_V1_STR}/publications", tags=["Publications"])
app.include_router(github_projects.router, prefix=f"{settings.API_V1_STR}/github-projects", tags=["GitHub Projects"])

# 已新增於 2025-11-30，原因：新增匯入履歷資料相關的路由
app.include_router(import_data.router, prefix=f"{settings.API_V1_STR}/import", tags=["Import"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Resume Management System API",
        "version": settings.VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
