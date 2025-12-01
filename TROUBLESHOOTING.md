# AeroPdf Editör - Troubleshooting Rehberi

## 🔍 Backend Bağlantı Sorunları

### Sorun: "Backend'e bağlanılamıyor" hatası alıyorum ama backend çalışıyor

#### Kontrol Listesi:

1. **Backend Durumu Kontrolü**
   ```bash
   # PowerShell'de:
   curl http://localhost:8001/health
   # veya tarayıcıda: http://localhost:8001/health
   ```

2. **Port Kontrolü**
   ```powershell
   netstat -ano | findstr :8001
   ```
   Port 8001'de LISTENING görünmeli.

3. **CORS Kontrolü**
   - Backend terminalinde CORS log'larını kontrol edin
   - Frontend'in origin'i CORS listesinde olmalı
   - Varsayılan: `http://localhost:3001`

4. **Tarayıcı Konsolu (F12)**
   - Network sekmesinde istekleri kontrol edin
   - CORS hatası var mı?
   - Request URL doğru mu?

5. **API URL Kontrolü**
   - Frontend console'da: `console.log('API_BASE_URL:', import.meta.env.VITE_API_BASE_URL)`
   - Beklenen: `http://localhost:8001/api`

### Çözümler:

#### Çözüm 1: Backend'i Yeniden Başlat
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

#### Çözüm 2: CORS Ayarlarını Kontrol Et
`backend/app/main.py` dosyasında CORS origins listesini kontrol edin:
```python
allowed_origins = [
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]
```

#### Çözüm 3: Frontend'i Yeniden Başlat
```bash
cd frontend
npm run dev
```

#### Çözüm 4: Tarayıcı Cache'ini Temizle
- Ctrl+Shift+Delete
- Cache ve cookies'i temizle
- Sayfayı hard refresh: Ctrl+F5

## 🐛 Yaygın Hatalar

### 405 Method Not Allowed
**Sebep**: Endpoint yanlış HTTP metodu kullanıyor.

**Çözüm**: 
- Word endpoint'i için PUT kullanın, GET değil
- Word bilgisi text map'ten alınmalı

### CORS Error
**Sebep**: Backend frontend'in origin'ine izin vermiyor.

**Çözüm**:
1. Backend'de CORS origins listesine frontend URL'ini ekleyin
2. Backend'i yeniden başlatın

### Network Error
**Sebep**: Backend çalışmıyor veya erişilemiyor.

**Çözüm**:
1. Backend process'ini kontrol edin
2. Port çakışması var mı kontrol edin
3. Firewall ayarlarını kontrol edin

## 📝 Debug İpuçları

1. **Backend Logları**: Backend terminalinde hata mesajlarını kontrol edin
2. **Frontend Console**: F12 → Console sekmesi
3. **Network Tab**: F12 → Network sekmesi → İstekleri inceleyin
4. **API Test**: Postman veya curl ile endpoint'leri test edin

## ✅ Hızlı Test

```powershell
# Backend health check
curl http://localhost:8001/health

# API endpoint test
curl http://localhost:8001/api/pdfs/{uuid}/pages/1/text-map
```
