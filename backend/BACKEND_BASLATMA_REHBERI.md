# Backend Başlatma Rehberi

## Sorun: Backend çalışmıyor

Backend'e bağlanamıyorsanız, backend çalışmıyor demektir.

## Hızlı Çözüm (Otomatik)

### Windows'ta:

**Yöntem 1: Batch dosyası (Kolay)**
1. `backend` klasörüne gidin
2. `BASLAT.bat` dosyasına çift tıklayın
3. Backend otomatik olarak başlayacak

**Yöntem 2: PowerShell script**
1. PowerShell'i yönetici olarak açın
2. `backend` klasörüne gidin
3. Şunu çalıştırın:
   ```powershell
   .\BASLAT.ps1
   ```

## Manuel Çözüm (Adım Adım)

### 1. Terminal/PowerShell'i açın

`backend` klasörüne gidin:
```powershell
cd C:\wamp64\www\PDFXYZSON\backend
```

### 2. Virtual Environment Oluşturun (İlk kez)

```powershell
python -m venv .venv
```

### 3. Virtual Environment'ı Aktif Edin

**PowerShell'de:**
```powershell
.\.venv\Scripts\Activate.ps1
```

Eğer hata alırsanız (execution policy):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**CMD'de:**
```cmd
.venv\Scripts\activate.bat
```

### 4. Bağımlılıkları Yükleyin

```powershell
pip install -r requirements.txt
```

Bu işlem 2-3 dakika sürebilir.

### 5. Veritabanını Başlatın (İlk kez)

```powershell
python -m app.db.init_db
```

### 6. Backend'i Başlatın

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

## Başarı Kontrolü

Backend başladığında şunu görmelisiniz:

```
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
AeroPdf API started successfully
INFO:     Application startup complete.
```

## Tarayıcıda Test Edin

1. **Health Check**: http://localhost:8001/health
   - Beklenen: `{"status":"healthy"}`

2. **API Docs**: http://localhost:8001/docs
   - Swagger UI açılmalı

## Yaygın Hatalar ve Çözümleri

### Hata: "python: command not found"
**Çözüm**: Python yüklü değil. [Python 3.11+](https://www.python.org/downloads/) yükleyin.

### Hata: "pip: command not found"
**Çözüm**: Python yüklenirken "Add Python to PATH" seçeneğini işaretleyin veya Python'u yeniden yükleyin.

### Hata: "ExecutionPolicy" (PowerShell)
**Çözüm**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Hata: "Port 8001 already in use"
**Çözüm**: Port'u kullanan uygulamayı kapatın veya farklı bir port kullanın:
```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
```

### Hata: "ModuleNotFoundError"
**Çözüm**: Bağımlılıklar yüklenmemiş. `pip install -r requirements.txt` çalıştırın.

## Backend'i Durdurma

Terminal'de `CTRL+C` basın.

## Sonraki Adım

Backend çalıştıktan sonra, **yeni bir terminal** açın ve frontend'i başlatın:

```powershell
cd C:\wamp64\www\PDFXYZSON\frontend
npm install
npm run dev
```

