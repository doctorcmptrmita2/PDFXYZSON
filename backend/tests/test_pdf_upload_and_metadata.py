"""Tests for PDF upload and metadata endpoints."""
import io
from fastapi import UploadFile


def test_upload_pdf(client, temp_storage, sample_pdf_bytes):
    """Test uploading a PDF and retrieving metadata."""
    # Create a file-like object
    file_obj = io.BytesIO(sample_pdf_bytes)
    file_obj.name = "test.pdf"
    
    # Upload PDF
    response = client.post(
        "/api/pdfs/",
        files={"file": ("test.pdf", file_obj, "application/pdf")}
    )
    
    assert response.status_code == 201
    data = response.json()
    
    assert "uuid" in data
    assert "original_filename" in data
    assert data["original_filename"] == "test.pdf"
    assert "page_count" in data
    assert data["page_count"] == 1
    assert "id" in data
    assert "created_at" in data
    
    pdf_uuid = data["uuid"]
    
    # Get metadata
    response = client.get(f"/api/pdfs/{pdf_uuid}")
    assert response.status_code == 200
    metadata = response.json()
    
    assert metadata["uuid"] == pdf_uuid
    assert metadata["original_filename"] == "test.pdf"
    assert metadata["page_count"] == 1


def test_upload_invalid_file(client):
    """Test uploading a non-PDF file."""
    file_obj = io.BytesIO(b"not a pdf")
    file_obj.name = "test.txt"
    
    response = client.post(
        "/api/pdfs/",
        files={"file": ("test.txt", file_obj, "text/plain")}
    )
    
    assert response.status_code == 400
    assert "PDF" in response.json()["detail"]


def test_get_nonexistent_pdf(client):
    """Test getting metadata for a non-existent PDF."""
    response = client.get("/api/pdfs/nonexistent-uuid")
    assert response.status_code == 404

