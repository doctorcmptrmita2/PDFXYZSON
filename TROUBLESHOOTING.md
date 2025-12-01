# Sorun Giderme Rehberi

## Frontend Bağlantı Sorunları

### "localhost:3001 sunucusuyla bağlantı kuramıyor" Hatası

Bu hata genellikle frontend development server'ın çalışmadığı anlamına gelir.

#### Çözüm Adımları:

1. **Frontend'in çalışıp çalışmadığını kontrol edin:**

   Terminal/PowerShell'de `frontend` dizinine gidin:
   ```bash
   cd frontend
   ```

2. **Development server'ı başlatın:**
   ```bash
   npm run dev
   ```

3. **Terminal çıktısını kontrol edin:**
   
   Şuna benzer bir çıktı görmelisiniz:
   ```
   VITE v5.x.x  ready in xxx ms

   ➜  Local:   http://localhost:3001/
   ➜  Network: http://192.168.x.x:3001/
   ```

4. **Port numarasını kontrol edin:**
   
   Eğer port 3001 kullanılıyorsa, Vite otomatik olarak farklı bir port kullanacaktır (örn: 3002, 3003). Terminal'de gösterilen gerçek portu kullanın.

#### Yaygın Sorunlar:

**Problem: "npm: command not found"**
- **Çözüm**: Node.js yüklü değil. [Node.js](https://nodejs.org/) v20 veya üzeri sürümü yükleyin.

**Problem: "Cannot find module" hataları**
- **Çözüm**: Bağımlılıklar yüklenmemiş. Şunu çalıştırın:
  ```bash
  cd frontend
  npm install
  ```

**Problem: Port zaten kullanılıyor**
- **Çözüm**: Vite otomatik olarak bir sonraki boş portu kullanacaktır. Terminal çıktısındaki portu kullanın veya `vite.config.ts` dosyasında farklı bir port belirtin.

**Problem: "EADDRINUSE" hatası**
- **Çözüm**: Port başka bir uygulama tarafından kullanılıyor. O uygulamayı kapatın veya `vite.config.ts`'de farklı bir port kullanın.

## Backend Bağlantı Sorunları

### Backend'e bağlanamıyorum

1. **Backend'in çalışıp çalışmadığını kontrol edin:**
   ```bash
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
   ```

2. **Tarayıcıda test edin:**
   - `http://localhost:8001/health` - "healthy" dönmeli
   - `http://localhost:8001/docs` - API dokümantasyonu açılmalı

3. **CORS hatası alıyorsanız:**
   - Backend'in `app/main.py` dosyasında frontend portunun CORS listesinde olduğundan emin olun.

## Docker Sorunları

### Container'lar başlamıyor

1. **Docker'ın çalıştığından emin olun**

2. **Logları kontrol edin:**
   ```bash
   docker-compose logs backend
   docker-compose logs frontend
   ```

3. **Yeniden build edin:**
   ```bash
   docker-compose down
   docker-compose up --build
   ```

### Port çakışması

Eğer portlar zaten kullanılıyorsa, `docker-compose.yml` dosyasındaki port mapping'leri değiştirin.

## Genel İpuçları

1. **Her zaman terminal çıktılarını kontrol edin** - Hata mesajları genellikle orada görünür.

2. **Port numaralarını doğrulayın** - Frontend ve backend'in farklı portlarda çalıştığından emin olun.

3. **Firewall ayarlarını kontrol edin** - Windows Firewall veya antivirüs yazılımı bağlantıları engelliyor olabilir.

4. **Node.js ve Python sürümlerini kontrol edin:**
   - Node.js: `node --version` (v20+ olmalı)
   - Python: `python --version` (v3.11+ olmalı)

