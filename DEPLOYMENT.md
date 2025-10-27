# 🚀 Deployment Guide - Render

## Prerequisites

✅ GitHub account with repository  
✅ Render account (sign up at https://render.com)  
✅ Telegram Bot Token from @BotFather

---

## 📋 Step-by-Step Deployment

### **Step 1: Prepare Your Repository**

1. Ensure all files are committed to GitHub:
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. Make sure these files exist in your repo:
   - ✅ `telegram_bot.py` - Main bot file
   - ✅ `requirements.txt` - Python dependencies
   - ✅ `config.py` - Configuration file
   - ✅ `render.yaml` - Render configuration
   - ✅ `runtime.txt` - Python version
   - ✅ `Procfile` - Process file for deployment

---

### **Step 2: Create Render Account**

1. Go to https://render.com
2. Click "Get Started" or "Sign Up"
3. Sign up with GitHub (recommended)
4. Authorize Render to access your repositories

---

### **Step 3: Create New Web Service**

1. From Render Dashboard, click **"New +"** button
2. Select **"Web Service"**
3. Connect your GitHub repository:
   - Click "Connect account" if not connected
   - Find and select `PDF-Downloader-Bot` repository
   - Click **"Connect"**

---

### **Step 4: Configure Service**

Fill in the following settings:

**Basic Settings:**
- **Name:** `pdf-downloader-bot` (or your preferred name)
- **Region:** Choose closest to you (e.g., Singapore, Oregon)
- **Branch:** `main`
- **Root Directory:** (leave empty)
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python telegram_bot.py`

**Instance Type:**
- Select **"Free"** plan ($0/month)
- Note: Free instances spin down after 15 min of inactivity

---

### **Step 5: Add Environment Variables**

Click **"Advanced"** and add environment variables:

1. Click **"Add Environment Variable"**
2. Add your bot token:
   - **Key:** `BOT_TOKEN`
   - **Value:** `your-telegram-bot-token-here`
   - (Get from @BotFather on Telegram)

3. (Optional) Add other variables:
   - **Key:** `MAX_DEPTH_DEFAULT`
   - **Value:** `2`
   
   - **Key:** `MAX_WORKERS_DEFAULT`
   - **Value:** `3`

---

### **Step 6: Deploy**

1. Click **"Create Web Service"** button
2. Wait for deployment (takes 2-5 minutes)
3. Watch the build logs for any errors
4. Once deployed, status will show "Live" (green dot)

---

### **Step 7: Test Your Bot**

1. Open Telegram
2. Search for your bot by username
3. Send `/start` command
4. Test download: `/download https://example.com/test.pdf`

---

## 🔧 Important Notes

### **Free Tier Limitations:**

- ⏸️ **Spins down after 15 minutes** of inactivity
- 🐌 **Cold start delay** when waking up (~30 seconds)
- 📊 **750 hours/month** free usage
- 💾 **Limited disk space** for temporary files

### **Keeping Bot Active (Optional):**

If you want to prevent spin-down:

1. Use a service like **UptimeRobot** or **Cron-job.org**
2. Ping your Render URL every 10 minutes
3. **Note:** This may exhaust free hours faster

### **Upgrading to Paid Plan:**

For 24/7 uptime without spin-down:
- **Starter Plan:** $7/month (always on)
- Better for production use

---

## 🛠️ Troubleshooting

### **Bot Not Responding?**

1. Check Render logs:
   - Go to Dashboard → Your Service
   - Click "Logs" tab
   - Look for errors

2. Check bot token:
   - Environment Variables → Verify `BOT_TOKEN`
   - Test with @BotFather

3. Check deployment status:
   - Should show "Live" with green dot
   - If "Deploy failed", check build logs

### **Build Fails?**

```bash
# Common issues:

1. requirements.txt missing or incorrect
   Solution: Ensure all dependencies are listed

2. Python version mismatch
   Solution: Check runtime.txt has correct version

3. Import errors
   Solution: Check all imports in telegram_bot.py
```

### **Downloads Not Working?**

1. Check temporary folder permissions
2. Verify internet access from Render
3. Check Render logs for specific errors

### **Timeout Errors?**

1. Increase timeout in config.py
2. Reduce MAX_WORKERS_DEFAULT for slow connections
3. Use lower MAX_DEPTH_DEFAULT

---

## 📊 Monitoring Your Bot

### **View Logs:**
1. Go to Render Dashboard
2. Click your service
3. Click "Logs" tab
4. View real-time logs

### **Metrics:**
- CPU usage
- Memory usage
- Request count
- Uptime percentage

---

## 🔄 Updating Your Bot

### **Automatic Deployment:**

Render auto-deploys when you push to GitHub:

```bash
# Make changes locally
git add .
git commit -m "Update bot features"
git push origin main

# Render will automatically:
# 1. Detect the push
# 2. Pull latest code
# 3. Rebuild and redeploy
```

### **Manual Deployment:**

From Render Dashboard:
1. Click your service
2. Click "Manual Deploy"
3. Select "Deploy latest commit"
4. Click "Deploy"

---

## 🔐 Security Best Practices

1. **Never commit tokens:**
   - Use environment variables only
   - Add `.env` to `.gitignore`

2. **Rotate tokens regularly:**
   - Use @BotFather to regenerate
   - Update in Render environment variables

3. **Monitor usage:**
   - Check logs for suspicious activity
   - Set up alerts in Render

---

## 📱 Alternative: Render Blueprint

You can also use the `render.yaml` file for one-click deployment:

1. Push `render.yaml` to your repo
2. Go to Render Dashboard
3. Click "Blueprints" → "New Blueprint Instance"
4. Connect your repository
5. Add environment variables
6. Click "Apply"

---

## 💡 Pro Tips

### **Tip 1: Use Environment-Specific Settings**
```python
# In config.py
import os

DEBUG_MODE = os.getenv("DEBUG", "False") == "True"
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "3"))
```

### **Tip 2: Add Health Check Endpoint**
Add a simple health check for monitoring:
```python
# Optional: Add to telegram_bot.py
# For keeping service alive
```

### **Tip 3: Monitor Disk Usage**
Free tier has limited disk space:
- Clean up temp files regularly
- Use `AUTO_CLEANUP_HOURS` in config

### **Tip 4: Set Up Notifications**
Configure Render to notify you:
- Deploy failures
- Service downtime
- Build errors

---

## 📞 Support Resources

- **Render Docs:** https://render.com/docs
- **Render Discord:** https://discord.gg/render
- **Telegram Bot API:** https://core.telegram.org/bots/api
- **python-telegram-bot:** https://python-telegram-bot.org

---

## ✅ Deployment Checklist

Before deploying, verify:

- [x] All code pushed to GitHub
- [x] `requirements.txt` is up to date
- [x] `render.yaml` configured correctly
- [x] `.gitignore` includes sensitive files
- [x] Bot token obtained from @BotFather
- [x] Render account created
- [x] Repository connected to Render
- [x] Environment variables added
- [x] Bot tested locally

---

## 🎉 You're All Set!

Your PDF Downloader Bot is now deployed on Render!

- **Free tier:** Great for testing and personal use
- **Paid tier:** Recommended for production (always on)

**Created by Srijan | Srijanxi Technologies**  
*Made with ❤️ for easy deployment*
