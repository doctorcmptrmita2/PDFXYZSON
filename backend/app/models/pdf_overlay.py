"""PDF overlay metadata model (optional for future use)."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models.base import Base


class PDFOverlay(Base):
    """PDF overlay metadata for tracking edits (optional for v1)."""

    __tablename__ = "pdf_overlays"

    id = Column(Integer, primary_key=True, index=True)
    pdf_document_id = Column(Integer, ForeignKey("pdf_documents.id"), nullable=False)
    page_number = Column(Integer, nullable=False)
    block_id = Column(String, nullable=False)
    original_text = Column(Text)
    edited_text = Column(Text)
    bbox_x0 = Column(Integer)
    bbox_y0 = Column(Integer)
    bbox_x1 = Column(Integer)
    bbox_y1 = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    pdf_document = relationship("PDFDocument", backref="overlays")

