# 🤖 Bot Commands Reference

## 📋 Complete Command List

### **Basic Commands**

#### `/start`
**Description:** Start the bot and see welcome message  
**Usage:** `/start`  
**Example:**
```
/start
```
**Output:** Welcome message with bot features and quick start guide

---

#### `/help`
**Description:** Display detailed help information and usage tips  
**Usage:** `/help`  
**Example:**
```
/help
```
**Output:** Comprehensive help with all commands, tips, and best practices

---

### **Download Commands**

#### `/download <url>` or `/d <url>`
**Description:** Download all PDFs from a website URL  
**Usage:** `/download <url>` or `/d <url>` (shortcut)  
**Required:** URL must start with http:// or https://  
**Examples:**
```
/download https://www.irs.gov/pub/irs-pdf/
/d https://example.com/documents/
/download https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf
```
**Features:**
- ✅ Automatically scans for PDFs
- ✅ Shows progress in real-time
- ✅ Downloads multiple files concurrently
- ✅ Uploads files directly to Telegram
- ✅ Auto-zips large batches (>10 files or >40MB)

---

### **Control Commands**

#### `/pause`
**Description:** Pause the current download  
**Usage:** `/pause` (or click ⏸ Pause button)  
**Example:**
```
/pause
```
**Note:** Can also use inline keyboard button during download

---

#### `/resume`
**Description:** Resume a paused download  
**Usage:** `/resume` (or click ▶️ Resume button)  
**Example:**
```
/resume
```
**Note:** Can also use inline keyboard button

---

#### `/cancel` or `/stop`
**Description:** Cancel current download and cleanup temporary files  
**Usage:** `/cancel` or `/stop`  
**Example:**
```
/cancel
/stop
```
**Output:** Confirmation message and cleanup status

---

### **Status & Monitoring**

#### `/status` or `/s`
**Description:** Check current download progress and statistics  
**Usage:** `/status` or `/s` (shortcut)  
**Example:**
```
/status
/s
```
**Shows:**
- 📊 Progress percentage
- 📥 Downloaded files count
- ⚡ Download speed (MB/s)
- 💾 Total data downloaded
- ⏱️ Elapsed time
- ⏸ Pause/Resume status

---

### **Configuration Commands**

#### `/settings`
**Description:** Configure bot settings (depth, workers, auto-zip)  
**Usage:** `/settings`  
**Example:**
```
/settings
```
**Configurable Options:**
- **📊 Max Depth** (0-10) - How deep to scan directories
- **⚡ Concurrent Workers** (1-10) - Number of simultaneous downloads
- **📦 Auto-ZIP** (ON/OFF) - Automatically compress files

**Settings Details:**

**Max Depth:**
- `0` = Current directory only
- `1` = One level deep
- `2` = Two levels (default, recommended)
- `5` = Deep scan
- `10` = Very deep scan (slower)

**Concurrent Workers:**
- `1` = Slow, minimal bandwidth
- `3` = Balanced (default, recommended)
- `5` = Fast, good for stable connections
- `10` = Very fast, high bandwidth usage

**Auto-ZIP:**
- `ON` = Always compress files
- `OFF` = Only zip if >10 files or >40MB (default behavior)

**How to Configure:**
1. Use `/settings` command
2. Click button to select option
3. For depth/workers: Type a number between the valid range
4. For auto-zip: Toggle with button click

---

## 🎯 Advanced Usage Examples

### **Example 1: Quick Single File Download**
```
/download https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf
# Or use shortcut:
/d https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf
```

### **Example 2: Download with Custom Settings**
```
Step 1: /settings
Step 2: Click "📊 Max Depth" and type: 3
Step 3: Click "⚡ Workers" and type: 5
Step 4: /d https://example.com/archive/
```

### **Example 3: Large Batch Download**
```
Step 1: /settings
Step 2: Click "📦 Auto-ZIP" to enable
Step 3: Click "⚡ Workers" and type: 8
Step 4: /download https://www.irs.gov/pub/irs-pdf/
```

### **Example 4: Monitor Active Download**
```
Step 1: /download https://example.com/pdfs/
Step 2: /s (check progress - shortcut)
Step 3: Click ⏸ Pause (if needed)
Step 4: Click ▶️ Resume (to continue)
Step 5: Click ⏹ Stop or use /stop to cancel
```

---

## 📝 Command Workflow

### **Complete Download Workflow:**

1. **Configure Settings** (Optional)
   ```
   /settings
   ```

2. **Start Download**
   ```
   /download <url>
   ```

3. **Monitor Progress** (During download)
   ```
   /status
   ```

