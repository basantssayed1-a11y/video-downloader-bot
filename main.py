# main.py - بوت Telegram الرئيسي
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging
from video_downloader import VideoDownloader
from caption_extractor import CaptionExtractor
import os
from dotenv import load_dotenv

load_dotenv()

# إعدادات السجل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class VideoDownloaderBot:
    def __init__(self, token: str):
        self.app = Application.builder().token(token).build()
        self.downloader = VideoDownloader()
        self.caption_extractor = CaptionExtractor()
        
        # أضف المعالجات
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_url))
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """بدء البوت"""
        await update.message.reply_text(
            "🎬 مرحباً بك في بوت تحميل الفيديوهات!\n\n"
            "🔗 أرسل لي رابط الفيديو من أي موقع:\n"
            "✅ YouTube\n"
            "✅ TikTok\n"
            "✅ Instagram\n"
            "✅ Twitter\n"
            "✅ Facebook\n\n"
            "💡 اكتب /help للمزيد من المعلومات"
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """أظهر المساعدة"""
        help_text = (
            "📚 **قائمة الأوامر:**\n\n"
            "/start - ابدأ هنا\n"
            "/help - اعرض المساعدة\n\n"
            "🎯 **الاستخدام:**\n"
            "1. أرسل رابط الفيديو\n"
            "2. اختر الجودة (1080p, 720p, 480p)\n"
            "3. اختر ما إذا كنت تريد الكابشن\n"
            "4. سيتم تحميل الفيديو وإرساله لك\n\n"
            "⚙️ **الخيارات:**\n"
            "- تحميل الفيديو فقط\n"
            "- تحميل مع الكابشن (SRT/VTT)\n"
            "- تحميل الصوت فقط (MP3)\n"
            "- ترجمة الكابشن تلقائياً"
        )
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def handle_url(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالجة الروابط المرسلة"""
        url = update.message.text
        
        # التحقق من أن النص عبارة عن رابط
        if not self._is_valid_url(url):
            await update.message.reply_text("❌ الرجاء إرسال رابط صحيح")
            return
        
        # اكتشف نوع الموقع
        platform = self._detect_platform(url)
        
        if not platform:
            await update.message.reply_text("❌ الموقع غير مدعوم حالياً")
            return
        
        # أرسل رسالة جاري التحميل
        message = await update.message.reply_text("⏳ جاري التحميل... يرجى الانتظار")
        
        try:
            # حمّل الفيديو
            video_info = await self.downloader.download(url, platform)
            
            # اسحب الكابشن
            captions = await self.caption_extractor.extract(url, platform)
            
            # أرسل الفيديو
            with open(video_info['path'], 'rb') as video_file:
                await update.message.reply_video(
                    video=video_file,
                    caption=f"📹 **{video_info['title']}**\n\n✅ تم التحميل بنجاح!"
                )
            
            # أرسل الكابشن إذا توفر
            if captions and os.path.exists(captions['path']):
                with open(captions['path'], 'rb') as caption_file:
                    await update.message.reply_document(
                        document=caption_file,
                        caption="📝 الكابشن (SRT)"
                    )
            
            await message.delete()
            
        except Exception as e:
            await message.edit_text(f"❌ خطأ: {str(e)}")
            logger.error(f"Error: {str(e)}")
    
    def _is_valid_url(self, text: str) -> bool:
        """تحقق من أن النص عبارة عن رابط"""
        return text.startswith(('http://', 'https://', 'www.'))
    
    def _detect_platform(self, url: str) -> str:
        """اكتشف منصة الفيديو"""
        platforms = {
            'youtube': ['youtube.com', 'youtu.be'],
            'tiktok': ['tiktok.com', 'vm.tiktok.com'],
            'instagram': ['instagram.com', 'instagr.am'],
            'twitter': ['twitter.com', 'x.com'],
            'facebook': ['facebook.com', 'fb.watch']
        }
        
        for platform, domains in platforms.items():
            for domain in domains:
                if domain in url:
                    return platform
        return None
    
    def run(self):
        """شغّل البوت"""
        self.app.run_polling()

# تشغيل البوت
if __name__ == '__main__':
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    if not TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN not found in .env file")
    bot = VideoDownloaderBot(TOKEN)
    print("🚀 بوت Telegram شغال...")
    bot.run()
