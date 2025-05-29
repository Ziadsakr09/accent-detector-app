import os
import tempfile
from yt_dlp import YoutubeDL

def download_audio(video_url):
    """Download audio from video URL using yt-dlp"""
    try:
        # Create temp directory
        temp_dir = tempfile.mkdtemp()
        audio_path = os.path.join(temp_dir, "audio.%(ext)s")
        
        ydl_opts = {
            'format': 'bestaudio/best[duration<600]',  # Limit to 10 minutes
            'outtmpl': audio_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',  # Lower quality for faster processing
            }],
            'quiet': True,
            'no_warnings': True,
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        # Find the downloaded file
        downloaded_file = None
        for file in os.listdir(temp_dir):
            if file.startswith("audio") and file.endswith(('.mp3', '.m4a', '.wav')):
                downloaded_file = os.path.join(temp_dir, file)
                break
        
        if not downloaded_file or not os.path.exists(downloaded_file):
            raise Exception("Audio file not found after download")
        
        # Check file size (limit to ~10MB)
        file_size = os.path.getsize(downloaded_file) / (1024 * 1024)
        if file_size > 10:
            raise Exception(f"Audio file too large ({file_size:.1f}MB). Please use shorter videos.")
        
        return downloaded_file
        
    except Exception as e:
        raise Exception(f"Download failed: {str(e)}")
