"""PDF text map schemas."""
from typing import List, Optional
from pydantic import BaseModel


class BBox(BaseModel):
    """Bounding box coordinates."""

    x0: float
    y0: float
    x1: float
    y1: float


class Word(BaseModel):
    """Word with bounding box and content."""

    id: str  # e.g., "page-1-block-3-word-5"
    text: str
    bbox: BBox
    block_id: str  # Parent block ID


class TextBlock(BaseModel):
    """Text block with bounding box and content."""

    id: str  # e.g., "page-1-block-3"
    page_number: int  # 1-based page number
    bbox: BBox
    text: str
    words: Optional[List[Word]] = None  # Word-level data


class TextMapResponse(BaseModel):
    """Response schema for page text map."""

    pdf_uuid: str
    page_number: int
    page_width: float  # Page width in PDF coordinate space
    page_height: float  # Page height in PDF coordinate space
    blocks: List[TextBlock]


class BlockEditRequest(BaseModel):
    """Request schema for editing a text block."""

    new_text: str

