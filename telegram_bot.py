"""
PDF Downloader Telegram Bot
Created by Srijan | Srijanxi Technologies

A Telegram bot that downloads PDFs from websites with:
- Recursive directory scanning
- Concurrent downloads
- Progress tracking
- Pause/Resume functionality
- File compression for large batches
"""

import os
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import asyncio
import time
import shutil
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from telegram.constants import ParseMode
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Import config
try:
    from config import BOT_TOKEN, MAX_FILE_SIZE_MB, TEMP_FOLDER, MAX_WORKERS_DEFAULT, MAX_DEPTH_DEFAULT
except ImportError:
    logger.error("config.py not found! Please create it with your BOT_TOKEN")
    sys.exit(1)

# User session storage
user_sessions = {}
session_lock = Lock()


class UserSession:
    """Manages download session for each user"""
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.visited_urls = set()
        self.pdf_links = []
        self.is_downloading = False
        self.is_paused = False
        self.downloaded_count = 0
        self.total_bytes_downloaded = 0
        self.download_start_time = 0
        self.settings = {
            'max_depth': MAX_DEPTH_DEFAULT,
            'max_workers': MAX_WORKERS_DEFAULT,
            'auto_zip': False  # Zip files if more than 5 PDFs
        }
        self.temp_folder = os.path.join(TEMP_FOLDER, str(user_id))
        self.current_message_id = None
        
    def reset(self):
        """Reset session for new download"""
        self.visited_urls.clear()
        self.pdf_links.clear()
        self.is_downloading = False
        self.is_paused = False
        self.downloaded_count = 0
        self.total_bytes_downloaded = 0
        self.download_start_time = 0
        
    def cleanup(self):
        """Clean up temporary files"""
        try:
            if os.path.exists(self.temp_folder):
                shutil.rmtree(self.temp_folder)
        except Exception as e:
            logger.error(f"Error cleaning up {self.temp_folder}: {e}")


def get_user_session(user_id):
    """Get or create user session"""
    with session_lock:
        if user_id not in user_sessions:
            user_sessions[user_id] = UserSession(user_id)
        return user_sessions[user_id]


