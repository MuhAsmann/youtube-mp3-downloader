"""Configuration settings for YouTube MP3 Downloader"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Download settings
DOWNLOADS_DIR = BASE_DIR / "downloads"
DEFAULT_AUDIO_FORMAT = "mp3"
DEFAULT_AUDIO_QUALITY = "192"  # kbps

# Create directories if they don't exist
DOWNLOADS_DIR.mkdir(exist_ok=True)

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
