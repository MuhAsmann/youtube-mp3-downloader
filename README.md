# 🎵 YouTube MP3 Downloader

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0%2B-green?style=for-the-badge&logo=flask)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

A powerful and easy-to-use tool to download audio from YouTube videos as MP3 files. Available as both a **Web Application** and a **Command Line Interface (CLI)**.

## ✨ Features

- 🎧 **High Quality Audio**: Download audio in various qualities (128, 192, 256, 320 kbps).
- 🚀 **Multiple Formats**: Support for MP3, AAC, M4A, OPUS, WAV, and FLAC.
- 🌐 **Web Interface**: Clean and simple web UI for easy downloading.
- 💻 **CLI Mode**: Powerful command-line interface for automation and power users.
- 🔄 **Smart Handling**: Automatic retry on failure and progress tracking.
- 📱 **Broad Support**: Works with standard YouTube URLs, Shorts, and `youtu.be` links.

## 🛠️ Tech Stack

- **[Python](https://www.python.org/)**: Core programming language.
- **[Flask](https://flask.palletsprojects.com/)**: Web framework for the UI.
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)**: Robust YouTube downloader engine.
- **[FFmpeg](https://ffmpeg.org/)**: Multimedia framework for audio conversion.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.8** or higher
- **FFmpeg** (Required for audio conversion)

### Installing FFmpeg

<details>
<summary><strong>Ubuntu / Debian</strong></summary>

```bash
sudo apt update
sudo apt install ffmpeg
```
</details>

<details>
<summary><strong>macOS (Homebrew)</strong></summary>

```bash
brew install ffmpeg
```
</details>

<details>
<summary><strong>Windows (Chocolatey)</strong></summary>

```bash
choco install ffmpeg
```
</details>

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd youtube-mp3-downloader
   ```

2. **Create a Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Usage

### 🌐 Web Application (Recommended)

Start the local web server to use the graphical interface.

1. Run the Flask app:
   ```bash
   python app.py
   ```
2. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

### 💻 Command Line Interface (CLI)

You can use the tool directly from your terminal.

**Interactive Mode:**
```bash
python main.py
```

**Quick Download:**
```bash
python main.py https://www.youtube.com/watch?v=VIDEO_ID
```

**Advanced Options:**
```bash
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

### 📦 Python Library

You can also import the downloader into your own Python projects.

```python
from downloader import YouTubeMP3Downloader

# Initialize
downloader = YouTubeMP3Downloader(output_dir="./music", audio_quality="320")

# Download
result = downloader.download("https://www.youtube.com/watch?v=VIDEO_ID")
print(f"Downloaded to: {result}")
```

## ⚙️ Configuration

You can customize default behaviors by editing `config.py`:

```python
# Default download directory
DOWNLOADS_DIR = BASE_DIR / "downloads"

# Default audio settings
DEFAULT_AUDIO_FORMAT = "mp3"
DEFAULT_AUDIO_QUALITY = "192"  # kbps

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY = 2
```

## 📂 Project Structure

```
youtube-mp3-downloader/
├── app.py              # Flask Web Application
├── main.py             # CLI Entry Point
├── downloader.py       # Core Downloader Logic
├── config.py           # Configuration Settings
├── requirements.txt    # Dependencies
├── downloads/          # Default Output Directory
├── static/             # Web Assets (CSS, JS)
├── templates/          # HTML Templates
└── utils/              # Helper Modules
```

## ⚠️ Legal Notice

This tool is intended for **personal use only**. Please respect copyright laws and YouTube's Terms of Service. Do not use this tool to download copyrighted content without permission.

## 📄 License

This project is licensed under the MIT License.
