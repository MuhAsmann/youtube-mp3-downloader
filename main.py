#!/usr/bin/env python3
"""
YouTube MP3 Downloader - Command Line Interface

Usage:
    python main.py <youtube_url> [options]
    python main.py --help

Examples:
    python main.py https://www.youtube.com/watch?v=dQw4w9WgXcQ
    python main.py https://youtu.be/dQw4w9WgXcQ -o ./my_music
    python main.py https://www.youtube.com/watch?v=dQw4w9WgXcQ -q 320
"""

import argparse
import sys
from pathlib import Path

from downloader import YouTubeMP3Downloader
from utils.logger import logger
from utils.helpers import get_video_id_from_url
import config

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Download MP3 audio from YouTube videos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s https://www.youtube.com/watch?v=dQw4w9WgXcQ
    %(prog)s https://youtu.be/dQw4w9WgXcQ -o ./my_music
    %(prog)s https://www.youtube.com/watch?v=dQw4w9WgXcQ -q 320 -n "my_song"
        """
    )
    
    parser.add_argument(
        'url',
        type=str,
        nargs='?',
        help='YouTube video URL to download'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help=f'Output directory (default: {config.DOWNLOADS_DIR})'
    )
    
    parser.add_argument(
        '-q', '--quality',
        type=str,
        default=config.DEFAULT_AUDIO_QUALITY,
        choices=['128', '192', '256', '320'],
        help=f'Audio quality in kbps (default: {config.DEFAULT_AUDIO_QUALITY})'
    )
    
    parser.add_argument(
        '-n', '--name',
        type=str,
        default=None,
        help='Custom filename for the downloaded audio (without extension)'
    )
    
    parser.add_argument(
        '-f', '--format',
        type=str,
        default=config.DEFAULT_AUDIO_FORMAT,
        choices=['mp3', 'aac', 'm4a', 'opus', 'wav', 'flac'],
        help=f'Audio format (default: {config.DEFAULT_AUDIO_FORMAT})'
    )
    
    parser.add_argument(
        '-i', '--info',
        action='store_true',
        help='Only show video information, do not download'
    )
    
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )
    
    return parser.parse_args()

def interactive_mode():
    """Run the downloader in interactive mode"""
    print("\n" + "="*50)
    print("  🎵 YouTube MP3 Downloader - Interactive Mode 🎵")
    print("="*50 + "\n")
    
    downloader = YouTubeMP3Downloader()
    
    while True:
        try:
            url = input("Enter YouTube URL (or 'quit' to exit): ").strip()
            
            if url.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye! 👋")
                break
            
            if not url:
                print("Please enter a valid URL.\n")
                continue
            
            # Validate URL
            video_id = get_video_id_from_url(url)
            if not video_id:
                print("Invalid YouTube URL. Please try again.\n")
                continue
            
            # Get video info first
            print("\nFetching video information...")
            info = downloader.get_video_info(url)
            
            if info:
                print(f"\n📹 Title: {info['title']}")
                print(f"👤 Uploader: {info['uploader']}")
                print(f"⏱️  Duration: {info['duration']} seconds")
                print(f"👁️  Views: {info['view_count']:,}\n")
            
            # Ask for confirmation
            confirm = input("Download this video as MP3? (y/n): ").strip().lower()
            if confirm != 'y':
                print("Skipped.\n")
                continue
            
            # Download
            print("\n⬇️  Starting download...")
            result = downloader.download(url)
            
            if result:
                print(f"\n✅ Successfully downloaded: {result}\n")
            else:
                print("\n❌ Download failed.\n")
                
        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye! 👋")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")

def main():
    """Main entry point"""
    args = parse_args()
    
    # Interactive mode
    if args.interactive or not args.url:
        interactive_mode()
        return
    
    # Validate URL
    video_id = get_video_id_from_url(args.url)
    if not video_id:
        logger.error("Invalid YouTube URL")
        sys.exit(1)
    
    # Initialize downloader
    downloader = YouTubeMP3Downloader(
        output_dir=args.output,
        audio_quality=args.quality,
        audio_format=args.format
    )
    
    # Info only mode
    if args.info:
        info = downloader.get_video_info(args.url)
        if info:
            print("\n📹 Video Information:")
            print(f"   ID: {info['id']}")
            print(f"   Title: {info['title']}")
            print(f"   Uploader: {info['uploader']}")
            print(f"   Duration: {info['duration']} seconds")
            print(f"   Views: {info['view_count']:,}")
            print(f"   Thumbnail: {info['thumbnail']}")
            print()
        return
    
    # Download
    logger.info(f"Starting download: {args.url}")
    result = downloader.download(args.url, custom_filename=args.name)
    
    if result:
        logger.info(f"✅ Successfully downloaded: {result}")
    else:
        logger.error("❌ Download failed")
        sys.exit(1)

if __name__ == '__main__':
    main()
