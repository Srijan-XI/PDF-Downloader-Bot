@echo off
REM PDF Downloader Telegram Bot - Quick Setup Script
REM Created by Srijan | Srijanxi Technologies

echo ========================================
echo PDF Downloader Telegram Bot - Setup
echo ========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo [1/4] Installing dependencies...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/4] Creating temporary download folder...
if not exist "temp_downloads" mkdir temp_downloads

echo.
echo [3/4] Checking configuration...
if not exist "config.py" (
    echo ERROR: config.py not found!
    pause
    exit /b 1
)

echo.
echo [4/4] Setup complete!
echo.
echo ========================================
echo Next Steps:
echo ========================================
echo.
echo 1. Get your Bot Token from @BotFather on Telegram
echo    - Open Telegram and search for @BotFather
echo    - Send /newbot and follow instructions
echo    - Copy the token provided
echo.
echo 2. Set your Bot Token:
echo.
echo    Option A - Environment Variable (Recommended):
echo    $env:BOT_TOKEN='your-token-here'
echo.
echo    Option B - Edit config.py:
echo    Open config.py and replace YOUR_BOT_TOKEN_HERE
echo.
echo 3. Run the bot:
echo    python telegram_bot.py
echo.
echo ========================================
echo.
pause
