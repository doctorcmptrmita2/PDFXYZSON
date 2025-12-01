# AeroPdf

A small, open-source demo of **block-based, Word-like PDF text editing** using a visual overlay approach.

## 🎯 Project Overview

AeroPdf allows users to upload PDF documents and edit text blocks in a Word-like experience. Unlike full PDF typesetting engines, this tool uses a **visual overlay approach**:

- Extracts text blocks with bounding boxes from each page
- Allows users to click on blocks and edit their content
- Overlays new text over the original block region (white-out + redraw)
- Provides a simple, intuitive editing experience

**Note**: This is a demonstration project focused on block-level editing. It does not implement full layout engines or multi-page text reflow.

## ✨ Features

- **Upload PDF**: Upload PDF files via web interface
- **View Pages**: Navigate through PDF pages with rendered images
- **Text Block Detection**: Automatically detects and highlights clickable text blocks
- **Block Editing**: Edit text blocks with a Word-like textarea interface
- **Visual Updates**: See changes immediately with overlay-based text rendering
- **Download**: Download the modified PDF file

### Limitations

- **Block-level only**: Edits are applied at the block level, not word or character level
- **No multi-page reflow**: Text blocks never spill over to other pages
- **Simple documents**: Best suited for simple documents, not complex magazine layouts
- **No OCR**: Scanned PDFs without text layers are not supported
- **Font matching**: Uses default fonts, may not perfectly match original font metrics

## 🛠️ Tech Stack

### Backend
- **Python 3.11+**
- **FastAPI**: Modern, fast web framework
- **PyMuPDF (fitz)**: PDF processing and text extraction
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Lightweight database for metadata
- **Pydantic v2**: Data validation

### Frontend
- **React 18+**: UI library
- **TypeScript**: Type safety
- **Vite**: Build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **React Router v6**: Client-side routing

### Infrastructure
- **Docker & Docker Compose**: Containerization (optional)

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+
- npm or yarn
- (Optional) Docker and Docker Compose

### Local Development

#### Backend Setup

**⚡ Hızlı Başlatma (Windows):**
1. `backend` klasörüne gidin
2. `BASLAT.bat` dosyasına çift tıklayın
3. Backend otomatik olarak başlayacak!

**Manuel Başlatma:**

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment (first time only):
```bash
python -m venv .venv
```

3. Activate virtual environment:
```bash
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# Windows CMD:
.venv\Scripts\activate.bat

# Linux/Mac:
source .venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Initialize database (first time only):
```bash
python -m app.db.init_db
```

6. Start development server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

**✅ Backend will be available at `http://localhost:8001`**
**📚 API documentation: `http://localhost:8001/docs`**

**⚠️ Important:** Keep the backend terminal window open! Do not close it.

#### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

**Not**: İlk kurulum biraz zaman alabilir (1-2 dakika).

3. Start development server:
```bash
npm run dev
```

4. Terminal çıktısını kontrol edin. Şuna benzer bir mesaj görmelisiniz:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3001/
```

Frontend will be available at `http://localhost:3001`

**Sorun Giderme:**
- Eğer port 3001 kullanılıyorsa, Vite otomatik olarak bir sonraki boş portu kullanacaktır (örn: 3002, 3003). Terminal çıktısındaki gerçek portu kontrol edin.
- "npm: command not found" hatası alıyorsanız, [Node.js](https://nodejs.org/) yüklü değildir. Node.js v20+ yükleyin.
- Bağımlılık hataları için: `rm -rf node_modules package-lock.json && npm install` (Linux/Mac) veya `rmdir /s node_modules && del package-lock.json && npm install` (Windows)

### Docker Usage

1. Build and start all services:
```bash
docker-compose up --build
```

2. Access the application:
- Frontend: `http://localhost:3001`
- Backend API: `http://localhost:8001`
- API Docs: `http://localhost:8001/docs`

3. Stop services:
```bash
docker-compose down
```

**Note**: PDF files and database are persisted in `backend/storage/` and `backend/aeropdf.db` respectively.

## 📖 Usage Flow

1. **Upload PDF**
   - Go to the home page
   - Click "Select PDF File" and choose a PDF
   - Click "Upload PDF"
   - You'll be redirected to the editor

2. **Navigate Pages**
   - Use "Previous" and "Next" buttons in the toolbar
   - Or use the page indicator to see current page

3. **Edit Text Blocks**
   - Click on any highlighted text block on the page
   - The block will be highlighted in blue
   - Edit the text in the right panel textarea
   - Click "Save Changes" to apply

4. **Download PDF**
   - Click "Download PDF" in the toolbar
   - The modified PDF will be downloaded to your computer

## 🧪 Testing

### Backend Tests

Run tests from the backend directory:

```bash
cd backend
pytest
```

Test coverage includes:
- PDF upload and metadata retrieval
- Text map extraction
- Block editing functionality
- Error handling

## 📁 Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/              # API routes
│   │   ├── core/             # Configuration
│   │   ├── db/               # Database setup
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   └── main.py           # FastAPI app
│   ├── tests/                # Test suite
│   ├── storage/              # PDF storage (created at runtime)
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/              # API client
│   │   ├── components/       # React components
│   │   ├── hooks/            # Custom hooks
│   │   ├── pages/            # Page components
│   │   ├── types/           # TypeScript types
│   │   └── styles/          # CSS
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
└── README.md
```

## 🔧 Configuration

### Backend

Configuration is managed via environment variables (see `backend/app/core/config.py`):

- `DATABASE_URL`: Database connection string (default: `sqlite:///./aeropdf.db`)
- `STORAGE_DIR`: Base storage directory (default: `storage`)
- `PDF_DIR`: PDF files directory (default: `storage/pdfs`)
- `RENDER_DIR`: Rendered images directory (default: `storage/renders`)
- `DEBUG`: Debug mode (default: `True`)

### Frontend

API base URL is configured in `frontend/src/api/client.ts`:
- Default: `http://localhost:8001/api`

## 🚧 Future Work

Potential improvements and features:

- **Better Font Detection**: Detect and match original fonts more accurately
- **Robust Block Detection**: Improved algorithms for text block identification
- **Authentication**: User accounts and session management
- **Edit History**: Undo/redo functionality
- **Multi-block Selection**: Select and edit multiple blocks at once
- **Export Formats**: Support for exporting to other formats
- **OCR Integration**: Support for scanned PDFs
- **Performance Optimization**: Caching and optimization for large documents

## 📝 License

This project is open-source and available for educational and demonstration purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📧 Support

For questions or issues, please open an issue on the project repository.

---

**Note**: This is a demonstration project. For production use, consider additional features like authentication, rate limiting, and more robust error handling.

