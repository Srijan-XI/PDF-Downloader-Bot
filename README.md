# 🤖 PDF Downloader Telegram Bot

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Telegram Bot API](https://img.shields.io/badge/Telegram-Bot%20API-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**Created by Srijan | Srijanxi Technologies**

A powerful Telegram bot that downloads PDFs from websites with recursive scanning, concurrent downloads, progress tracking, and pause/resume functionality.

---

## ✨ Features

- 🔍 **Recursive Website Scanning** - Automatically discover PDFs in nested directories
- ⚡ **Concurrent Downloads** - Download multiple PDFs simultaneously (1-10 workers)
- 📊 **Real-time Progress Tracking** - Live updates with progress bars and download speed
- ⏸️ **Pause/Resume** - Control downloads with inline buttons
- 📦 **Smart ZIP Compression** - Automatically zip large batches of files
- 🎯 **Per-User Sessions** - Multiple users can download simultaneously
- 🛡️ **Error Handling** - Robust error handling and recovery
- 🎨 **User-friendly Interface** - Intuitive commands and inline keyboards

---

## 📋 Requirements

- Python 3.8 or higher
- A Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- Internet connection

---

## 🚀 Quick Start

### 1️⃣ Get a Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow the instructions
3. Choose a name and username for your bot
4. Copy the token provided (looks like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2️⃣ Install Dependencies

**Windows (PowerShell):**
```powershell
cd telegraam_bot
python -m pip install -r requirements.txt
```

**Linux/macOS:**
```bash
cd telegraam_bot
python3 -m pip install -r requirements.txt
```

### 3️⃣ Configure Bot Token

**Option 1: Environment Variable (Recommended)**

Windows (PowerShell):
```powershell
$env:BOT_TOKEN='your-bot-token-here'
python telegram_bot.py
```

Linux/macOS:
```bash
export BOT_TOKEN='your-bot-token-here'
python3 telegram_bot.py
```

**Option 2: Edit config.py**

Open `config.py` and replace:
```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
```

with your actual token:
```python
BOT_TOKEN = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
```

### 4️⃣ Run the Bot

```bash
python telegram_bot.py
```

You should see:
```
INFO - Bot started! Press Ctrl+C to stop.
```

### 5️⃣ Start Using

1. Open Telegram and search for your bot
2. Send `/start` to begin
3. Use `/download <url>` to download PDFs

---

## 📚 Bot Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Show welcome message and features | `/start` |
| `/help` | Display detailed help and tips | `/help` |
| `/download <url>` | Download PDFs from a website | `/download https://example.com/pdfs/` |
| `/settings` | Configure bot settings | `/settings` |
| `/status` | Check current download progress | `/status` |
| `/cancel` | Cancel current download | `/cancel` |

---

## ⚙️ Settings

Access settings with `/settings` command:

### 📊 Max Depth
- Controls how many directory levels to scan
- Range: 0-10
- Default: 2
- **0** = Current directory only
- **2** = Two levels deep (recommended)
- **10** = Very deep scan (slower)

### ⚡ Concurrent Workers
- Number of simultaneous downloads
- Range: 1-10
- Default: 3
- **1** = Slow, minimal bandwidth
- **3** = Balanced (recommended)
- **10** = Fast, high bandwidth

### 📦 Auto-ZIP
- Automatically compress files
- Enabled when:
  - More than 10 PDFs found
  - Total size exceeds 40MB
- Toggle: ON/OFF

---

## 💡 Usage Examples

### Basic Download
```
/download https://example.com/documents/
```

### Download from Deep Directory
```
1. Send: /settings
2. Set Max Depth to 5
3. Send: /download https://example.com/archive/
```

### Fast Download with Multiple Workers
```
1. Send: /settings
2. Set Concurrent Workers to 8
3. Send: /download https://example.com/files/
```

### Monitor Progress
```
/status
```

### Pause and Resume
Click the inline buttons:
- **⏸ Pause** - Pause current download
- **▶️ Resume** - Resume paused download
- **⏹ Stop** - Cancel and cleanup

---

## 🛠️ Project Structure

```
telegraam_bot/
├── telegram_bot.py       # Main bot application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── .env.example         # Environment template
└── temp_downloads/      # Temporary download folder (auto-created)
```

---

## ⚠️ Limitations

- **File Size**: Telegram bots can only send files up to 50MB
- **Large Batches**: Files are automatically zipped if more than 10 PDFs or total size > 40MB
- **Timeout**: Very large downloads may timeout (use smaller depth or fewer workers)
- **Rate Limits**: Telegram has rate limits for file uploads

---

## 🔧 Advanced Configuration

Edit `config.py` to customize:

```python
# Maximum file size (MB)
MAX_FILE_SIZE_MB = 48

# Temporary download folder
TEMP_FOLDER = "temp_downloads"

# Default settings
MAX_DEPTH_DEFAULT = 2
MAX_WORKERS_DEFAULT = 3

# Request timeout (seconds)
REQUEST_TIMEOUT = 30

# Maximum PDFs to find
MAX_PDF_LIMIT = 500
```

---

## 🐛 Troubleshooting

### Bot doesn't respond
- Check if bot is running (`python telegram_bot.py`)
- Verify bot token is correct
- Check internet connection

### Import errors
```bash
pip install -r requirements.txt
```

### "BOT_TOKEN not configured" error
- Set environment variable or edit `config.py`
- See [Configure Bot Token](#3️⃣-configure-bot-token)

### Files not uploading
- Check file size (must be < 50MB)
- Enable auto-ZIP for large batches
- Check Telegram rate limits

### Downloads are slow
- Increase concurrent workers in settings
- Check internet connection
- Website might have rate limiting

---

## 🔐 Security Tips

1. **Keep Token Secret** - Never share your bot token publicly
2. **Use Environment Variables** - Don't hardcode tokens in files
3. **HTTPS Only** - Only scan HTTPS websites for security
4. **Validate URLs** - Bot validates URLs before scanning
5. **Cleanup** - Temporary files are auto-deleted after upload

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

This project is open source and available for personal and commercial use.

---

## 🆘 Support

If you encounter issues:

1. Check the [Troubleshooting](#🐛-troubleshooting) section
2. Review bot logs for error messages
3. Open an issue on GitHub
4. Contact: Srijanxi Technologies

---

## 🎯 Roadmap

- [ ] Support for other file types (DOCX, XLSX, etc.)
- [ ] Cloud storage integration
- [ ] Download scheduling
- [ ] User authentication
- [ ] Download history
- [ ] Multi-language support
- [ ] Web dashboard

---

## 📊 Performance

- **Scan Speed**: 10-50 URLs/second
- **Download Speed**: Limited by internet connection
- **Concurrent Users**: Unlimited (resource-dependent)
- **File Handling**: Automatic cleanup after upload

---

## 🌟 Credits

**Created with ❤️ by Srijan | Srijanxi Technologies**

Based on the original [PDF-Downloader](https://github.com/Srijan-XI/PDF-Downloader) project.

### Technologies Used:
- [Python Telegram Bot](https://python-telegram-bot.org/) - Telegram Bot API wrapper
- [Requests](https://requests.readthedocs.io/) - HTTP library
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing

---

## 📞 Contact

- **Creator**: Srijan
- **Organization**: Srijanxi Technologies
- **GitHub**: [@Srijan-XI](https://github.com/Srijan-XI)

---

**Happy Downloading! 🎉**
# PDF-Downloader-Bot
# PDF-Downloader-Bot
