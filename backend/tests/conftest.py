"""Pytest configuration and fixtures."""
import pytest
import tempfile
import shutil
from pathlib import Path
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.models.base import Base
from app.core.config import settings


@pytest.fixture(scope="function")
def test_db():
    """Create a temporary database for testing."""
    # Use in-memory SQLite for tests
    test_db_url = "sqlite:///:memory:"
    engine = create_engine(test_db_url, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    yield TestingSessionLocal()
    
    # Cleanup
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    """Create a test client with overridden database dependency."""
    from app.db.session import get_db
    
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def temp_storage(monkeypatch):
    """Create a temporary storage directory."""
    from app.core.config import settings
    
    temp_dir = tempfile.mkdtemp()
    pdf_dir = str(Path(temp_dir) / "pdfs")
    render_dir = str(Path(temp_dir) / "renders")
    
    Path(pdf_dir).mkdir(parents=True, exist_ok=True)
    Path(render_dir).mkdir(parents=True, exist_ok=True)
    
    # Patch settings
    monkeypatch.setattr(settings, "STORAGE_DIR", temp_dir)
    monkeypatch.setattr(settings, "PDF_DIR", pdf_dir)
    monkeypatch.setattr(settings, "RENDER_DIR", render_dir)
    
    yield temp_dir
    
    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def sample_pdf_bytes():
    """Generate a minimal PDF file in bytes."""
    # This is a minimal valid PDF (1 page, empty)
    # In real tests, you might want to use a more substantial PDF
    return b"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj
2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj
3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
/Resources <<
/Font <<
/F1 <<
/Type /Font
/Subtype /Type1
/BaseFont /Helvetica
>>
>>
>>
>>
endobj
4 0 obj
<<
/Length 44
>>
stream
BT
/F1 12 Tf
100 700 Td
(Hello World) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000317 00000 n 
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
398
%%EOF"""

