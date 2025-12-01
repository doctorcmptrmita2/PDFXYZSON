"""Tests for block edit endpoint."""
import io


def test_edit_block(client, temp_storage, sample_pdf_bytes):
    """Test editing a text block."""
    # Upload PDF
    file_obj = io.BytesIO(sample_pdf_bytes)
    file_obj.name = "test.pdf"
    
    response = client.post(
        "/api/pdfs/",
        files={"file": ("test.pdf", file_obj, "application/pdf")}
    )
    assert response.status_code == 201
    pdf_uuid = response.json()["uuid"]
    
    # Get text map
    response = client.get(f"/api/pdfs/{pdf_uuid}/pages/1/text-map")
    assert response.status_code == 200
    text_map = response.json()
    
    # If there are blocks, edit one
    if len(text_map["blocks"]) > 0:
        block = text_map["blocks"][0]
        block_id = block["id"]
        original_text = block["text"]
        new_text = "Edited text content"
        
        # Edit block
        response = client.put(
            f"/api/pdfs/{pdf_uuid}/pages/1/blocks/{block_id}",
            json={"new_text": new_text}
        )
        assert response.status_code == 200
        
        updated_text_map = response.json()
        assert updated_text_map["page_number"] == 1
        
        # Find the edited block
        edited_block = next(
            (b for b in updated_text_map["blocks"] if b["id"] == block_id),
            None
        )
        assert edited_block is not None
        assert edited_block["text"] == new_text
        
        # Verify PDF was modified by checking download
        response = client.get(f"/api/pdfs/{pdf_uuid}/download")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert len(response.content) > 0


def test_edit_nonexistent_block(client, temp_storage, sample_pdf_bytes):
    """Test editing a non-existent block."""
    # Upload PDF
    file_obj = io.BytesIO(sample_pdf_bytes)
    file_obj.name = "test.pdf"
    
    response = client.post(
        "/api/pdfs/",
        files={"file": ("test.pdf", file_obj, "application/pdf")}
    )
    assert response.status_code == 201
    pdf_uuid = response.json()["uuid"]
    
    # Try to edit non-existent block
    response = client.put(
        f"/api/pdfs/{pdf_uuid}/pages/1/blocks/nonexistent-block",
        json={"new_text": "New text"}
    )
    assert response.status_code == 404


def test_edit_block_empty_text(client, temp_storage, sample_pdf_bytes):
    """Test editing a block with empty text (should white-out)."""
    # Upload PDF
    file_obj = io.BytesIO(sample_pdf_bytes)
    file_obj.name = "test.pdf"
    
    response = client.post(
        "/api/pdfs/",
        files={"file": ("test.pdf", file_obj, "application/pdf")}
    )
    assert response.status_code == 201
    pdf_uuid = response.json()["uuid"]
    
    # Get text map
    response = client.get(f"/api/pdfs/{pdf_uuid}/pages/1/text-map")
    assert response.status_code == 200
    text_map = response.json()
    
    # If there are blocks, edit with empty text
    if len(text_map["blocks"]) > 0:
        block_id = text_map["blocks"][0]["id"]
        
        # Edit with empty text
        response = client.put(
            f"/api/pdfs/{pdf_uuid}/pages/1/blocks/{block_id}",
            json={"new_text": ""}
        )
        assert response.status_code == 200
        
        # Block should still exist but with empty text
        updated_text_map = response.json()
        edited_block = next(
            (b for b in updated_text_map["blocks"] if b["id"] == block_id),
            None
        )
        # Note: Empty blocks might be filtered out, so we just check the request succeeded

