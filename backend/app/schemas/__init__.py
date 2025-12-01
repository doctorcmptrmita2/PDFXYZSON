"""Pydantic schemas for API requests and responses."""
from app.schemas.pdf_document import PDFDocumentCreate, PDFDocumentResponse
from app.schemas.pdf_page import PageImageResponse
from app.schemas.pdf_text_map import BBox, TextBlock, TextMapResponse, BlockEditRequest

__all__ = [
    "PDFDocumentCreate",
    "PDFDocumentResponse",
    "PageImageResponse",
    "BBox",
    "TextBlock",
    "TextMapResponse",
    "BlockEditRequest",
]

