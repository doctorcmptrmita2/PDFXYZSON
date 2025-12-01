"""PDF page schemas."""
from pydantic import BaseModel


class PageImageResponse(BaseModel):
    """Response schema for page image (binary PNG)."""

    # This is typically returned as StreamingResponse, but can be used for metadata
    pass

