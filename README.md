# 🎵 YouTube MP3 Downloader

A simple Python tool to download audio from YouTube videos as MP3 files.

## Features

- ✅ Download audio from YouTube videos as MP3
- ✅ Support for various YouTube URL formats (youtube.com, youtu.be, shorts)
- ✅ Customizable audio quality (128, 192, 256, 320 kbps)
- ✅ Multiple audio format support (MP3, AAC, M4A, OPUS, WAV, FLAC)
- ✅ Interactive and command-line modes
- ✅ Automatic retry on failure
- ✅ Progress indicator during download

## Requirements

- Python 3.8+
- FFmpeg (required for audio conversion)

## Installation

1. Clone or copy this project
2. Active virtual environment:
```bash
source venv/bin/activate
```
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Make sure FFmpeg is installed on your system:

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS (Homebrew)
brew install ffmpeg

# Windows (Chocolatey)
choco install ffmpeg
```

## Usage

### Command Line

```bash
# Basic download
python main.py https://www.youtube.com/watch?v=VIDEO_ID

# Custom output directory
python main.py https://www.youtube.com/watch?v=VIDEO_ID -o ./my_music

# High quality (320kbps)
python main.py https://www.youtube.com/watch?v=VIDEO_ID -q 320

# Custom filename
python main.py https://www.youtube.com/watch?v=VIDEO_ID -n "my_favorite_song"

# Different format (e.g., FLAC)
python main.py https://www.youtube.com/watch?v=VIDEO_ID -f flac

# Get video info only
python main.py https://www.youtube.com/watch?v=VIDEO_ID --info
```

### Interactive Mode

```bash
python main.py --interactive
# or just
python main.py
```

### As a Python Module

```python
from downloader import YouTubeMP3Downloader

# Initialize downloader
downloader = YouTubeMP3Downloader(
    output_dir="./my_music",
    audio_quality="320",
    audio_format="mp3"
)

# Get video info
info = downloader.get_video_info("https://www.youtube.com/watch?v=VIDEO_ID")
print(f"Title: {info['title']}")

# Download single video
result = downloader.download("https://www.youtube.com/watch?v=VIDEO_ID")
print(f"Downloaded: {result}")

# Download multiple videos
urls = [
    "https://www.youtube.com/watch?v=VIDEO_ID_1",
    "https://www.youtube.com/watch?v=VIDEO_ID_2",
]
results = downloader.download_multiple(urls)
```

## Configuration

Edit `config.py` to change default settings:

```python
# Default download directory
DOWNLOADS_DIR = BASE_DIR / "downloads"

# Default audio format and quality
DEFAULT_AUDIO_FORMAT = "mp3"
DEFAULT_AUDIO_QUALITY = "192"  # kbps

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
```

## Project Structure

```
youtube-mp3-downloader/
├── config.py           # Configuration settings
├── downloader.py       # Main downloader class
├── main.py             # CLI entry point
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── downloads/          # Default download directory
└── utils/
    ├── __init__.py
    ├── helpers.py      # Helper utilities
    └── logger.py       # Logging configuration
```

## Legal Notice

⚠️ **Disclaimer**: This tool is for personal use only. Please respect copyright laws and YouTube's Terms of Service. Only download content that you have the right to download.

## License

MIT License
