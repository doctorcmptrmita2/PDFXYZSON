# AeroPdf - Backend

Backend API for AeroPdf, a block-based PDF editing engine.

## Technology Stack

- Python 3.11+
- FastAPI
- PyMuPDF (pymupdf)
- SQLAlchemy (SQLite)
- Pydantic v2

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Initialize database:

```bash
python -m app.db.init_db
```

3. Run the development server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

The API will be available at `http://localhost:8001`

API documentation: `http://localhost:8001/docs`

## Testing

Run tests with pytest:

```bash
pytest
```

For verbose output:

```bash
pytest -v
```

## Docker

Build and run with Docker:

```bash
docker build -t aeropdf-backend .
docker run -p 8001:8001 -v $(pwd)/storage:/app/storage aeropdf-backend
```

Or use docker-compose from the root directory.

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── core/
│   │   └── config.py        # Application settings
│   ├── models/              # SQLAlchemy models
│   │   ├── base.py
│   │   ├── pdf_document.py
│   │   └── pdf_overlay.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── pdf_document.py
│   │   ├── pdf_page.py
│   │   └── pdf_text_map.py
│   ├── api/                 # API routes
│   │   ├── deps.py          # Dependencies
│   │   └── routes/
│   │       └── pdfs.py      # PDF endpoints
│   ├── services/            # Business logic
│   │   ├── storage.py       # File storage
│   │   └── pdf_engine.py    # PyMuPDF operations
│   └── db/                  # Database
│       ├── session.py
│       └── init_db.py
├── tests/                    # Test suite
├── storage/                  # PDF storage (created at runtime)
├── requirements.txt
├── pytest.ini
└── README.md
```

## API Endpoints

- `POST /api/pdfs/` - Upload PDF
- `GET /api/pdfs/{pdf_uuid}` - Get PDF metadata
- `GET /api/pdfs/{pdf_uuid}/pages/{page_number}/image` - Get page image (PNG)
- `GET /api/pdfs/{pdf_uuid}/pages/{page_number}/text-map` - Get page text map
- `PUT /api/pdfs/{pdf_uuid}/pages/{page_number}/blocks/{block_id}` - Edit text block
- `GET /api/pdfs/{pdf_uuid}/download` - Download PDF

## Storage

PDFs are stored in `storage/pdfs/` and rendered page images in `storage/renders/`.

Database file: `aeropdf.db` (SQLite)

## Environment Variables

- `DATABASE_URL`: Database connection string (default: `sqlite:///./aeropdf.db`)
- `STORAGE_DIR`: Base storage directory (default: `storage`)
- `PDF_DIR`: PDF files directory (default: `storage/pdfs`)
- `RENDER_DIR`: Rendered images directory (default: `storage/renders`)
- `DEBUG`: Debug mode (default: `True`)