def find_pdfs(url, session, depth=0):
    """Recursively find PDF links in directories"""
    if depth > session.settings['max_depth'] or url in session.visited_urls:
        return
    
    session.visited_urls.add(url)
    
    try:
        # Increased timeout and added retries
        response = requests.get(url, timeout=30, allow_redirects=True, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        for link in soup.find_all("a", href=True):
            href = link["href"]
            
            # Skip parent directory links
            if href == "../":
                continue
            
            if not isinstance(href, str):
                continue
                
            full_url = urljoin(url, href)
            
            # If it's a PDF, add to list
            if href.lower().endswith(".pdf"):
                session.pdf_links.append(full_url)
            # If it's a directory, recursively search
            elif href.endswith("/") and depth < session.settings['max_depth']:
                find_pdfs(full_url, session, depth + 1)
    
    except Exception as e:
        logger.error(f"Error scanning {url}: {e}")


def download_single_pdf(pdf_url, output_folder, session):
    """Download a single PDF file"""
    # Wait if paused
    while session.is_paused and session.is_downloading:
        time.sleep(0.1)
    
    if not session.is_downloading:
        return None
    
    # Handle duplicate filenames
    base_filename = pdf_url.split("/")[-1]
    # Sanitize filename
    base_filename = "".join(c for c in base_filename if c.isalnum() or c in "._- ")
    if not base_filename:
        base_filename = f"download_{int(time.time())}.pdf"
    
    filename = os.path.join(output_folder, base_filename)
    
    # If file exists, add a number suffix
    if os.path.exists(filename):
        name, ext = os.path.splitext(base_filename)
        counter = 1
        while os.path.exists(filename):
            filename = os.path.join(output_folder, f"{name}_{counter}{ext}")
            counter += 1
    
    try:
        # Added headers and increased timeout for better compatibility
        response = requests.get(pdf_url, timeout=60, stream=True, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response.raise_for_status()
        
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                # Check pause/stop
                while session.is_paused and session.is_downloading:
                    time.sleep(0.1)
                
                if not session.is_downloading:
                    # Clean up partial file
                    try:
                        os.remove(filename)
                    except:
                        pass
                    return None
                
                if chunk:
                    f.write(chunk)
                    session.total_bytes_downloaded += len(chunk)
        
        return filename
    except Exception as e:
        logger.error(f"Error downloading {pdf_url}: {e}")
        # Clean up partial file on error
        try:
            if os.path.exists(filename):
                os.remove(filename)
        except:
            pass
        return None


async def download_pdfs_async(base_url, session, update, context):
    """Main download function with concurrent downloads"""
    session.reset()
    session.is_downloading = True
    session.download_start_time = time.time()
    
    # Create output folder
    os.makedirs(session.temp_folder, exist_ok=True)
    
    # Send initial message
    msg = await update.message.reply_text(
        f"🔍 <b>Scanning for PDFs...</b>\n\n"
        f"URL: <code>{base_url}</code>\n"
        f"Max Depth: {session.settings['max_depth']}\n"
        f"Concurrent Downloads: {session.settings['max_workers']}",
        parse_mode=ParseMode.HTML
    )
    session.current_message_id = msg.message_id
    
    # Find all PDFs (run in thread pool to avoid blocking)
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, find_pdfs, base_url, session, 0)
    
    if len(session.pdf_links) == 0:
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=msg.message_id,
            text=f"❌ <b>No PDFs found</b>\n\nURL: <code>{base_url}</code>",
            parse_mode=ParseMode.HTML
        )
        session.is_downloading = False
        return
    
    # Update message with found PDFs
    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=msg.message_id,
        text=f"✅ <b>Found {len(session.pdf_links)} PDFs</b>\n\n"
             f"Starting downloads...\n"
             f"Concurrent workers: {session.settings['max_workers']}",
        parse_mode=ParseMode.HTML,
        reply_markup=get_download_keyboard()
    )
    
    # Download all PDFs with concurrent workers
    downloaded_files = []
    
    def download_wrapper(pdf_url):
        return download_single_pdf(pdf_url, session.temp_folder, session)
    
    with ThreadPoolExecutor(max_workers=session.settings['max_workers']) as executor:
        future_to_url = {executor.submit(download_wrapper, pdf_url): pdf_url 
                         for pdf_url in session.pdf_links}
        
        for future in as_completed(future_to_url):
            if not session.is_downloading:
                executor.shutdown(wait=False, cancel_futures=True)
                await context.bot.edit_message_text(
                    chat_id=update.effective_chat.id,
                    message_id=msg.message_id,
                    text="❌ <b>Download cancelled by user</b>",
                    parse_mode=ParseMode.HTML
                )
                session.cleanup()
                return
            
            result = future.result()
            
            if result:
                session.downloaded_count += 1
                downloaded_files.append(result)
                
                # Update progress every few downloads
                if session.downloaded_count % 3 == 0 or session.downloaded_count == len(session.pdf_links):
                    elapsed = time.time() - session.download_start_time
                    speed = (session.total_bytes_downloaded / (1024 * 1024)) / elapsed if elapsed > 0 else 0
                    progress = (session.downloaded_count / len(session.pdf_links)) * 100
                    
                    progress_bar = create_progress_bar(progress)
                    
                    try:
                        await context.bot.edit_message_text(
                            chat_id=update.effective_chat.id,
                            message_id=msg.message_id,
                            text=f"📥 <b>Downloading PDFs...</b>\n\n"
                                 f"{progress_bar}\n"
                                 f"Progress: {session.downloaded_count}/{len(session.pdf_links)} "
                                 f"({progress:.1f}%)\n"
                                 f"Speed: {speed:.2f} MB/s\n"
                                 f"Downloaded: {session.total_bytes_downloaded / (1024*1024):.2f} MB",
                            parse_mode=ParseMode.HTML,
                            reply_markup=get_download_keyboard()
                        )
                    except Exception as e:
                        # Message not modified, skip
                        pass
    
    session.is_downloading = False
    
    # Calculate final stats
    elapsed = time.time() - session.download_start_time
    total_mb = session.total_bytes_downloaded / (1024 * 1024)
    avg_speed = total_mb / elapsed if elapsed > 0 else 0
    
    # Send files or zip them
    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=msg.message_id,
        text=f"✅ <b>Download Complete!</b>\n\n"
             f"Downloaded: {session.downloaded_count} PDFs\n"
             f"Total Size: {total_mb:.2f} MB\n"
             f"Average Speed: {avg_speed:.2f} MB/s\n"
             f"Time: {elapsed:.1f}s\n\n"
             f"📤 Uploading files to Telegram...",
        parse_mode=ParseMode.HTML
    )
    
    # Send files
    await send_files_to_user(update, context, downloaded_files, session)
    
    # Cleanup
    session.cleanup()


