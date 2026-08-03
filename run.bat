@echo off
title VPTradeBot - متاتریدر ۵ داشبورد پیشرفته
cd /d "%~dp0"

echo ============================================
echo   VPTradeBot - MetaTrader 5 Dashboard
echo   در حال راه‌اندازی...
echo ============================================
echo.

:: Check if Python is available
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python first.
    echo [ERROR] پایتون روی سیستم نصب نیست.
    pause
    exit /b 1
)

:: Install dependencies if needed
echo [INFO] Checking dependencies...
py -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [WARN] Some dependencies may not be installed.
)

:: Run the application
echo [INFO] Starting VPTradeBot...
echo.
py vptradebot.py

:: If application exits with error
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Application exited with error code: %errorlevel%
    echo [ERROR] برنامه با خطا متوقف شد.
    pause
)
