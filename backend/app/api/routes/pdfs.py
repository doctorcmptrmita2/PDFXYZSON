"""PDF management API routes."""
import uuid
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from fastapi.responses import StreamingResponse, FileResponse
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_storage_service, get_pdf_engine
from app.models.pdf_document import PDFDocument
from app.schemas.pdf_document import PDFDocumentResponse
from app.schemas.pdf_text_map import TextMapResponse, BlockEditRequest
from app.services.storage import PDFStorageService
from app.services.pdf_engine import PDFEngine

router = APIRouter(prefix="/pdfs", tags=["pdfs"])


@router.post("/", response_model=PDFDocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    storage: PDFStorageService = Depends(get_storage_service),
    engine: PDFEngine = Depends(get_pdf_engine),
):
    """
    Upload a PDF file.

    Args:
        file: PDF file to upload
        db: Database session
        storage: Storage service
        engine: PDF engine

    Returns:
        Created PDF document metadata
    """
    # Validate file type
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be a PDF",
        )

    # Generate UUID
    pdf_uuid = str(uuid.uuid4())

    # Save file
    stored_path = await storage.save_upload(file, pdf_uuid)

    # Get page count
    page_count = engine.get_page_count(Path(stored_path))

    # Create database record
    db_pdf = PDFDocument(
        uuid=pdf_uuid,
        original_filename=file.filename,
        stored_path=stored_path,
        page_count=page_count,
    )
    db.add(db_pdf)
    db.commit()
    db.refresh(db_pdf)

    return PDFDocumentResponse.model_validate(db_pdf)


@router.get("/{pdf_uuid}", response_model=PDFDocumentResponse)
def get_pdf(
    pdf_uuid: str,
    db: Session = Depends(get_db),
):
    """
    Get PDF document metadata.

    Args:
        pdf_uuid: PDF document UUID
        db: Database session

    Returns:
        PDF document metadata
    """
    db_pdf = db.query(PDFDocument).filter(PDFDocument.uuid == pdf_uuid).first()
    if not db_pdf:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"PDF not found: {pdf_uuid}",
        )
    return PDFDocumentResponse.model_validate(db_pdf)


@router.get("/{pdf_uuid}/pages/{page_number}/image")
def get_page_image(
    pdf_uuid: str,
    page_number: int,
    storage: PDFStorageService = Depends(get_storage_service),
    engine: PDFEngine = Depends(get_pdf_engine),
    db: Session = Depends(get_db),
):
    """
    Get rendered page image as PNG.

    Args:
        pdf_uuid: PDF document UUID
        page_number: Page number (1-based)
        storage: Storage service
        engine: PDF engine
        db: Database session

    Returns:
        PNG image stream
    """
    # Verify PDF exists
    db_pdf = db.query(PDFDocument).filter(PDFDocument.uuid == pdf_uuid).first()
    if not db_pdf:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"PDF not found: {pdf_uuid}",
        )

    if page_number < 1 or page_number > db_pdf.page_count:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid page number: {page_number} (max: {db_pdf.page_count})",
        )

    # Check if rendered file exists, otherwise render and save
    render_path = storage.get_render_path(pdf_uuid, page_number)
    pdf_path = storage.get_pdf_path(pdf_uuid)

    if not render_path.exists():
        png_bytes = engine.render_page_to_png(pdf_path, page_number)
        render_path.parent.mkdir(parents=True, exist_ok=True)
        render_path.write_bytes(png_bytes)

    return FileResponse(
        str(render_path),
        media_type="image/png",
        filename=f"page_{page_number}.png",
    )


@router.get("/{pdf_uuid}/pages/{page_number}/text-map", response_model=TextMapResponse)
def get_page_text_map(
    pdf_uuid: str,
    page_number: int,
    storage: PDFStorageService = Depends(get_storage_service),
    engine: PDFEngine = Depends(get_pdf_engine),
    db: Session = Depends(get_db),
):
    """
    Get text map (blocks with bounding boxes) for a page.

    Args:
        pdf_uuid: PDF document UUID
        page_number: Page number (1-based)
        storage: Storage service
        engine: PDF engine
        db: Database session

    Returns:
        Text map with blocks
    """
    # Verify PDF exists
    db_pdf = db.query(PDFDocument).filter(PDFDocument.uuid == pdf_uuid).first()
    if not db_pdf:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"PDF not found: {pdf_uuid}",
        )

    if page_number < 1 or page_number > db_pdf.page_count:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid page number: {page_number} (max: {db_pdf.page_count})",
        )

    pdf_path = storage.get_pdf_path(pdf_uuid)
    blocks, page_width, page_height = engine.extract_text_map(pdf_path, page_number)

    return TextMapResponse(
        pdf_uuid=pdf_uuid,
        page_number=page_number,
        page_width=page_width,
        page_height=page_height,
        blocks=blocks,
    )


