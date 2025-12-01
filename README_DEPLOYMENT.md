# AeroPdf Editör - Deployment Rehberi

## 🚀 EasyPanel Deployment

Detaylı deployment rehberi için: [EASYPANEL_UPLOAD.md](./EASYPANEL_UPLOAD.md)

## 📋 Hızlı Başlangıç

### 1. Environment Variables

#### Backend
```env
DATABASE_URL=sqlite:///./aeropdf.db
STORAGE_BASE_DIR=/app/storage
STORAGE_PDF_DIR=/app/storage/pdfs
STORAGE_RENDER_DIR=/app/storage/renders
DEBUG=false
CORS_ORIGINS=https://aeropdf.com,https://www.aeropdf.com
FRONTEND_DOMAIN=aeropdf.com
```

#### Frontend (Build-time)
```env
VITE_API_BASE_URL=https://api.aeropdf.com/api
```

### 2. Docker Compose

Production için:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 3. Domain Yapılandırması

- **Frontend**: `aeropdf.com` → Port 80
- **Backend API**: `api.aeropdf.com` → Port 8001

## 🔍 SEO Ayarları

✅ Meta tags eklendi
✅ Open Graph tags eklendi
✅ Twitter Card tags eklendi
✅ Structured Data (JSON-LD) eklendi
✅ robots.txt eklendi
✅ sitemap.xml eklendi

## 📝 Checklist

- [x] SEO meta tags
- [x] Open Graph tags
- [x] Structured Data
- [x] robots.txt
- [x] sitemap.xml
- [x] Production Dockerfile'lar
- [x] Nginx configuration
- [x] CORS yapılandırması
- [x] Environment variables
- [x] EasyPanel deployment guide

## 🔗 İlgili Dosyalar

- `EASYPANEL_UPLOAD.md` - Detaylı EasyPanel rehberi
- `docker-compose.prod.yml` - Production compose file
- `frontend/nginx.conf` - Nginx configuration
- `frontend/index.html` - SEO meta tags

