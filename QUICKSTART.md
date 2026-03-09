# 🚀 Quick Start Guide

## Get Started in 3 Minutes!

### Step 1: Get Bot Token (1 min)
1. Open Telegram
2. Search for `@BotFather`
3. Send `/newbot`
4. Follow the prompts to create your bot
5. **Copy the token** (looks like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Step 2: Setup (1 min)

**Windows:**
```powershell
cd telegraam_bot
.\setup.bat
```

**Linux/macOS:**
```bash
cd telegraam_bot
chmod +x setup.sh
./setup.sh
```

### Step 3: Run Bot (30 seconds)

**Windows:**
```powershell
# Set your token
$env:BOT_TOKEN='paste-your-token-here'

# Run the bot
python telegram_bot.py
```

**Linux/macOS:**
```bash
# Set your token
export BOT_TOKEN='paste-your-token-here'

# Run the bot
python3 telegram_bot.py
```

### Step 4: Use Your Bot!

1. Find your bot in Telegram
2. Send `/start`
3. Try downloading:
   ```
   /download https://example.com/pdfs/
   ```

---

## 📱 Example Usage

### Download PDFs from a website:
```
/download https://www.irs.gov/pub/irs-pdf/
```

### Configure settings:
```
/settings
```
Then click buttons to adjust:
- **Max Depth**: How deep to scan (0-10)
- **Workers**: Concurrent downloads (1-10)
- **Auto-ZIP**: Automatically zip files

### Check progress:
```
/status
```

### Control downloads:
Click inline buttons:
- ⏸ **Pause** - Pause download
- ▶️ **Resume** - Resume download
- ⏹ **Stop** - Cancel and cleanup

---

## ⚡ Common Issues

### "BOT_TOKEN not configured"
**Solution:** Set environment variable before running:
```powershell
# Windows
$env:BOT_TOKEN='your-token'

# Linux/macOS
export BOT_TOKEN='your-token'
```

### "Import could not be resolved"
**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Bot doesn't respond
**Solution:** 
1. Check bot is running
2. Verify token is correct
3. Check internet connection

---

## 💡 Tips

- Use **HTTPS** URLs for security
- Start with **depth=2** for balanced scanning
- Use **3 workers** for normal internet speed
- Enable **auto-ZIP** for 10+ files
- Files over 50MB cannot be sent via Telegram

---

## 🎯 Ready to Go!

Your bot is now ready to download PDFs! 

For detailed documentation, see [README.md](README.md)

**Happy Downloading! 🎉**