@router.put("/{pdf_uuid}/pages/{page_number}/blocks/{block_id}", response_model=TextMapResponse)
def edit_block(
    pdf_uuid: str,
    page_number: int,
    block_id: str,
    request: BlockEditRequest,
    storage: PDFStorageService = Depends(get_storage_service),
    engine: PDFEngine = Depends(get_pdf_engine),
    db: Session = Depends(get_db),
):
    """
    Edit a text block on a page.

    Args:
        pdf_uuid: PDF document UUID
        page_number: Page number (1-based)
        block_id: Block identifier
        request: Edit request with new text
        storage: Storage service
        engine: PDF engine
        db: Database session

    Returns:
        Updated text map for the page
    """
    # Verify PDF exists
    db_pdf = db.query(PDFDocument).filter(PDFDocument.uuid == pdf_uuid).first()
    if not db_pdf:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"PDF not found: {pdf_uuid}",
        )

    if page_number < 1 or page_number > db_pdf.page_count:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid page number: {page_number} (max: {db_pdf.page_count})",
        )

    pdf_path = storage.get_pdf_path(pdf_uuid)

    # Get current text map to find the block
    blocks, _, _ = engine.extract_text_map(pdf_path, page_number)
    target_block = None

    for block in blocks:
        if block.id == block_id:
            target_block = block
            break

    if not target_block:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Block not found: {block_id}",
        )

    # Apply edit
    engine.apply_block_edit(
        pdf_path,
        page_number,
        target_block.bbox,
        request.new_text,
    )

    # Invalidate rendered page image (delete if exists)
    render_path = storage.get_render_path(pdf_uuid, page_number)
    if render_path.exists():
        render_path.unlink()

    # Return updated text map
    updated_blocks, page_width, page_height = engine.extract_text_map(pdf_path, page_number)
    return TextMapResponse(
        pdf_uuid=pdf_uuid,
        page_number=page_number,
        page_width=page_width,
        page_height=page_height,
        blocks=updated_blocks,
    )


@router.put("/{pdf_uuid}/pages/{page_number}/words/{word_id}", response_model=TextMapResponse)
def edit_word(
    pdf_uuid: str,
    page_number: int,
    word_id: str,
    request: BlockEditRequest,
    storage: PDFStorageService = Depends(get_storage_service),
    engine: PDFEngine = Depends(get_pdf_engine),
    db: Session = Depends(get_db),
):
    """
    Edit a single word on a page.

    Args:
        pdf_uuid: PDF document UUID
        page_number: Page number (1-based)
        word_id: Word identifier (e.g., "page-1-block-3-word-5")
        request: Edit request with new text
        storage: Storage service
        engine: PDF engine
        db: Database session

    Returns:
        Updated text map for the page
    """
    # Verify PDF exists
    db_pdf = db.query(PDFDocument).filter(PDFDocument.uuid == pdf_uuid).first()
    if not db_pdf:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"PDF not found: {pdf_uuid}",
        )

    if page_number < 1 or page_number > db_pdf.page_count:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid page number: {page_number} (max: {db_pdf.page_count})",
        )

    pdf_path = storage.get_pdf_path(pdf_uuid)

    # Get current text map to find the word
    blocks, _, _ = engine.extract_text_map(pdf_path, page_number)
    target_word = None
    target_block = None

    for block in blocks:
        if block.words:
            for word in block.words:
                if word.id == word_id:
                    target_word = word
                    target_block = block
                    break
            if target_word:
                break

    if not target_word or not target_block:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Word not found: {word_id}",
        )

    # Apply word-level edit
    engine.apply_word_edit(
        pdf_path,
        page_number,
        target_word.bbox,
        request.new_text,
    )

    # Invalidate rendered page image (delete if exists)
    render_path = storage.get_render_path(pdf_uuid, page_number)
    if render_path.exists():
        render_path.unlink()

    # Return updated text map
    updated_blocks, page_width, page_height = engine.extract_text_map(pdf_path, page_number)
    return TextMapResponse(
        pdf_uuid=pdf_uuid,
        page_number=page_number,
        page_width=page_width,
        page_height=page_height,
        blocks=updated_blocks,
    )


