# AeroPdf Editör - EasyPanel Deployment Rehberi

Bu rehber, AeroPdf Editör projesini EasyPanel'e yüklemek için adım adım talimatlar içerir.

## 📋 Ön Gereksinimler

- EasyPanel kurulumu
- Docker desteği
- En az 2GB RAM
- 10GB disk alanı

## 🚀 Deployment Adımları

### 1. Projeyi EasyPanel'e Yükleme

#### Yöntem 1: Git Repository (Önerilen)

1. EasyPanel'de yeni bir **App** oluşturun
2. **Source** sekmesinde:
   - **Type**: Git Repository
   - **Repository URL**: `https://github.com/yourusername/aeropdf-editor.git` (veya kendi repo URL'niz)
   - **Branch**: `main` veya `master`
   - **Build Command**: `docker-compose build`
   - **Start Command**: `docker-compose up -d`

#### Yöntem 2: Docker Compose File

1. EasyPanel'de yeni bir **App** oluşturun
2. **Source** sekmesinde:
   - **Type**: Docker Compose
   - **Compose File**: Aşağıdaki `docker-compose.yml` içeriğini yapıştırın

### 2. Docker Compose Yapılandırması

EasyPanel'de kullanılacak `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: aeropdf-backend
    restart: unless-stopped
    ports:
      - "8001:8001"
    environment:
      - DATABASE_URL=sqlite:///./aeropdf.db
      - STORAGE_BASE_DIR=/app/storage
      - STORAGE_PDF_DIR=/app/storage/pdfs
      - STORAGE_RENDER_DIR=/app/storage/renders
      - DEBUG=false
    volumes:
      - backend_storage:/app/storage
      - backend_db:/app
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - aeropdf-network

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: aeropdf-frontend
    restart: unless-stopped
    ports:
      - "3001:3001"
    environment:
      - VITE_API_BASE_URL=http://localhost:8001/api
    depends_on:
      backend:
        condition: service_healthy
    networks:
      - aeropdf-network

volumes:
  backend_storage:
    driver: local
  backend_db:
    driver: local

networks:
  aeropdf-network:
    driver: bridge
```

### 3. Environment Variables (EasyPanel'de Ayarlayın)

#### Backend Environment Variables:

```env
DATABASE_URL=sqlite:///./aeropdf.db
STORAGE_BASE_DIR=/app/storage
STORAGE_PDF_DIR=/app/storage/pdfs
STORAGE_RENDER_DIR=/app/storage/renders
DEBUG=false
```

#### Frontend Environment Variables:

```env
VITE_API_BASE_URL=http://your-backend-domain:8001/api
```

**ÖNEMLİ**: Production'da frontend'in backend'e erişebilmesi için:
- Backend URL'ini frontend environment variable'ında ayarlayın
- CORS ayarlarını backend'de güncelleyin

### 4. Port Yapılandırması

EasyPanel'de port mapping:

- **Backend**: `8001:8001`
- **Frontend**: `3001:3001`

Veya EasyPanel'in otomatik port atama özelliğini kullanabilirsiniz.

### 5. Volume Yapılandırması

EasyPanel'de volume mapping:

- **Backend Storage**: `/app/storage` → Persistent storage
- **Backend Database**: `/app` → Database dosyası için

### 6. Domain ve Reverse Proxy Ayarları

EasyPanel'de reverse proxy kurulumu:

1. **Backend için**:
   - Domain: `api.aeropdf.com` (veya `backend.aeropdf.com`)
   - Target: `http://backend:8001`
   - Path: `/`

2. **Frontend için**:
   - Domain: `aeropdf.com` (veya `www.aeropdf.com`)
   - Target: `http://frontend:3001`
   - Path: `/`

### 7. CORS Ayarlarını Güncelleme

Production'da backend'in CORS ayarlarını güncelleyin:

`backend/app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://aeropdf.com",
        "https://www.aeropdf.com",
        "http://localhost:3001",  # Development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 8. Frontend API URL Güncelleme

Production build için frontend'de API URL'ini güncelleyin:

`frontend/src/api/client.ts`:

```typescript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://api.aeropdf.com/api';
```

### 9. Build ve Deploy

EasyPanel'de:

1. **Build** butonuna tıklayın
2. Build tamamlandıktan sonra **Start** butonuna tıklayın
3. Logları kontrol edin

### 10. Health Check

Deployment sonrası kontrol:

```bash
# Backend health check
curl https://api.aeropdf.com/health

# Frontend kontrol
curl https://aeropdf.com/
```

## 🔧 Production Optimizasyonları

### 1. Backend Optimizasyonu

`backend/Dockerfile` production için optimize edilmiş:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run as non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "4"]
```

### 2. Frontend Production Build

`frontend/Dockerfile` production için:

```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### 3. Nginx Configuration (Frontend için)

`frontend/nginx.conf`:

```nginx
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## 📝 Environment Variables Checklist

### Backend (.env veya EasyPanel Environment)

- [ ] `DATABASE_URL` - SQLite database path
- [ ] `STORAGE_BASE_DIR` - Storage base directory
- [ ] `STORAGE_PDF_DIR` - PDF files directory
- [ ] `STORAGE_RENDER_DIR` - Rendered images directory
- [ ] `DEBUG` - Debug mode (false for production)

### Frontend (Build-time)

- [ ] `VITE_API_BASE_URL` - Backend API URL

## 🔒 Güvenlik Kontrolleri

- [ ] CORS ayarları production domain'lerine göre güncellendi
- [ ] DEBUG mode kapalı
- [ ] Environment variables güvenli şekilde saklanıyor
- [ ] HTTPS aktif
- [ ] Security headers eklendi (Nginx)

## 📊 Monitoring

EasyPanel'de monitoring ayarları:

1. **Health Checks**: Backend için `/health` endpoint
2. **Logs**: EasyPanel log viewer'da kontrol edin
3. **Resources**: CPU ve Memory kullanımını izleyin

## 🐛 Troubleshooting

### Backend başlamıyor

1. Logları kontrol edin: `docker logs aeropdf-backend`
2. Port çakışması var mı kontrol edin
3. Database permissions kontrol edin

### Frontend backend'e bağlanamıyor

1. CORS ayarlarını kontrol edin
2. API URL'ini kontrol edin
3. Network connectivity kontrol edin

### Storage sorunları

1. Volume permissions kontrol edin
2. Disk space kontrol edin
3. Storage path'lerini kontrol edin

## 📞 Destek

Sorun yaşarsanız:
1. EasyPanel loglarını kontrol edin
2. Docker container loglarını kontrol edin
3. Health check endpoint'lerini test edin

## ✅ Deployment Checklist

- [ ] Git repository hazır
- [ ] Docker Compose yapılandırması hazır
- [ ] Environment variables ayarlandı
- [ ] CORS ayarları güncellendi
- [ ] Domain ve reverse proxy ayarlandı
- [ ] SSL sertifikası aktif
- [ ] Health checks çalışıyor
- [ ] Storage volumes mount edildi
- [ ] Production build yapıldı
- [ ] Test edildi

---

**Not**: Bu rehber EasyPanel'in güncel versiyonu için hazırlanmıştır. EasyPanel versiyonunuza göre bazı adımlar farklılık gösterebilir.

