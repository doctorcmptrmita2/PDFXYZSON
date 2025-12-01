"""FastAPI application entry point."""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import init_db
from app.api.routes import pdfs, pdf_operations

app = FastAPI(
    title="AeroPdf API",
    description="Block-based PDF editing engine API with 50+ operations",
    version="1.0.0",
    debug=settings.DEBUG,
)

# Configure CORS
# Get allowed origins from environment or use defaults
import os
allowed_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3001,http://127.0.0.1:3001,http://localhost:3000,http://127.0.0.1:3000"
).split(",")

# Add production domains if set
production_domain = os.getenv("FRONTEND_DOMAIN")
if production_domain:
    allowed_origins.extend([
        f"https://{production_domain}",
        f"http://{production_domain}",
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in allowed_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(pdfs.router, prefix="/api")
app.include_router(pdf_operations.router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    # Initialize database
    init_db()

    # Ensure storage directories exist (handled by Settings)
    print("AeroPdf API started successfully")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AeroPdf API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

