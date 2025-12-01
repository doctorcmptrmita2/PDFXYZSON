@echo off
chcp 65001 >nul
echo ========================================
echo Backend Yeniden Baslat
echo ========================================
echo.

echo Eski backend process'leri durduruluyor...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8001.*LISTENING"') do (
    echo Process %%a durduruluyor...
    taskkill /F /PID %%a >nul 2>&1
)

timeout /t 2 /nobreak >nul

echo.
echo Virtual environment aktif ediliyor...
call .venv\Scripts\activate.bat

echo.
echo Backend baslatiliyor...
echo.
echo Backend: http://localhost:8001
echo API Docs: http://localhost:8001/docs
echo.
echo Durdurmak icin CTRL+C basiniz.
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

pause

