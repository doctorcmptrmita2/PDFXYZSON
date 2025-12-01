"""PDF document schemas."""
from datetime import datetime
from pydantic import BaseModel


class PDFDocumentCreate(BaseModel):
    """Schema for PDF document creation (internal use)."""

    uuid: str
    original_filename: str
    stored_path: str
    page_count: int


class PDFDocumentResponse(BaseModel):
    """Schema for PDF document API response."""

    id: int
    uuid: str
    original_filename: str
    page_count: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

