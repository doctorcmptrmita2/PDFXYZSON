"""PDF operations endpoints for merge, split, rotate, etc."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_storage_service, get_pdf_engine
from app.models.pdf_document import PDFDocument
from app.services.storage import PDFStorageService
from app.services.pdf_engine import PDFEngine
import fitz  # PyMuPDF
from pathlib import Path
import uuid

router = APIRouter(prefix="/pdf-operations", tags=["PDF Operations"])


@router.post("/merge")
async def merge_pdfs(
    files: List[UploadFile] = File(...),
    storage: PDFStorageService = Depends(get_storage_service),
    db: Session = Depends(get_db),
):
    """
    Merge multiple PDFs into one.
    
    Args:
        files: List of PDF files to merge
        storage: Storage service
        db: Database session
        
    Returns:
        UUID of the merged PDF
    """
    if len(files) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least 2 PDF files required for merging"
        )
    
    # Create merged PDF
    merged_doc = fitz.open()
    pdf_uuid = str(uuid.uuid4())
    
    try:
        for file in files:
            if file.content_type != "application/pdf":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"File {file.filename} is not a PDF"
                )
            
            # Read file content
            content = await file.read()
            temp_path = storage.pdf_dir / f"temp_{uuid.uuid4()}.pdf"
            temp_path.write_bytes(content)
            
            # Open and append pages
            src_doc = fitz.open(temp_path)
            merged_doc.insert_pdf(src_doc)
            src_doc.close()
            temp_path.unlink()  # Cleanup
        
        # Save merged PDF
        merged_path = storage.pdf_dir / f"{pdf_uuid}.pdf"
        merged_doc.save(merged_path)
        merged_doc.close()
        
        # Create database record
        page_count = len(fitz.open(merged_path))
        db_pdf = PDFDocument(
            uuid=pdf_uuid,
            original_filename=f"merged_{pdf_uuid[:8]}.pdf",
            stored_path=str(merged_path),
            page_count=page_count,
        )
        db.add(db_pdf)
        db.commit()
        db.refresh(db_pdf)
        
        return {"uuid": pdf_uuid, "page_count": page_count}
    except Exception as e:
        if merged_doc:
            merged_doc.close()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to merge PDFs: {str(e)}"
        )


@router.post("/{pdf_uuid}/split")
async def split_pdf(
    pdf_uuid: str,
    page_ranges: List[str],  # e.g., ["1-5", "6-10", "11-"]
    storage: PDFStorageService = Depends(get_storage_service),
    db: Session = Depends(get_db),
):
    """
    Split a PDF into multiple files based on page ranges.
    
    Args:
        pdf_uuid: Source PDF UUID
        page_ranges: List of page ranges (1-based, inclusive)
        storage: Storage service
        db: Database session
        
    Returns:
        List of UUIDs for split PDFs
    """
    pdf_path = storage.get_pdf_path(pdf_uuid)
    db_pdf = db.query(PDFDocument).filter(PDFDocument.uuid == pdf_uuid).first()
    
    if not db_pdf:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"PDF not found: {pdf_uuid}"
        )
    
    source_doc = fitz.open(pdf_path)
    split_uuids = []
    
    try:
        for range_str in page_ranges:
            # Parse range (e.g., "1-5" or "6-10" or "11-")
            parts = range_str.split("-")
            start = int(parts[0]) - 1  # Convert to 0-based
            end = int(parts[1]) - 1 if len(parts) > 1 and parts[1] else len(source_doc) - 1
            
            if start < 0 or end >= len(source_doc) or start > end:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid page range: {range_str}"
                )
            
            # Create new PDF with selected pages
            new_doc = fitz.open()
            new_doc.insert_pdf(source_doc, from_page=start, to_page=end)
            
            # Save split PDF
            split_uuid = str(uuid.uuid4())
            split_path = storage.pdf_dir / f"{split_uuid}.pdf"
            new_doc.save(split_path)
            new_doc.close()
            
            # Create database record
            page_count = end - start + 1
            db_split = PDFDocument(
                uuid=split_uuid,
                original_filename=f"{db_pdf.original_filename}_split_{start+1}-{end+1}.pdf",
                stored_path=str(split_path),
                page_count=page_count,
            )
            db.add(db_split)
            split_uuids.append(split_uuid)
        
        db.commit()
        return {"split_uuids": split_uuids}
    finally:
        source_doc.close()


@router.post("/{pdf_uuid}/rotate")
async def rotate_pages(
    pdf_uuid: str,
    page_numbers: List[int],  # 1-based page numbers
    angle: int,  # 90, 180, or 270
    storage: PDFStorageService = Depends(get_storage_service),
    db: Session = Depends(get_db),
):
    """
    Rotate specific pages in a PDF.
    
    Args:
        pdf_uuid: PDF UUID
        page_numbers: List of page numbers to rotate (1-based)
        angle: Rotation angle (90, 180, or 270)
        storage: Storage service
        db: Database session
        
    Returns:
        Success message
    """
    if angle not in [90, 180, 270]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Angle must be 90, 180, or 270"
        )
    
    pdf_path = storage.get_pdf_path(pdf_uuid)
    db_pdf = db.query(PDFDocument).filter(PDFDocument.uuid == pdf_uuid).first()
    
    if not db_pdf:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"PDF not found: {pdf_uuid}"
        )
    
    doc = fitz.open(pdf_path)
    
    try:
        for page_num in page_numbers:
            if page_num < 1 or page_num > len(doc):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid page number: {page_num}"
                )
            page = doc[page_num - 1]  # Convert to 0-based
            page.set_rotation(angle)
        
        doc.save(pdf_path, incremental=False)
        
        # Invalidate rendered images
        for page_num in page_numbers:
            render_path = storage.get_render_path(pdf_uuid, page_num)
            if render_path.exists():
                render_path.unlink()
        
        return {"message": f"Rotated {len(page_numbers)} page(s) by {angle} degrees"}
    finally:
        doc.close()


@router.delete("/{pdf_uuid}/pages")
async def delete_pages(
    pdf_uuid: str,
    page_numbers: List[int],  # 1-based page numbers
    storage: PDFStorageService = Depends(get_storage_service),
    db: Session = Depends(get_db),
):
    """
    Delete specific pages from a PDF.
    
    Args:
        pdf_uuid: PDF UUID
        page_numbers: List of page numbers to delete (1-based)
        storage: Storage service
        db: Database session
        
    Returns:
        Success message
    """
    pdf_path = storage.get_pdf_path(pdf_uuid)
    db_pdf = db.query(PDFDocument).filter(PDFDocument.uuid == pdf_uuid).first()
    
    if not db_pdf:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"PDF not found: {pdf_uuid}"
        )
    
    doc = fitz.open(pdf_path)
    
    try:
        # Convert to 0-based and sort descending to delete from end
        pages_to_delete = sorted([p - 1 for p in page_numbers], reverse=True)
        
        for page_idx in pages_to_delete:
            if page_idx < 0 or page_idx >= len(doc):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid page number: {page_idx + 1}"
                )
            doc.delete_page(page_idx)
        
        doc.save(pdf_path, incremental=False)
        
        # Update page count
        db_pdf.page_count = len(doc)
        db.commit()
        
        # Invalidate all rendered images
        for i in range(1, db_pdf.page_count + 1):
            render_path = storage.get_render_path(pdf_uuid, i)
            if render_path.exists():
                render_path.unlink()
        
        return {"message": f"Deleted {len(page_numbers)} page(s)", "new_page_count": len(doc)}
    finally:
        doc.close()

