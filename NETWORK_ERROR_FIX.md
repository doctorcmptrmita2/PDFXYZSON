# NetworkError Çözüm Rehberi

## Sorun: "NetworkError when attempting to fetch resource"

Bu hata, frontend'in backend'e bağlanamadığı anlamına gelir.

## Hızlı Çözüm

### 1. Backend'in Çalıştığını Kontrol Edin

**Terminal/PowerShell'de:**

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

**Beklenen çıktı:**
```
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
AeroPdf API started successfully
INFO:     Application startup complete.
```

### 2. Backend'i Tarayıcıda Test Edin

Aşağıdaki URL'leri açın:

- **Health check**: http://localhost:8001/health
  - Beklenen: `{"status":"healthy"}`
  
- **API Docs**: http://localhost:8001/docs
  - Swagger UI açılmalı

- **Root endpoint**: http://localhost:8001/
  - API mesajı görünmeli

### 3. Frontend'i Başlatın

**Yeni bir terminal/PowerShell penceresinde:**

```bash
cd frontend
npm run dev
```

### 4. Port Kontrolü

- **Backend**: Port **8001**'de çalışmalı
- **Frontend**: Port **3001**'de çalışmalı (veya Vite'ın gösterdiği port)

## Yaygın Sorunlar ve Çözümleri

### Sorun 1: "Connection refused" veya "Failed to fetch"

**Neden**: Backend çalışmıyor

**Çözüm**:
1. Backend terminalinde hata var mı kontrol edin
2. Port 8001 başka bir uygulama tarafından kullanılıyor olabilir
3. `netstat -ano | findstr :8001` (Windows) ile kontrol edin
4. Backend'i yeniden başlatın

### Sorun 2: CORS Hatası

**Neden**: Backend CORS ayarları frontend portunu içermiyor

**Kontrol**: `backend/app/main.py` dosyasında şu satırlar olmalı:
```python
allow_origins=[
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    ...
]
```

### Sorun 3: Port Çakışması

**Neden**: Port 8001 zaten kullanılıyor

**Çözüm**:
1. Port'u kullanan uygulamayı bulun:
   ```bash
   # Windows
   netstat -ano | findstr :8001
   
   # Linux/Mac
   lsof -i :8001
   ```
2. Uygulamayı kapatın veya backend'i farklı bir portta çalıştırın

### Sorun 4: Firewall/Antivirus

**Neden**: Windows Firewall veya antivirüs engelliyor

**Çözüm**:
1. Windows Defender Firewall ayarlarını kontrol edin
2. Python ve Node.js için istisna ekleyin
3. Antivirüs yazılımını geçici olarak devre dışı bırakın (test için)

## Adım Adım Kontrol Listesi

- [ ] Backend terminalinde "Uvicorn running" mesajı var mı?
- [ ] http://localhost:8001/health çalışıyor mu?
- [ ] http://localhost:8001/docs açılıyor mu?
- [ ] Frontend terminalinde "VITE ready" mesajı var mı?
- [ ] Frontend hangi portta çalışıyor? (Terminal çıktısını kontrol edin)
- [ ] Backend CORS ayarlarında frontend portu var mı?
- [ ] Her iki terminal de açık ve çalışıyor mu?

## Test Komutları

### Backend Test
```bash
# Health check
curl http://localhost:8001/health

# Veya tarayıcıda açın
start http://localhost:8001/health  # Windows
```

### Frontend Test
```bash
# Frontend çalışıyor mu kontrol edin
curl http://localhost:3001
```

## Hala Çalışmıyorsa

1. **Her iki servisi de durdurun** (Ctrl+C)
2. **Yeniden başlatın**:
   - Önce backend
   - Sonra frontend
3. **Tarayıcı konsolunu kontrol edin** (F12 > Console)
4. **Network sekmesini kontrol edin** (F12 > Network)
   - Hangi istek başarısız oluyor?
   - Hata mesajı ne?

## Docker Kullanıyorsanız

```bash
docker-compose up --build
```

Logları kontrol edin:
```bash
docker-compose logs backend
docker-compose logs frontend
```