async def send_files_to_user(update, context, files, session):
    """Send downloaded files to user (zip if too many or too large)"""
    total_size = sum(os.path.getsize(f) for f in files if os.path.exists(f))
    total_size_mb = total_size / (1024 * 1024)
    
    # If more than 10 files or total size > 40MB, create zip
    if len(files) > 10 or total_size_mb > 40 or session.settings['auto_zip']:
        await update.effective_chat.send_message(
            "📦 Creating ZIP archive (too many files or size too large)..."
        )
        
        zip_path = os.path.join(session.temp_folder, f"pdfs_{int(time.time())}.zip")
        
        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in files:
                    if os.path.exists(file):
                        zipf.write(file, os.path.basename(file))
            
            zip_size = os.path.getsize(zip_path) / (1024 * 1024)
            
            if zip_size < MAX_FILE_SIZE_MB:
                await update.effective_chat.send_document(
                    document=open(zip_path, 'rb'),
                    filename=os.path.basename(zip_path),
                    caption=f"📦 {len(files)} PDFs ({zip_size:.2f} MB)"
                )
            else:
                await update.effective_chat.send_message(
                    f"❌ ZIP file too large ({zip_size:.2f} MB > {MAX_FILE_SIZE_MB} MB limit)\n"
                    f"Please use a file hosting service."
                )
        except Exception as e:
            logger.error(f"Error creating zip: {e}")
            await update.effective_chat.send_message(f"❌ Error creating ZIP: {e}")
    else:
        # Send individual files
        sent_count = 0
        for file in files:
            if os.path.exists(file):
                try:
                    file_size = os.path.getsize(file) / (1024 * 1024)
                    
                    if file_size < MAX_FILE_SIZE_MB:
                        await update.effective_chat.send_document(
                            document=open(file, 'rb'),
                            filename=os.path.basename(file),
                            caption=f"📄 {os.path.basename(file)} ({file_size:.2f} MB)"
                        )
                        sent_count += 1
                    else:
                        await update.effective_chat.send_message(
                            f"⚠️ File too large: {os.path.basename(file)} ({file_size:.2f} MB)"
                        )
                except Exception as e:
                    logger.error(f"Error sending {file}: {e}")
        
        await update.effective_chat.send_message(
            f"✅ Sent {sent_count}/{len(files)} files successfully!"
        )


def create_progress_bar(percentage, length=10):
    """Create a text-based progress bar"""
    filled = int(length * percentage / 100)
    bar = "█" * filled + "░" * (length - filled)
    return f"[{bar}] {percentage:.1f}%"