@router.put("/{pdf_uuid}/pages/{page_number}/words/{word_id}", response_model=TextMapResponse)
def edit_word(
    pdf_uuid: str,
    page_number: int,
    word_id: str,
    request: BlockEditRequest,
    storage: PDFStorageService = Depends(get_storage_service),
    engine: PDFEngine = Depends(get_pdf_engine),
    db: Session = Depends(get_db),
):
    """
    Edit a single word on a page.

    Args:
        pdf_uuid: PDF document UUID
        page_number: Page number (1-based)
        word_id: Word identifier (e.g., "page-1-block-3-word-5")
        request: Edit request with new text
        storage: Storage service
        engine: PDF engine
        db: Database session

    Returns:
        Updated text map for the page
    """
    # Verify PDF exists
    db_pdf = db.query(PDFDocument).filter(PDFDocument.uuid == pdf_uuid).first()
    if not db_pdf:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"PDF not found: {pdf_uuid}",
        )

    if page_number < 1 or page_number > db_pdf.page_count:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid page number: {page_number} (max: {db_pdf.page_count})",
        )

    pdf_path = storage.get_pdf_path(pdf_uuid)

    # Get current text map to find the word
    blocks, _, _ = engine.extract_text_map(pdf_path, page_number)
    target_word = None
    target_block = None

    # First try to find by exact ID match
    for block in blocks:
        if block.words:
            for word in block.words:
                if word.id == word_id:
                    target_word = word
                    target_block = block
                    break
            if target_word:
                break
    
    # If not found by ID, try to find by parsing word_id (fallback)
    if not target_word:
        # Parse word_id format: "page-X-block-Y-word-Z"
        parts = word_id.split("-")
        if len(parts) >= 6 and parts[0] == "page" and parts[2] == "block" and parts[4] == "word":
            try:
                block_num = int(parts[3])
                word_num = int(parts[5])
                # Find block by number
                block_index = 0
                for block in blocks:
                    if block.page_number == page_number:
                        block_index += 1
                        if block_index == block_num:
                            if block.words and word_num <= len(block.words):
                                target_word = block.words[word_num - 1]  # 1-based to 0-based
                                target_block = block
                                break
            except (ValueError, IndexError):
                pass

    if not target_word or not target_block:
        # Provide helpful error message
        available_words = []
        for block in blocks[:3]:  # First 3 blocks only
            if block.words:
                available_words.extend([w.id for w in block.words[:3]])
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Word not found: {word_id}. Available words (sample): {available_words}",
        )

    # Apply word-level edit
    engine.apply_word_edit(
        pdf_path,
        page_number,
        target_word.bbox,
        request.new_text,
    )

    # Invalidate rendered page image (delete if exists)
    render_path = storage.get_render_path(pdf_uuid, page_number)
    if render_path.exists():
        render_path.unlink()

    # Return updated text map
    updated_blocks, page_width, page_height = engine.extract_text_map(pdf_path, page_number)
    return TextMapResponse(
        pdf_uuid=pdf_uuid,
        page_number=page_number,
        page_width=page_width,
        page_height=page_height,
        blocks=updated_blocks,
    )


@router.get("/{pdf_uuid}/download")
def download_pdf(
    pdf_uuid: str,
    storage: PDFStorageService = Depends(get_storage_service),
    db: Session = Depends(get_db),
):
    """
    Download the PDF file.

    Args:
        pdf_uuid: PDF document UUID
        storage: Storage service
        db: Database session

    Returns:
        PDF file stream
    """
    # Verify PDF exists
    db_pdf = db.query(PDFDocument).filter(PDFDocument.uuid == pdf_uuid).first()
    if not db_pdf:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"PDF not found: {pdf_uuid}",
        )

    pdf_path = storage.get_pdf_path(pdf_uuid)

    return FileResponse(
        str(pdf_path),
        media_type="application/pdf",
        filename=db_pdf.original_filename,
    )

