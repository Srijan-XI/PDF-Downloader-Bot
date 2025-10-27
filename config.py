"""
Configuration file for PDF Downloader Telegram Bot
Created by Srijan | Srijanxi Technologies
"""

import os

# ============================================
# TELEGRAM BOT CONFIGURATION
# ============================================

# Get bot token from environment variable or set it here
BOT_TOKEN = os.getenv("BOT_TOKEN", "8224872646:AAHuknu1JnOL5x0W72XpjNljjR0PfjUytI4")

# If BOT_TOKEN is not set, raise an error with instructions
if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
    print("\n" + "="*60)
    print("⚠️  BOT TOKEN NOT CONFIGURED!")
    print("="*60)
    print("\nPlease set your Telegram Bot Token in one of these ways:\n")
    print("1. Set environment variable:")
    print("   Windows (PowerShell):")
    print("   $env:BOT_TOKEN='your-token-here'")
    print("   python telegram_bot.py\n")
    print("   Linux/macOS:")
    print("   export BOT_TOKEN='your-token-here'")
    print("   python3 telegram_bot.py\n")
    print("2. Edit config.py and replace 'YOUR_BOT_TOKEN_HERE' with your token\n")
    print("3. Create .env file (requires python-dotenv):\n")
    print("   BOT_TOKEN=your-token-here\n")
    print("\n📖 How to get a Bot Token:")
    print("   1. Open Telegram and search for @BotFather")
    print("   2. Send /newbot and follow the instructions")
    print("   3. Copy the token provided\n")
    print("="*60 + "\n")

# ============================================
# DOWNLOAD SETTINGS
# ============================================

# Maximum file size for Telegram uploads (in MB)
# Telegram's limit is 50MB for bots, but we use 48MB for safety
MAX_FILE_SIZE_MB = 48

# Temporary folder for downloads (will be created automatically)
TEMP_FOLDER = os.path.join(os.getcwd(), "temp_downloads")

# Default maximum depth for recursive scanning
MAX_DEPTH_DEFAULT = 2

# Default number of concurrent download workers
MAX_WORKERS_DEFAULT = 3

# ============================================
# ADVANCED SETTINGS
# ============================================

# Request timeout in seconds
REQUEST_TIMEOUT = 30

# Maximum number of PDFs to find (prevent infinite loops)
MAX_PDF_LIMIT = 500

# Auto-cleanup old temp files (in hours)
AUTO_CLEANUP_HOURS = 24

# Enable debug logging
DEBUG_MODE = False