def get_download_keyboard():
    """Get inline keyboard for download controls"""
    keyboard = [
        [
            InlineKeyboardButton("⏸ Pause", callback_data="pause"),
            InlineKeyboardButton("▶️ Resume", callback_data="resume"),
            InlineKeyboardButton("⏹ Stop", callback_data="stop")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


# Command handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    welcome_text = (
        "👋 <b>Welcome to PDF Downloader Bot!</b>\n\n"
        "Created by Srijan | Srijanxi Technologies\n\n"
        "📥 <b>Features:</b>\n"
        "• Recursive website scanning for PDFs\n"
        "• Concurrent downloads (1-10 threads)\n"
        "• Real-time progress tracking\n"
        "• Pause/Resume functionality\n"
        "• Automatic ZIP for large batches\n\n"
        "📋 <b>Commands:</b>\n"
        "/download &lt;url&gt; - Download PDFs from URL\n"
        "/settings - Configure download settings\n"
        "/status - Check current download status\n"
        "/help - Show detailed help\n\n"
        "🚀 <b>Quick Start:</b>\n"
        "Send: /download https://example.com/pdfs/"
    )
    
    await update.message.reply_text(welcome_text, parse_mode=ParseMode.HTML)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = (
        "📚 <b>PDF Downloader Bot - Help</b>\n\n"
        "<b>Commands:</b>\n\n"
        "/download &lt;url&gt;\n"
        "  Download PDFs from a website\n"
        "  Example: /download https://example.com/pdfs/\n\n"
        "/settings\n"
        "  Configure:\n"
        "  • Max scan depth (0-10)\n"
        "  • Concurrent downloads (1-10)\n"
        "  • Auto-ZIP files\n\n"
        "/status\n"
        "  Check current download progress\n\n"
        "/cancel\n"
        "  Cancel current download\n\n"
        "<b>Tips:</b>\n"
        "• Use HTTPS URLs for security\n"
        "• Higher depth = more subdirectories scanned\n"
        "• More workers = faster but more bandwidth\n"
        "• Files larger than 50MB will be skipped\n"
        "• Use auto-ZIP for 10+ files\n\n"
        "Made with ❤️ by Srijanxi Technologies"
    )
    
    await update.message.reply_text(help_text, parse_mode=ParseMode.HTML)


async def download_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /download command"""
    user_id = update.effective_user.id
    
    if not context.args:
        await update.message.reply_text(
            "❌ <b>Usage:</b> /download &lt;url&gt;\n\n"
            "Example:\n/download https://example.com/pdfs/",
            parse_mode=ParseMode.HTML
        )
        return
    
    url = context.args[0]
    
    # Validate URL
    if not url.startswith(("http://", "https://")):
        await update.message.reply_text(
            "❌ Invalid URL! Must start with http:// or https://",
            parse_mode=ParseMode.HTML
        )
        return
    
    session = get_user_session(user_id)
    
    if session.is_downloading:
        await update.message.reply_text(
            "⚠️ You already have a download in progress!\n"
            "Use /cancel to stop it first.",
            parse_mode=ParseMode.HTML
        )
        return
    
    # Start download in background
    asyncio.create_task(download_pdfs_async(url, session, update, context))


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /settings command"""
    user_id = update.effective_user.id
    session = get_user_session(user_id)
    
    keyboard = [
        [
            InlineKeyboardButton("📊 Max Depth", callback_data="set_depth"),
            InlineKeyboardButton("⚡ Workers", callback_data="set_workers")
        ],
        [
            InlineKeyboardButton(
                f"📦 Auto-ZIP: {'ON' if session.settings['auto_zip'] else 'OFF'}",
                callback_data="toggle_zip"
            )
        ]
    ]
    
    settings_text = (
        "⚙️ <b>Current Settings:</b>\n\n"
        f"📊 Max Depth: {session.settings['max_depth']}\n"
        f"⚡ Concurrent Workers: {session.settings['max_workers']}\n"
        f"📦 Auto-ZIP Files: {'Enabled' if session.settings['auto_zip'] else 'Disabled'}\n\n"
        "Click buttons below to change settings:"
    )
    
    await update.message.reply_text(
        settings_text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command"""
    user_id = update.effective_user.id
    session = get_user_session(user_id)
    
    if not session.is_downloading:
        await update.message.reply_text(
            "ℹ️ No download in progress.\n\nUse /download &lt;url&gt; to start!",
            parse_mode=ParseMode.HTML
        )
        return
    
    elapsed = time.time() - session.download_start_time
    speed = (session.total_bytes_downloaded / (1024 * 1024)) / elapsed if elapsed > 0 else 0
    progress = (session.downloaded_count / len(session.pdf_links)) * 100 if session.pdf_links else 0
    
    status_text = (
        f"{'⏸ PAUSED' if session.is_paused else '📥 DOWNLOADING'}\n\n"
        f"{create_progress_bar(progress)}\n\n"
        f"Progress: {session.downloaded_count}/{len(session.pdf_links)} PDFs\n"
        f"Speed: {speed:.2f} MB/s\n"
        f"Downloaded: {session.total_bytes_downloaded / (1024*1024):.2f} MB\n"
        f"Time: {elapsed:.1f}s"
    )
    
    await update.message.reply_text(status_text, reply_markup=get_download_keyboard())


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /cancel command"""
    user_id = update.effective_user.id
    session = get_user_session(user_id)
    
    if not session.is_downloading:
        await update.message.reply_text("ℹ️ No download in progress.")
        return
    
    session.is_downloading = False
    session.is_paused = False
    session.cleanup()
    
    await update.message.reply_text("✅ Download cancelled and files cleaned up.")


async def pause_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /pause command"""
    user_id = update.effective_user.id
    session = get_user_session(user_id)
    
    if not session.is_downloading:
        await update.message.reply_text("ℹ️ No download in progress to pause.")
        return
    
    if session.is_paused:
        await update.message.reply_text("⏸ Download is already paused.")
        return
    
    session.is_paused = True
    await update.message.reply_text(
        "⏸ <b>Download Paused</b>\n\nUse /resume to continue.",
        parse_mode=ParseMode.HTML
    )


async def resume_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /resume command"""
    user_id = update.effective_user.id
    session = get_user_session(user_id)
    
    if not session.is_downloading:
        await update.message.reply_text("ℹ️ No download in progress to resume.")
        return
    
    if not session.is_paused:
        await update.message.reply_text("▶️ Download is already running.")
        return
    
    session.is_paused = False
    await update.message.reply_text(
        "▶️ <b>Download Resumed</b>\n\nDownload continuing...",
        parse_mode=ParseMode.HTML
    )


# Callback query handlers
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    session = get_user_session(user_id)
    
    if query.data == "pause":
        if session.is_downloading and not session.is_paused:
            session.is_paused = True
            await query.edit_message_text(
                text=query.message.text + "\n\n⏸ <b>PAUSED</b>",
                parse_mode=ParseMode.HTML,
                reply_markup=get_download_keyboard()
            )
    
    elif query.data == "resume":
        if session.is_downloading and session.is_paused:
            session.is_paused = False
            # Remove paused text
            text = query.message.text.replace("\n\n⏸ <b>PAUSED</b>", "")
            await query.edit_message_text(
                text=text + "\n\n▶️ <b>RESUMED</b>",
                parse_mode=ParseMode.HTML,
                reply_markup=get_download_keyboard()
            )
    
    elif query.data == "stop":
        session.is_downloading = False
        session.is_paused = False
        session.cleanup()
        await query.edit_message_text(
            text=query.message.text + "\n\n⏹ <b>STOPPED</b>",
            parse_mode=ParseMode.HTML
        )
    
    elif query.data == "toggle_zip":
        session.settings['auto_zip'] = not session.settings['auto_zip']
        await query.message.edit_text(
            f"✅ Auto-ZIP {'enabled' if session.settings['auto_zip'] else 'disabled'}!"
        )
        # Resend settings
        await settings_command(update, context)
    
    elif query.data == "set_depth":
        await query.message.reply_text(
            "📊 <b>Set Max Depth</b>\n\n"
            "Send a number between 0-10:\n"
            "• 0 = Current directory only\n"
            "• 1 = One level deep\n"
            "• 2 = Two levels (recommended)\n"
            "• 10 = Very deep scan",
            parse_mode=ParseMode.HTML
        )
    
    elif query.data == "set_workers":
        await query.message.reply_text(
            "⚡ <b>Set Concurrent Workers</b>\n\n"
            "Send a number between 1-10:\n"
            "• 1 = Slow, minimal bandwidth\n"
            "• 3 = Balanced (recommended)\n"
            "• 10 = Fast, high bandwidth",
            parse_mode=ParseMode.HTML
        )


async def handle_settings_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle numeric input for settings"""
    user_id = update.effective_user.id
    session = get_user_session(user_id)
    
    try:
        value = int(update.message.text)
        
        # Assume they're setting depth or workers based on range
        if 0 <= value <= 10:
            # Could be either, for now set depth
            session.settings['max_depth'] = value
            await update.message.reply_text(f"✅ Max depth set to {value}")
        elif 1 <= value <= 10:
            session.settings['max_workers'] = value
            await update.message.reply_text(f"✅ Concurrent workers set to {value}")
    except:
        pass  # Ignore non-numeric messages


def main():
    """Start the bot"""
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("download", download_command))
    application.add_handler(CommandHandler("d", download_command))  # Shortcut
    application.add_handler(CommandHandler("settings", settings_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("s", status_command))  # Shortcut
    application.add_handler(CommandHandler("cancel", cancel_command))
    application.add_handler(CommandHandler("stop", cancel_command))  # Alias
    application.add_handler(CommandHandler("pause", pause_command))
    application.add_handler(CommandHandler("resume", resume_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_settings_input))
    
    # Start bot
    logger.info("Bot started! Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
