#!/usr/bin/env python3
"""
YouTube MP3 Downloader - Flask Web Application
"""

import os
import threading
from flask import Flask, render_template, request, jsonify, send_file, after_this_request
from downloader import YouTubeMP3Downloader
from utils.helpers import get_video_id_from_url
from utils.logger import logger
import config

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize downloader
downloader = YouTubeMP3Downloader()

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/info', methods=['POST'])
def get_info():
    """Get video information"""
    data = request.get_json()
    url = data.get('url', '')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    # Validate URL
    video_id = get_video_id_from_url(url)
    if not video_id:
        return jsonify({'error': 'Invalid YouTube URL'}), 400
    
    # Get video info
    info = downloader.get_video_info(url)
    if not info:
        return jsonify({'error': 'Failed to get video information'}), 500
    
    return jsonify({
        'success': True,
        'info': info
    })

@app.route('/api/download', methods=['POST'])
def download():
    """Download video as MP3"""
    data = request.get_json()
    url = data.get('url', '')
    quality = data.get('quality', config.DEFAULT_AUDIO_QUALITY)
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    # Validate URL
    video_id = get_video_id_from_url(url)
    if not video_id:
        return jsonify({'error': 'Invalid YouTube URL'}), 400
    
    # Create a new downloader with specified quality
    dl = YouTubeMP3Downloader(audio_quality=quality)
    
    # Download
    result = dl.download(url)
    
    if result and os.path.exists(result):
        return jsonify({
            'success': True,
            'filename': os.path.basename(result),
            'filepath': result
        })
    else:
        return jsonify({'error': 'Download failed'}), 500

@app.route('/api/download-video', methods=['POST'])
def download_video():
    """Download video without conversion"""
    data = request.get_json()
    url = data.get('url', '')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    # Validate URL
    video_id = get_video_id_from_url(url)
    if not video_id:
        return jsonify({'error': 'Invalid YouTube URL'}), 400
    
    # Download video
    result = downloader.download_video(url)
    
    if result and os.path.exists(result):
        return jsonify({
            'success': True,
            'filename': os.path.basename(result),
            'filepath': result
        })
    else:
        return jsonify({'error': 'Download failed'}), 500

@app.route('/api/get-file/<path:filename>')
def get_file(filename):
    """Serve the downloaded file and delete after sending"""
    filepath = os.path.join(config.DOWNLOADS_DIR, filename)
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    # Delete file after sending
    @after_this_request
    def remove_file(response):
        def delete_file():
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
                    logger.info(f"Deleted file: {filepath}")
            except Exception as e:
                logger.error(f"Error deleting file: {e}")
        
        # Delete file in a separate thread to not block response
        threading.Thread(target=delete_file).start()
        return response
    
    return send_file(
        filepath,
        as_attachment=True,
        download_name=filename
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
