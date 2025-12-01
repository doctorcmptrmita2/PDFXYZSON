"""PDF processing engine using PyMuPDF."""
import logging
from pathlib import Path
from typing import List

import fitz  # PyMuPDF

from app.schemas.pdf_text_map import TextBlock, BBox, Word
from app.services.storage import PDFStorageService

logger = logging.getLogger(__name__)


class PDFEngine:
    """PDF processing engine using PyMuPDF."""

    def __init__(self, storage_service: PDFStorageService):
        """
        Initialize PDF engine.

        Args:
            storage_service: Storage service instance
        """
        self.storage = storage_service

    def get_page_count(self, pdf_path: Path) -> int:
        """
        Get total number of pages in PDF.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Number of pages
        """
        doc = fitz.open(pdf_path)
        try:
            return len(doc)
        finally:
            doc.close()

    def render_page_to_png(
        self, pdf_path: Path, page_number: int, zoom: float = 2.0
    ) -> bytes:
        """
        Render a PDF page to PNG bytes.

        Args:
            pdf_path: Path to PDF file
            page_number: Page number (1-based)
            zoom: Zoom factor for rendering (default: 2.0)

        Returns:
            PNG image bytes
        """
        doc = fitz.open(pdf_path)
        try:
            if page_number < 1 or page_number > len(doc):
                raise ValueError(f"Invalid page number: {page_number}")

            page = doc[page_number - 1]  # Convert to 0-based index
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            png_bytes = pix.tobytes("png")
            return png_bytes
        finally:
            doc.close()

    def extract_text_map(
        self, pdf_path: Path, page_number: int
    ) -> tuple[List[TextBlock], float, float]:
        """
        Extract text map (blocks with bounding boxes) from a PDF page.

        This method uses PyMuPDF's block extraction to identify text regions.
        Each block is treated independently - no multi-column layout inference.

        Args:
            pdf_path: Path to PDF file
            page_number: Page number (1-based)

        Returns:
            List of text blocks with bounding boxes

        Raises:
            ValueError: If page_number is out of range
        """
        doc = fitz.open(pdf_path)
        try:
            if page_number < 1 or page_number > len(doc):
                raise ValueError(f"Invalid page number: {page_number}")

            page = doc[page_number - 1]  # Convert to 0-based index
            page_rect = page.rect
            page_width = page_rect.width
            page_height = page_rect.height

            blocks = page.get_text("blocks")

            text_blocks = []
            block_index = 0

            for block in blocks:
                # PyMuPDF block format: (x0, y0, x1, y1, "text", block_no, block_type, ...)
                if len(block) >= 5 and isinstance(block[4], str):
                    x0, y0, x1, y1 = float(block[0]), float(block[1]), float(block[2]), float(block[3])
                    text = block[4]

                    # Normalize text: strip trailing newlines and whitespace
                    text = text.rstrip()

                    # Only include non-empty blocks with valid bounding boxes
                    if text and x1 > x0 and y1 > y0:
                        block_index += 1
                        block_id = f"page-{page_number}-block-{block_index}"
                        
                        # Extract words with bounding boxes
                        words = self._extract_words_from_block(
                            page, block_id, text, x0, y0, x1, y1, page_number
                        )
                        
                        text_blocks.append(
                            TextBlock(
                                id=block_id,
                                page_number=page_number,
                                bbox=BBox(x0=x0, y0=y0, x1=x1, y1=y1),
                                text=text,
                                words=words if words else None,
                            )
                        )

            # Return tuple with page dimensions (will be used in API route)
            return text_blocks, page_width, page_height
        finally:
            doc.close()

    def apply_block_edit(
        self,
        pdf_path: Path,
        page_number: int,
        block_bbox: BBox,
        new_text: str,
        *,
        font_name: str = "helv",
        font_size: float = 11.0,
        padding: float = 1.0,
        line_spacing: float = 1.2,
    ) -> None:
        """
        Apply a block edit using overlay approach.

        This method performs a visual overlay edit:
        1. Draws a white rectangle over the original block region (with padding)
        2. Word-wraps the new text to fit within the block width
        3. Draws the wrapped text lines inside the block region

        Note: This is NOT a low-level PDF content stream rewrite.
        We are visually overriding the original block region.

        Args:
            pdf_path: Path to PDF file (will be overwritten)
            page_number: Page number (1-based)
            block_bbox: Bounding box of the block to edit
            new_text: New text content (empty string allowed - will white-out only)
            font_name: Font name (default: "helv")
            font_size: Font size in points (default: 11.0)
            padding: Internal padding within block (default: 1.0)
            line_spacing: Line spacing multiplier (default: 1.2)

        Raises:
            ValueError: If page_number is out of range or bbox is invalid
        """
        doc = fitz.open(pdf_path)
        try:
            if page_number < 1 or page_number > len(doc):
                raise ValueError(f"Invalid page number: {page_number}")

            page = doc[page_number - 1]

            # Validate bbox
            if block_bbox.x1 <= block_bbox.x0 or block_bbox.y1 <= block_bbox.y0:
                raise ValueError(f"Invalid bounding box: {block_bbox}")

            # Calculate padded rectangle for white-out (extend outward slightly)
            whiteout_x0 = block_bbox.x0 - padding
            whiteout_y0 = block_bbox.y0 - padding
            whiteout_x1 = block_bbox.x1 + padding
            whiteout_y1 = block_bbox.y1 + padding

            # Draw white rectangle to cover original text
            whiteout_rect = fitz.Rect(whiteout_x0, whiteout_y0, whiteout_x1, whiteout_y1)
            page.draw_rect(whiteout_rect, color=(1, 1, 1), fill=(1, 1, 1))

            # If new_text is empty, just white-out and return
            if not new_text or not new_text.strip():
                doc.save(pdf_path, incremental=False)
                return

            # Calculate internal text area (with padding inside block)
            text_x0 = block_bbox.x0 + padding
            text_y0 = block_bbox.y0 + padding
            text_x1 = block_bbox.x1 - padding
            text_y1 = block_bbox.y1 - padding

            # Ensure valid text area
            if text_x1 <= text_x0 or text_y1 <= text_y0:
                logger.warning(f"Text area too small for block {block_bbox}, attempting minimal draw")
                text_x0 = block_bbox.x0
                text_y0 = block_bbox.y0
                text_x1 = block_bbox.x1
                text_y1 = block_bbox.y1

            available_width = text_x1 - text_x0
            available_height = text_y1 - text_y0

            # Word-wrap text to fit block width
            wrapped_lines = self._word_wrap_text(
                page, new_text, available_width, font_name, font_size
            )

            # Draw wrapped lines
            line_height = font_size * line_spacing
            current_y = text_y0 + font_size  # Start below top padding

            for line in wrapped_lines:
                # Stop if we exceed available height
                if current_y > text_y1:
                    break

                # Draw line
                point = fitz.Point(text_x0, current_y)
                page.insert_text(
                    point,
                    line,
                    fontname=font_name,
                    fontsize=font_size,
                    color=(0, 0, 0),
                )
                current_y += line_height

            # Save modified PDF (overwrite original)
            doc.save(pdf_path, incremental=False)
        finally:
            doc.close()

    def _word_wrap_text(
        self,
        page: fitz.Page,
        text: str,
        max_width: float,
        font_name: str,
        font_size: float,
    ) -> List[str]:
        """
        Word-wrap text to fit within a given width.

        Handles explicit newlines (\n) as line breaks and word-wraps
        each paragraph independently.

        Args:
            page: PyMuPDF page object
            text: Text to wrap (may contain explicit newlines)
            max_width: Maximum width in points
            font_name: Font name
            font_size: Font size in points

        Returns:
            List of wrapped lines
        """
        if not text:
            return [""]

        # Split by explicit newlines first
        paragraphs = text.split("\n")
        all_lines = []

        for paragraph in paragraphs:
            # Normalize whitespace: collapse multiple spaces to single space
            paragraph = " ".join(paragraph.split())

            if not paragraph:
                # Empty paragraph becomes empty line
                all_lines.append("")
                continue

            # Word-wrap this paragraph
            words = paragraph.split()
            current_line = []

            for word in words:
                # Test if adding this word would exceed width
                test_line = " ".join(current_line + [word])
                text_width = page.get_text_length(
                    test_line, fontname=font_name, fontsize=font_size
                )

                if text_width <= max_width:
                    current_line.append(word)
                else:
                    # Current line is full, start new line
                    if current_line:
                        all_lines.append(" ".join(current_line))
                    current_line = [word]

            # Add remaining words as last line
            if current_line:
                all_lines.append(" ".join(current_line))

        return all_lines if all_lines else [""]

    def _extract_words_from_block(
        self,
        page: fitz.Page,
        block_id: str,
        block_text: str,
        block_x0: float,
        block_y0: float,
        block_x1: float,
        block_y1: float,
        page_number: int,
    ) -> List[Word]:
        """
        Extract words with bounding boxes from a text block.

        Args:
            page: PyMuPDF page object
            block_id: Block identifier
            block_text: Block text content
            block_x0, block_y0, block_x1, block_y1: Block bounding box
            page_number: Page number (1-based)

        Returns:
            List of words with bounding boxes
        """
        try:
            # Get ALL words from the page (not clipped) to avoid missing words
            all_words = page.get_text("words")
            
            words = []
            word_index = 0
            
            # Expand block bounds slightly to catch words on edges
            margin = 2.0
            expanded_x0 = block_x0 - margin
            expanded_y0 = block_y0 - margin
            expanded_x1 = block_x1 + margin
            expanded_y1 = block_y1 + margin
            
            for word_data in all_words:
                # PyMuPDF word format: (x0, y0, x1, y1, "word", block_no, line_no, word_no)
                if len(word_data) >= 5:
                    wx0, wy0, wx1, wy1 = float(word_data[0]), float(word_data[1]), float(word_data[2]), float(word_data[3])
                    word_text = word_data[4].strip()
                    
                    # Check if word is within or overlaps the block bounds
                    word_center_x = (wx0 + wx1) / 2
                    word_center_y = (wy0 + wy1) / 2
                    
                    # Include word if its center is within expanded block bounds
                    if (word_text and 
                        wx1 > wx0 and wy1 > wy0 and
                        expanded_x0 <= word_center_x <= expanded_x1 and
                        expanded_y0 <= word_center_y <= expanded_y1):
                        word_index += 1
                        # Use coordinate-based ID for better reliability
                        word_id = f"{block_id}-word-{int(wx0)}-{int(wy0)}-{word_index}"
                        words.append(
                            Word(
                                id=word_id,
                                text=word_text,
                                bbox=BBox(x0=wx0, y0=wy0, x1=wx1, y1=wy1),
                                block_id=block_id,
                            )
                        )
            
            # Sort words by position (top to bottom, left to right)
            words.sort(key=lambda w: (w.bbox.y0, w.bbox.x0))
            
            # Re-assign sequential IDs after sorting
            for idx, word in enumerate(words, 1):
                word.id = f"{block_id}-word-{idx}"
            
            return words
        except Exception as e:
            logger.warning(f"Failed to extract words from block {block_id}: {e}")
            return []

    def apply_word_edit(
        self,
        pdf_path: Path,
        page_number: int,
        word_bbox: BBox,
        new_text: str,
        *,
        font_name: str = "helv",
        font_size: float = None,
        padding: float = 2.0,
    ) -> None:
        """
        Apply a word-level edit by overlaying new text over the original word.

        This method performs a visual overlay edit:
        1. Draws a white rectangle over the original word region (with padding)
        2. Draws the new text at the word position

        Args:
            pdf_path: Path to PDF file (will be overwritten)
            page_number: Page number (1-based)
            word_bbox: Bounding box of the word to edit
            new_text: New text content
            font_name: Font name (default: "helv")
            font_size: Font size in points (auto-detected if None)
            padding: Internal padding around word (default: 2.0)

        Raises:
            ValueError: If page_number is out of range or bbox is invalid
        """
        doc = fitz.open(pdf_path)
        try:
            if page_number < 1 or page_number > len(doc):
                raise ValueError(f"Invalid page number: {page_number}")

            page = doc[page_number - 1]

            # Validate bbox
            if word_bbox.x1 <= word_bbox.x0 or word_bbox.y1 <= word_bbox.y0:
                raise ValueError(f"Invalid bounding box: {word_bbox}")

            # Auto-detect font size from word height if not provided
            if font_size is None:
                word_height = word_bbox.y1 - word_bbox.y0
                # Estimate font size from height (typically font_size ≈ height * 0.8)
                font_size = max(word_height * 0.8, 8.0)  # Minimum 8pt
                logger.debug(f"Auto-detected font size: {font_size} from word height: {word_height}")

            # Calculate padded rectangle for white-out (more padding for better coverage)
            whiteout_x0 = word_bbox.x0 - padding
            whiteout_y0 = word_bbox.y0 - padding
            whiteout_x1 = word_bbox.x1 + padding
            whiteout_y1 = word_bbox.y1 + padding

            # Draw white rectangle to cover original word
            whiteout_rect = fitz.Rect(whiteout_x0, whiteout_y0, whiteout_x1, whiteout_y1)
            page.draw_rect(whiteout_rect, color=(1, 1, 1), fill=(1, 1, 1))

            # If new_text is empty, just white-out and return
            if not new_text or not new_text.strip():
                doc.save(pdf_path, incremental=False)
                return

            # Calculate text position (baseline) - PyMuPDF uses bottom-left origin
            # y0 is bottom of word, so we place text at y0
            text_x = word_bbox.x0
            text_y = word_bbox.y0  # Baseline is at bottom of bbox

            # Draw new text
            point = fitz.Point(text_x, text_y)
            page.insert_text(
                point,
                new_text.strip(),
                fontname=font_name,
                fontsize=font_size,
                color=(0, 0, 0),
            )

            # Save modified PDF
            doc.save(pdf_path, incremental=False)
        finally:
            doc.close()

