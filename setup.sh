#!/bin/bash
# PDF Downloader Telegram Bot - Quick Setup Script
# Created by Srijan | Srijanxi Technologies

echo "========================================"
echo "PDF Downloader Telegram Bot - Setup"
echo "========================================"
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "[1/4] Installing dependencies..."
python3 -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "[2/4] Creating temporary download folder..."
mkdir -p temp_downloads

echo ""
echo "[3/4] Checking configuration..."
if [ ! -f "config.py" ]; then
    echo "ERROR: config.py not found!"
    exit 1
fi

echo ""
echo "[4/4] Setup complete!"
echo ""
echo "========================================"
echo "Next Steps:"
echo "========================================"
echo ""
echo "1. Get your Bot Token from @BotFather on Telegram"
echo "   - Open Telegram and search for @BotFather"
echo "   - Send /newbot and follow instructions"
echo "   - Copy the token provided"
echo ""
echo "2. Set your Bot Token:"
echo ""
echo "   Option A - Environment Variable (Recommended):"
echo "   export BOT_TOKEN='your-token-here'"
echo ""
echo "   Option B - Edit config.py:"
echo "   Open config.py and replace YOUR_BOT_TOKEN_HERE"
echo ""
echo "3. Run the bot:"
echo "   python3 telegram_bot.py"
echo ""
echo "========================================"
echo ""
