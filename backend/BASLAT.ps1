# AeroPdf - Backend Başlat Script (PowerShell)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "AeroPdf - Backend Başlat" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Virtual environment kontrolü
if (-not (Test-Path .venv)) {
    Write-Host "[1/4] Virtual environment oluşturuluyor..." -ForegroundColor Yellow
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "HATA: Virtual environment oluşturulamadı!" -ForegroundColor Red
        Read-Host "Devam etmek için Enter'a basın"
        exit 1
    }
    Write-Host "Virtual environment oluşturuldu." -ForegroundColor Green
} else {
    Write-Host "[1/4] Virtual environment zaten var." -ForegroundColor Green
}

Write-Host ""
Write-Host "[2/4] Virtual environment aktif ediliyor..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "HATA: Virtual environment aktif edilemedi!" -ForegroundColor Red
    Write-Host "Çözüm: PowerShell'de execution policy'yi değiştirin:" -ForegroundColor Yellow
    Write-Host "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    Read-Host "Devam etmek için Enter'a basın"
    exit 1
}

Write-Host ""
Write-Host "[3/4] Bağımlılıklar yükleniyor..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "HATA: Bağımlılıklar yüklenemedi!" -ForegroundColor Red
    Read-Host "Devam etmek için Enter'a basın"
    exit 1
}

Write-Host ""
Write-Host "[4/4] Veritabanı başlatılıyor..." -ForegroundColor Yellow
python -m app.db.init_db
if ($LASTEXITCODE -ne 0) {
    Write-Host "UYARI: Veritabanı başlatılamadı (ilk çalıştırma olabilir)." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Backend başlatılıyor..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend şu adreste çalışacak: http://localhost:8001" -ForegroundColor Green
Write-Host "API Dokümantasyon: http://localhost:8001/docs" -ForegroundColor Green
Write-Host ""
Write-Host "Durdurmak için CTRL+C basınız." -ForegroundColor Yellow
Write-Host ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

