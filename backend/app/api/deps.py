"""API dependencies."""
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.storage import PDFStorageService
from app.services.pdf_engine import PDFEngine
from app.core.config import settings


def get_storage_service() -> PDFStorageService:
    """Get PDF storage service instance."""
    return PDFStorageService(
        base_dir=settings.STORAGE_DIR,
        pdf_dir=settings.PDF_DIR,
        render_dir=settings.RENDER_DIR,
    )


def get_pdf_engine() -> PDFEngine:
    """Get PDF engine instance."""
    storage = get_storage_service()
    return PDFEngine(storage)

