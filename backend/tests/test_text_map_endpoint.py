"""Tests for text map extraction endpoint."""
import io


def test_get_text_map(client, temp_storage, sample_pdf_bytes):
    """Test extracting text map from a PDF page."""
    # Upload PDF
    file_obj = io.BytesIO(sample_pdf_bytes)
    file_obj.name = "test.pdf"
    
    response = client.post(
        "/api/pdfs/",
        files={"file": ("test.pdf", file_obj, "application/pdf")}
    )
    assert response.status_code == 201
    pdf_uuid = response.json()["uuid"]
    
    # Get text map for page 1
    response = client.get(f"/api/pdfs/{pdf_uuid}/pages/1/text-map")
    assert response.status_code == 200
    
    data = response.json()
    assert "pdf_uuid" in data
    assert data["pdf_uuid"] == pdf_uuid
    assert "page_number" in data
    assert data["page_number"] == 1
    assert "page_width" in data
    assert "page_height" in data
    assert isinstance(data["page_width"], (int, float))
    assert isinstance(data["page_height"], (int, float))
    assert "blocks" in data
    assert isinstance(data["blocks"], list)
    
    # Check block structure if blocks exist
    if len(data["blocks"]) > 0:
        block = data["blocks"][0]
        assert "id" in block
        assert "page_number" in block
        assert "bbox" in block
        assert "text" in block
        
        bbox = block["bbox"]
        assert "x0" in bbox
        assert "y0" in bbox
        assert "x1" in bbox
        assert "y1" in bbox


def test_get_text_map_invalid_page(client, temp_storage, sample_pdf_bytes):
    """Test getting text map for invalid page number."""
    # Upload PDF
    file_obj = io.BytesIO(sample_pdf_bytes)
    file_obj.name = "test.pdf"
    
    response = client.post(
        "/api/pdfs/",
        files={"file": ("test.pdf", file_obj, "application/pdf")}
    )
    assert response.status_code == 201
    pdf_uuid = response.json()["uuid"]
    
    # Try invalid page number
    response = client.get(f"/api/pdfs/{pdf_uuid}/pages/999/text-map")
    assert response.status_code == 400

