# caption_extractor.py - استخراج الكابشن
import yt_dlp
import os
from typing import Optional, Dict
import asyncio

class CaptionExtractor:
    def __init__(self):
        self.output_dir = "downloads/captions"
        os.makedirs(self.output_dir, exist_ok=True)
    
    async def extract(self, url: str, platform: str) -> Optional[Dict]:
        """استخرج الكابشن من الفيديو"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._extract_sync, url)
    
    def _extract_sync(self, url: str) -> Optional[Dict]:
        """استخ��اج متزامن للكابشن"""
        ydl_opts = {
            'writesubtitles': True,
            'subtitleslangs': ['ar', 'en', 'auto'],
            'subtitlesformat': 'srt',
            'outtmpl': os.path.join(self.output_dir, '%(title)s'),
            'skip_unavailable_fragments': True,
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                # ابحث عن ملف الكابشن
                title = info.get('title', 'caption')
                caption_file = os.path.join(self.output_dir, f"{title}.ar.srt")
                
                if os.path.exists(caption_file):
                    return {
                        'path': caption_file,
                        'language': 'ar',
                        'format': 'srt'
                    }
                
                # إذا لم توجد النسخة العربية، حاول الإنجليزية
                caption_file = os.path.join(self.output_dir, f"{title}.en.srt")
                if os.path.exists(caption_file):
                    return {
                        'path': caption_file,
                        'language': 'en',
                        'format': 'srt'
                    }
                
                return None
                
        except Exception as e:
            print(f"خطأ في استخراج الكابشن: {str(e)}")
            return None
    
    def translate_caption(self, caption_path: str, target_lang: str) -> str:
        """ترجم الكابشن باستخدام Google Translate"""
        try:
            from google_trans_new import google_translator
            
            translator = google_translator()
            translated_path = caption_path.replace('.srt', f'_{target_lang}.srt')
            
            with open(caption_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            translated_lines = []
            for line in lines:
                if line.strip() and not line[0].isdigit() and '-->' not in line:
                    translated = translator.translate(line.strip(), lang_tgt=target_lang)
                    translated_lines.append(translated + '\n')
                else:
                    translated_lines.append(line)
            
            with open(translated_path, 'w', encoding='utf-8') as f:
                f.writelines(translated_lines)
            
            return translated_path
        except Exception as e:
            print(f"خطأ في الترجمة: {str(e)}")
            return None
