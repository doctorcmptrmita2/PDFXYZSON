"""PDF file storage service."""
from pathlib import Path
from typing import Optional

from fastapi import UploadFile


class PDFStorageService:
    """Service for managing PDF file storage."""

    def __init__(self, base_dir: str, pdf_dir: str, render_dir: str):
        """
        Initialize storage service.

        Args:
            base_dir: Base storage directory
            pdf_dir: Directory for PDF files
            render_dir: Directory for rendered page images
        """
        self.base_dir = Path(base_dir)
        self.pdf_dir = Path(pdf_dir)
        self.render_dir = Path(render_dir)

        # Ensure directories exist
        self.pdf_dir.mkdir(parents=True, exist_ok=True)
        self.render_dir.mkdir(parents=True, exist_ok=True)

    async def save_upload(self, file: UploadFile, pdf_uuid: str) -> str:
        """
        Save uploaded PDF file.

        Args:
            file: Uploaded file
            pdf_uuid: Unique identifier for the PDF

        Returns:
            Full path to saved PDF file
        """
        file_path = self.pdf_dir / f"{pdf_uuid}.pdf"

        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        return str(file_path)

    def get_pdf_path(self, pdf_uuid: str) -> Path:
        """
        Get path to PDF file.

        Args:
            pdf_uuid: Unique identifier for the PDF

        Returns:
            Path to PDF file

        Raises:
            FileNotFoundError: If PDF file doesn't exist
        """
        file_path = self.pdf_dir / f"{pdf_uuid}.pdf"
        if not file_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_uuid}")
        return file_path

    def get_render_path(self, pdf_uuid: str, page_number: int) -> Path:
        """
        Get path for rendered page image.

        Args:
            pdf_uuid: Unique identifier for the PDF
            page_number: Page number (1-based)

        Returns:
            Path to rendered PNG file
        """
        return self.render_dir / f"{pdf_uuid}_page_{page_number}.png"

