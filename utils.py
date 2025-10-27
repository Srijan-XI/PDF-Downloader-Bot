"""
Utility functions for PDF Downloader Telegram Bot
Created by Srijan | Srijanxi Technologies
"""

import os
import shutil
import time
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


def cleanup_old_folders(base_folder, hours=24):
    """
    Clean up temporary folders older than specified hours
    
    Args:
        base_folder: Base temporary folder path
        hours: Age threshold in hours
    """
    if not os.path.exists(base_folder):
        return
    
    current_time = time.time()
    threshold = hours * 3600  # Convert to seconds
    
    try:
        for folder_name in os.listdir(base_folder):
            folder_path = os.path.join(base_folder, folder_name)
            
            if os.path.isdir(folder_path):
                # Check folder age
                folder_age = current_time - os.path.getmtime(folder_path)
                
                if folder_age > threshold:
                    logger.info(f"Cleaning up old folder: {folder_path}")
                    shutil.rmtree(folder_path)
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")


def get_folder_size(folder_path):
    """
    Calculate total size of a folder in bytes
    
    Args:
        folder_path: Path to folder
        
    Returns:
        Total size in bytes
    """
    total_size = 0
    
    if not os.path.exists(folder_path):
        return 0
    
    try:
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.exists(filepath):
                    total_size += os.path.getsize(filepath)
    except Exception as e:
        logger.error(f"Error calculating folder size: {e}")
    
    return total_size


def format_bytes(bytes_value):
    """
    Format bytes to human-readable size
    
    Args:
        bytes_value: Size in bytes
        
    Returns:
        Formatted string (e.g., "1.23 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"


def format_duration(seconds):
    """
    Format seconds to human-readable duration
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted string (e.g., "1h 23m 45s")
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    
    if minutes < 60:
        return f"{minutes}m {seconds}s"
    
    hours = minutes // 60
    minutes = minutes % 60
    
    return f"{hours}h {minutes}m {seconds}s"


def sanitize_filename(filename):
    """
    Sanitize filename to remove invalid characters
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Ensure filename is not empty
    if not filename or filename.strip() == '':
        filename = f"file_{int(time.time())}"
    
    return filename.strip()


def ensure_directory(directory_path):
    """
    Ensure directory exists, create if it doesn't
    
    Args:
        directory_path: Path to directory
        
    Returns:
        True if successful, False otherwise
    """
    try:
        os.makedirs(directory_path, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Error creating directory {directory_path}: {e}")
        return False


def is_valid_url(url):
    """
    Validate URL format
    
    Args:
        url: URL string to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not url or not isinstance(url, str):
        return False
    
    # Basic URL validation
    url = url.strip()
    
    if not url.startswith(('http://', 'https://')):
        return False
    
    # Check for common invalid patterns
    if ' ' in url or '\n' in url or '\t' in url:
        return False
    
    return True


def get_file_extension(filename):
    """
    Get file extension from filename
    
    Args:
        filename: Filename or path
        
    Returns:
        Extension with dot (e.g., ".pdf") or empty string
    """
    if not filename:
        return ''
    
    if '.' in filename:
        return '.' + filename.rsplit('.', 1)[-1].lower()
    
    return ''


def count_files(directory, extension=None):
    """
    Count files in a directory
    
    Args:
        directory: Directory path
        extension: Optional file extension filter (e.g., ".pdf")
        
    Returns:
        Number of files
    """
    if not os.path.exists(directory):
        return 0
    
    count = 0
    
    try:
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            
            if os.path.isfile(filepath):
                if extension is None or filename.lower().endswith(extension.lower()):
                    count += 1
    except Exception as e:
        logger.error(f"Error counting files: {e}")
    
    return count


class DownloadStats:
    """Track download statistics"""
    
    def __init__(self):
        self.total_downloads = 0
        self.successful_downloads = 0
        self.failed_downloads = 0
        self.total_bytes = 0
        self.start_time = time.time()
    
    def add_success(self, bytes_downloaded):
        """Record successful download"""
        self.successful_downloads += 1
        self.total_downloads += 1
        self.total_bytes += bytes_downloaded
    
    def add_failure(self):
        """Record failed download"""
        self.failed_downloads += 1
        self.total_downloads += 1
    
    def get_average_speed(self):
        """Get average download speed in MB/s"""
        elapsed = time.time() - self.start_time
        
        if elapsed == 0:
            return 0
        
        return (self.total_bytes / (1024 * 1024)) / elapsed
    
    def get_success_rate(self):
        """Get success rate as percentage"""
        if self.total_downloads == 0:
            return 0
        
        return (self.successful_downloads / self.total_downloads) * 100
    
    def get_summary(self):
        """Get summary statistics"""
        elapsed = time.time() - self.start_time
        
        return {
            'total': self.total_downloads,
            'successful': self.successful_downloads,
            'failed': self.failed_downloads,
            'total_size': format_bytes(self.total_bytes),
            'avg_speed': f"{self.get_average_speed():.2f} MB/s",
            'success_rate': f"{self.get_success_rate():.1f}%",
            'duration': format_duration(elapsed)
        }


def create_progress_emoji(percentage):
    """
    Create emoji-based progress indicator
    
    Args:
        percentage: Progress percentage (0-100)
        
    Returns:
        Emoji string
    """
    if percentage < 25:
        return "🔴"
    elif percentage < 50:
        return "🟡"
    elif percentage < 75:
        return "🟠"
    elif percentage < 100:
        return "🟢"
    else:
        return "✅"


def estimate_time_remaining(current, total, elapsed_seconds):
    """
    Estimate time remaining for download
    
    Args:
        current: Current progress count
        total: Total count
        elapsed_seconds: Elapsed time in seconds
        
    Returns:
        Estimated remaining time string
    """
    if current == 0 or elapsed_seconds == 0:
        return "Calculating..."
    
    rate = current / elapsed_seconds
    remaining = total - current
    
    if rate == 0:
        return "Unknown"
    
    remaining_seconds = remaining / rate
    
    return format_duration(remaining_seconds)
