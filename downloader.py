"""YouTube MP3 Downloader - Download audio from YouTube videos as MP3"""
import os
import time
import yt_dlp
import config
from utils.logger import logger
from utils.helpers import get_video_id_from_url, sanitize_filename

class YouTubeMP3Downloader:
    """Download MP3 audio from YouTube videos"""
    
    def __init__(self, output_dir=None, max_retries=None, retry_delay=None, 
                 audio_quality=None, audio_format=None):
        """Initialize the YouTube MP3 downloader
        
        Args:
            output_dir: Directory to save downloaded audio (defaults to config.DOWNLOADS_DIR)
            max_retries: Maximum number of download attempts (defaults to config.MAX_RETRIES)
            retry_delay: Delay between retry attempts in seconds (defaults to config.RETRY_DELAY)
            audio_quality: Audio quality in kbps (defaults to config.DEFAULT_AUDIO_QUALITY)
            audio_format: Audio format/extension (defaults to config.DEFAULT_AUDIO_FORMAT)
        """
        self.output_dir = output_dir or config.DOWNLOADS_DIR
        self.max_retries = max_retries or config.MAX_RETRIES
        self.retry_delay = retry_delay or config.RETRY_DELAY
        self.audio_quality = audio_quality or config.DEFAULT_AUDIO_QUALITY
        self.audio_format = audio_format or config.DEFAULT_AUDIO_FORMAT
        
        os.makedirs(self.output_dir, exist_ok=True)
    
    def get_video_info(self, url):
        """Get video information without downloading
        
        Args:
            url: YouTube video URL
            
        Returns:
            dict: Video information or None if failed
        """
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'id': info.get('id'),
                    'title': info.get('title'),
                    'duration': info.get('duration'),
                    'uploader': info.get('uploader'),
                    'thumbnail': info.get('thumbnail'),
                    'view_count': info.get('view_count'),
                }
        except Exception as e:
            logger.error(f"Failed to get video info: {str(e)}")
            return None
    
    def download(self, url, custom_filename=None):
        """Download audio from YouTube video as MP3
        
        Args:
            url: YouTube video URL
            custom_filename: Optional custom filename (without extension)
            
        Returns:
            str: Path to downloaded MP3 file or None if download failed
        """
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Downloading audio from {url} (Attempt {attempt+1}/{self.max_retries})")
                
                # Get video ID for filename
                video_id = get_video_id_from_url(url)
                
                # If we couldn't get the ID from the URL helper, try to get it via yt-dlp info
                if not video_id:
                    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                        info = ydl.extract_info(url, download=False)
                        video_id = info.get('id')

                logger.info(f"Video ID: {video_id}")
                
                # Determine filename
                if custom_filename:
                    filename = f"{sanitize_filename(custom_filename)}.{self.audio_format}"
                else:
                    # Get video title for filename
                    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                        info = ydl.extract_info(url, download=False)
                        title = sanitize_filename(info.get('title', video_id))
                        filename = f"{title}.{self.audio_format}"
                
                logger.info(f"Filename: {filename}")
                output_path = os.path.join(str(self.output_dir), filename)
                
                # If file already exists, return the path
                if os.path.exists(output_path):
                    logger.info(f"Audio already downloaded: {output_path}")
                    return output_path

                logger.info(f"Output path: {output_path}")
                
                # Download audio
                logger.info(f"Downloading audio at {self.audio_quality}kbps quality")
                
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': self.audio_format,
                        'preferredquality': self.audio_quality,
                    }],
                    'outtmpl': output_path.replace(f'.{self.audio_format}', ''),
                    'quiet': False,
                    'no_warnings': False,
                    'progress_hooks': [self._progress_hook],
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                # yt-dlp adds the extension, so the final path might be different
                final_path = output_path
                if not os.path.exists(final_path):
                    # Try without double extension
                    alt_path = output_path.replace(f'.{self.audio_format}', '') + f'.{self.audio_format}'
                    if os.path.exists(alt_path):
                        final_path = alt_path
                
                logger.info(f"Download complete: {final_path}")
                return final_path
                
            except Exception as e:
                logger.warning(f"Error downloading audio (attempt {attempt+1}): {str(e)}")
                if attempt < self.max_retries - 1:
                    logger.info(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"Failed to download after {self.max_retries} attempts")
                    return None
    
    def _progress_hook(self, d):
        """Progress hook for download status updates
        
        Args:
            d: Progress dictionary from yt-dlp
        """
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            logger.info(f"Progress: {percent} | Speed: {speed} | ETA: {eta}")
        elif d['status'] == 'finished':
            logger.info("Download finished, converting to MP3...")
    
    def download_multiple(self, urls):
        """Download multiple videos as MP3
        
        Args:
            urls: List of YouTube video URLs
            
        Returns:
            list: List of downloaded file paths (None for failed downloads)
        """
        results = []
        for i, url in enumerate(urls, 1):
            logger.info(f"Processing {i}/{len(urls)}: {url}")
            result = self.download(url)
            results.append(result)
        return results
