# AeroPdf - Feature List

## ✅ Implemented Features

### Core Editing
- ✅ **Word-Level Editing**: Edit individual words with inline editing
- ✅ **Block-Level Editing**: Edit entire text blocks
- ✅ **Real-time Preview**: See changes instantly
- ✅ **Auto-save**: Debounced auto-save (500ms)
- ✅ **Optimistic Updates**: UI updates immediately

### PDF Operations (Backend Ready)
- ✅ **Merge PDFs**: Combine multiple PDFs into one
- ✅ **Split PDF**: Divide PDFs into multiple files by page ranges
- ✅ **Rotate Pages**: Rotate pages in 90, 180, or 270 degrees
- ✅ **Delete Pages**: Remove specific pages from PDF

### UI/UX
- ✅ **Professional Landing Page**: Feature showcase
- ✅ **Modern UI**: Tailwind CSS with gradient design
- ✅ **Responsive Design**: Works on all screen sizes
- ✅ **Visual Overlays**: Word and block selection with hover effects
- ✅ **Loading States**: Proper feedback during operations

## 🚧 Planned Features

### Organize Operations
- [ ] Extract specific pages
- [ ] Crop PDF pages
- [ ] Adjust page size/scale
- [ ] Multi-page layout
- [ ] Rearrange pages (drag & drop)

### Convert to PDF
- [ ] Image to PDF
- [ ] Word/Excel/PowerPoint to PDF
- [ ] HTML to PDF
- [ ] Markdown to PDF
- [ ] Email to PDF
- [ ] eBook to PDF (EPUB, MOBI)

### Convert from PDF
- [ ] PDF to Word
- [ ] PDF to Image
- [ ] PDF to HTML
- [ ] PDF to Markdown
- [ ] PDF to CSV
- [ ] PDF to XML

### Sign & Security
- [ ] Add digital signatures
- [ ] Add/Remove password
- [ ] Add watermarks
- [ ] Redact content
- [ ] Change permissions
- [ ] Sanitize PDF

### View & Edit
- [ ] OCR / Cleanup scans
- [ ] Add/Extract images
- [ ] Change metadata
- [ ] Add page numbers
- [ ] Remove blank pages
- [ ] Flatten PDF

### Advanced
- [ ] Compress PDF
- [ ] Repair corrupted PDFs
- [ ] Compare PDFs
- [ ] Overlay PDFs
- [ ] Auto-split by size/count
- [ ] Pipeline processing

## 📝 API Endpoints

### PDF Management
- `POST /api/pdfs/` - Upload PDF
- `GET /api/pdfs/{uuid}` - Get PDF metadata
- `GET /api/pdfs/{uuid}/pages/{page}/image` - Get page image
- `GET /api/pdfs/{uuid}/pages/{page}/text-map` - Get text map
- `PUT /api/pdfs/{uuid}/pages/{page}/blocks/{block_id}` - Edit block
- `PUT /api/pdfs/{uuid}/pages/{page}/words/{word_id}` - Edit word
- `GET /api/pdfs/{uuid}/download` - Download PDF

### PDF Operations
- `POST /api/pdf-operations/merge` - Merge PDFs
- `POST /api/pdf-operations/{uuid}/split` - Split PDF
- `POST /api/pdf-operations/{uuid}/rotate` - Rotate pages
- `DELETE /api/pdf-operations/{uuid}/pages` - Delete pages

## 🚀 Getting Started

1. **Backend**: 
   ```bash
   cd backend
   .\.venv\Scripts\Activate.ps1
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
   ```

2. **Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access**:
   - Landing Page: http://localhost:3001
   - Upload: http://localhost:3001/app
   - API Docs: http://localhost:8001/docs

## 📦 Technology Stack

- **Backend**: Python 3.11+, FastAPI, PyMuPDF, SQLAlchemy
- **Frontend**: React 18+, TypeScript, Vite, Tailwind CSS
- **State Management**: React Query
- **Icons**: Lucide React