4. **Control Download** (If needed)
   - Pause: Click ⏸ button or `/pause`
   - Resume: Click ▶️ button or `/resume`
   - Stop: Click ⏹ button or `/cancel`

5. **Receive Files**
   - Individual files sent to chat
   - Or ZIP file if batch is large

---

## ⚙️ Settings Details

### **Max Depth Configuration**

| Depth | Behavior | Use Case |
|-------|----------|----------|
| 0 | Current directory only | Single page with PDFs |
| 1 | One subdirectory | Simple folder structure |
| 2 | Two levels deep | Most websites (default) |
| 3-5 | Deep scanning | Complex archives |
| 6-10 | Very deep | Large document repositories |

### **Worker Configuration**

| Workers | Speed | Bandwidth | Use Case |
|---------|-------|-----------|----------|
| 1 | Slow | Low | Slow connection |
| 2-3 | Moderate | Medium | Standard usage (default) |
| 4-6 | Fast | High | Fast connection |
| 7-10 | Very Fast | Very High | Excellent connection |

---

## 🔧 Troubleshooting Commands

### **Bot Not Responding?**
```
/start
```
Re-initializes the bot connection

### **Stuck Download?**
```
/stop
/d <url>
```
Cancel and retry (use shortcuts for faster access)

### **Check Current Status?**
```
/s
```
View download progress and state (shortcut command)

### **Reset Settings?**
```
/settings
```
Set back to defaults (Depth: 2, Workers: 3, Auto-ZIP: OFF)
Note: Settings are per-user and persist during bot session

---

## 💡 Pro Tips

### **Tip 1: Test First**
```
# First check with single file (use shortcut)
/d https://example.com/test.pdf

# Then do full download
/d https://example.com/all-pdfs/
```

### **Tip 2: Optimize Speed**
```
/settings
Click "⚡ Workers" button
# Set workers based on your internet:
# - Mobile data: type 1-2
# - Home WiFi: type 3-5 (default: 3)
# - Fast fiber: type 8-10
```

### **Tip 3: Handle Large Sites**
```
/settings
# Click "📊 Max Depth" and type 1-2 for faster scanning (default: 2)
# Click "📦 Auto-ZIP" to enable for easier file management
```

### **Tip 4: Monitor Progress**
```
# Start download (use shortcut)
/d <url>

# Check progress (use shortcut)
/s

# Control options:
# - Click ⏸ Pause button or use /pause
# - Click ▶️ Resume button or use /resume
# - Click ⏹ Stop button or use /stop
```

---

## 📊 Command Priorities

### **Essential (Use Always)**
- `/start` - Initialize bot
- `/download <url>` - Main function
- `/help` - Get help

### **Important (Use Often)**
- `/settings` - Configure before downloads
- `/status` - Monitor progress
- `/cancel` - Stop if needed

### **Optional (Use When Needed)**
- Inline buttons (⏸ ⏹ ▶️) - Quick controls
- `/pause` / `/resume` - Manual control

---

## 🚀 Quick Reference Card

| Command | Shortcut/Alias | Function |
|---------|----------------|----------|
| `/start` | - | Welcome & intro |
| `/help` | - | Show help |
| `/download <url>` | `/d <url>` | Download PDFs |
| `/settings` | - | Configure bot |
| `/status` | `/s` | Check progress |
| `/cancel` | `/stop` | Cancel download |
| `/pause` | ⏸ Button | Pause download |
| `/resume` | ▶️ Button | Resume download |
| ⏹ Button | `/cancel` or `/stop` | Stop download |

---

## 📱 Sample URLs for Testing

### **Quick Test (Single PDF)**
```
/download https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf
```

### **Medium Test (Multiple PDFs)**
```
/download https://www.irs.gov/pub/irs-pdf/
```

### **Advanced Test (With Settings)**
```
/settings
Set Depth: 1
Set Workers: 5
/download https://www.irs.gov/pub/irs-pdf/
```

---

## ⚠️ Limitations

- **File Size:** Maximum 50MB per file (Telegram limit)
- **Auto-ZIP Trigger:** Automatically creates ZIP for >10 files or >40MB total (unless auto-zip is enabled)
- **Timeout:** Website requests timeout after 30s (scanning) or 60s (downloading)
- **Rate Limits:** Telegram has upload rate limits
- **Storage:** Temporary files auto-deleted after upload/cancellation
- **User-Agent:** Bot uses Mozilla/5.0 user agent for better compatibility

---

## 📞 Support Commands

If you need help:

1. **Check help:** `/help`
2. **View status:** `/status`
3. **Reset:** `/cancel` then `/start`
4. **Reconfigure:** `/settings`

---

**Created by Srijan | Srijanxi Technologies**  
*Made with ❤️ for easy PDF downloading*
