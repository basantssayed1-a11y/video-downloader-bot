# discord_bot.py - بوت Discord
import discord
from discord.ext import commands
from video_downloader import VideoDownloader
from caption_extractor import CaptionExtractor
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

class DiscordVideoDownloaderBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.downloader = VideoDownloader()
        self.caption_extractor = CaptionExtractor()
    
    @commands.command(name='download')
    async def download_video(self, ctx, url: str):
        """تحميل الفيديو من رابط
        الاستخدام: !download <URL>
        """
        async with ctx.typing():
            try:
                # اكتشف المنصة
                platform = self._detect_platform(url)
                
                if not platform:
                    await ctx.send("❌ الموقع غير مدعوم")
                    return
                
                # حمّل الفيديو
                video_info = await self.downloader.download(url, platform)
                
                # اسحب الكابشن
                captions = await self.caption_extractor.extract(url, platform)
                
                # أرسل الفيديو
                await ctx.send(
                    f"📹 **{video_info['title']}**",
                    file=discord.File(video_info['path'])
                )
                
                # أرسل الكابشن
                if captions and os.path.exists(captions['path']):
                    await ctx.send(
                        "📝 الكابشن:",
                        file=discord.File(captions['path'])
                    )
                
            except Exception as e:
                await ctx.send(f"❌ خطأ: {str(e)}")
    
    @commands.command(name='audio')
    async def download_audio(self, ctx, url: str):
        """تحميل الصوت فقط (MP3)"""
        async with ctx.typing():
            try:
                audio_info = await self.downloader.download_audio(url)
                await ctx.send(
                    f"🎵 {audio_info['title']}",
                    file=discord.File(audio_info['path'])
                )
            except Exception as e:
                await ctx.send(f"❌ خطأ: {str(e)}")
    
    def _detect_platform(self, url: str) -> str:
        """اكتشف منصة الفيديو"""
        platforms = {
            'youtube': ['youtube.com', 'youtu.be'],
            'tiktok': ['tiktok.com'],
            'instagram': ['instagram.com'],
            'twitter': ['twitter.com', 'x.com'],
            'facebook': ['facebook.com']
        }
        
        for platform, domains in platforms.items():
            for domain in domains:
                if domain in url:
                    return platform
        return None

async def setup(bot):
    await bot.add_cog(DiscordVideoDownloaderBot(bot))

# تشغيل بوت Discord
if __name__ == '__main__':
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    @bot.event
    async def on_ready():
        print(f'✅ {bot.user} شغال!')
    
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        raise ValueError("DISCORD_BOT_TOKEN not found in .env file")
    
    bot.run(token)
