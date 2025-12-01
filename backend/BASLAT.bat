@echo off
chcp 65001 >nul
echo ========================================
echo AeroPdf - Backend Baslat
echo ========================================
echo.
echo NOT: Bu pencereyi KAPATMAYIN!
echo Backend bu pencerede calisacak.
echo.
pause
echo.

REM Virtual environment kontrolu
if not exist .venv (
    echo [1/4] Virtual environment olusturuluyor...
    python -m venv .venv
    if errorlevel 1 (
        echo HATA: Virtual environment olusturulamadi!
        pause
        exit /b 1
    )
    echo Virtual environment olusturuldu.
) else (
    echo [1/4] Virtual environment zaten var.
)

echo.
echo [2/4] Virtual environment aktif ediliyor...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo HATA: Virtual environment aktif edilemedi!
    pause
    exit /b 1
)

echo.
echo [3/4] Bagimliliklari yukleniyor...
pip install -r requirements.txt
if errorlevel 1 (
    echo HATA: Bagimliliklar yuklenemedi!
    pause
    exit /b 1
)

echo.
echo [4/4] Veritabani baslatiliyor...
python -m app.db.init_db
if errorlevel 1 (
    echo UYARI: Veritabani baslatilamadi (ilk calistirma olabilir).
)

echo.
echo ========================================
echo Backend baslatiliyor...
echo ========================================
echo.
echo Backend su adreste calisacak: http://localhost:8001
echo API Dokumantasyon: http://localhost:8001/docs
echo.
echo Durdurmak icin CTRL+C basiniz.
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

pause

