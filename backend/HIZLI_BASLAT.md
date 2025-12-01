# ⚡ Backend Hızlı Başlatma

## 🚨 Sorun: Backend çalışmıyor

Backend'e bağlanamıyorsanız, backend çalışmıyor demektir.

## ✅ Çözüm: 3 Adımda Backend'i Başlatın

### Adım 1: PowerShell'i Açın

`backend` klasörüne gidin:
```powershell
cd C:\wamp64\www\PDFXYZSON\backend
```

### Adım 2: Virtual Environment'ı Aktif Edin

```powershell
.\.venv\Scripts\Activate.ps1
```

**Eğer hata alırsanız:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Sonra tekrar deneyin.

### Adım 3: Backend'i Başlatın

**Eğer bağımlılıklar yüklü değilse (ilk kez):**
```powershell
pip install -r requirements.txt
```

**Backend'i başlatın:**
```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

## ✅ Başarı Kontrolü

Backend başladığında şunu görmelisiniz:

```
INFO:     Uvicorn running on http://0.0.0.0:8001
INFO:     Application startup complete.
```

**Tarayıcıda test edin:**
- ✅ http://localhost:8001/health → `{"status":"healthy"}`
- ✅ http://localhost:8001/docs → Swagger UI

## 🔄 Alternatif: Otomatik Başlatma

`BASLAT.bat` dosyasına çift tıklayın - her şeyi otomatik yapar!

## ⚠️ Önemli Notlar

1. **Backend terminali açık kalmalı** - Kapatmayın!
2. **Frontend için yeni terminal açın** - Aynı terminali kullanmayın
3. **Port 8001 boş olmalı** - Başka bir uygulama kullanıyorsa kapatın

## 🐛 Hala Çalışmıyorsa

1. Terminal çıktısını kontrol edin - hata mesajı var mı?
2. Port kontrolü: `netstat -ano | findstr :8001`
3. Python versiyonu: `python --version` (3.11+ olmalı)

