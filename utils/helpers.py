"""Helper utilities for YouTube MP3 Downloader"""
import os
import re
from pathlib import Path

def get_video_id_from_url(url):
    """Extract YouTube video ID from URL
    
    Args:
        url: YouTube video URL (supports various formats)
    
    Returns:
        str: Video ID or None if not found
    """
    # Handle youtu.be short URLs
    if "youtu.be" in url:
        return url.split("/")[-1].split("?")[0]
    
    # Handle youtube.com URLs
    elif "youtube.com" in url:
        # Extract from watch URL format
        if "v=" in url:
            video_id = url.split("v=")[1]
            amp_pos = video_id.find("&")
            if amp_pos != -1:
                return video_id[:amp_pos]
            return video_id
        
        # Handle /shorts/ URLs
        elif "/shorts/" in url:
            match = re.search(r'/shorts/([a-zA-Z0-9_-]+)', url)
            if match:
                return match.group(1)
        
        # Handle /embed/ URLs
        elif "/embed/" in url:
            match = re.search(r'/embed/([a-zA-Z0-9_-]+)', url)
            if match:
                return match.group(1)
    
    return None

def sanitize_filename(filename):
    """Sanitize a filename by removing invalid characters
    
    Args:
        filename: Filename to sanitize
    
    Returns:
        str: Sanitized filename
    """
    if isinstance(filename, Path):
        filename = str(filename)
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def format_duration(seconds):
    """Format duration in seconds to HH:MM:SS format
    
    Args:
        seconds: Duration in seconds
    
    Returns:
        str: Formatted duration string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"

def format_filesize(bytes_size):
    """Format file size in bytes to human-readable format
    
    Args:
        bytes_size: Size in bytes
    
    Returns:
        str: Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.2f} TB"
