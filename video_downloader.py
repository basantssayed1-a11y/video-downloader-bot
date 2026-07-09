# video_downloader.py - تحميل الفيديوهات
import yt_dlp
import os
from typing import Dict, Optional
import asyncio

class VideoDownloader:
    def __init__(self):
        self.output_dir = "downloads"
        os.makedirs(self.output_dir, exist_ok=True)
    
    async def download(self, url: str, platform: str) -> Dict:
        """حمّل الفيديو من المنصة المحددة"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._download_sync, url, platform)
    
    def _download_sync(self, url: str, platform: str) -> Dict:
        """تحميل متزامن للفيديو"""
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            'writesubtitles': True,
            'subtitleslangs': ['ar', 'en'],
            'skip_unavailable_fragments': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return {
                    'title': info.get('title', 'Video'),
                    'path': ydl.prepare_filename(info),
                    'duration': info.get('duration'),
                    'platform': platform,
                    'thumbnail': info.get('thumbnail')
                }
        except Exception as e:
            raise Exception(f"خطأ في التحميل: {str(e)}")

    async def download_audio(self, url: str) -> Dict:
        """حمّل الصوت فقط (MP3)"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._download_audio_sync, url)
    
    def _download_audio_sync(self, url: str) -> Dict:
        """تحميل الصوت متزامن"""
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s'),
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return {
                    'title': info.get('title'),
                    'path': os.path.join(self.output_dir, f"{info.get('title')}.mp3")
                }
        except Exception as e:
            raise Exception(f"خطأ في تحميل الصوت: {str(e)}")
