# 🎬 Video Downloader Bot

بوت متكامل لتحميل الفيديوهات مع الكابشن من عدة مواقع

## ✨ المميزات

- ✅ تحميل الفيديوهات بجودات مختلفة
- ✅ استخراج الكابشن تلقائياً
- ✅ دعم أفضل المواقع:
  - YouTube
  - TikTok
  - Instagram
  - Twitter/X
  - Facebook
- ✅ تحميل الصوت فقط (MP3)
- ✅ ترجمة الكابشن التلقائية
- ✅ بوت Telegram و Discord معاً

## 📋 المتطلبات

- Python 3.8+
- FFmpeg مثبت على النظام
- توكن Telegram Bot
- توكن Discord Bot

## 🚀 التثبيت والتشغيل

### 1️⃣ استنسخ المشروع
```bash
git clone https://github.com/basantssayed1-a11y/video-downloader-bot.git
cd video-downloader-bot
```

### 2️⃣ ثبت المتطلبات
```bash
pip install -r requirements.txt
```

### 3️⃣ ثبت FFmpeg

**على Windows:**
```bash
choco install ffmpeg
```

**على macOS:**
```bash
brew install ffmpeg
```

**على Linux:**
```bash
sudo apt-get install ffmpeg
```

### 4️⃣ أضف التوكنات

انسخ مملف `.env.example` إلى `.env`:
```bash
cp .env.example .env
```

ثم أضف توكنات البوتات في ملف `.env`

### 5️⃣ شغّل البوت

**بوت Telegram:**
```bash
python main.py
```

**بوت Discord:**
```bash
python discord_bot.py
```

## 📝 الاستخدام

### Telegram

1. ابدأ البوت بـ `/start`
2. أرسل رابط الفيديو مباشرة
3. البو�� سيحمل الفيديو مع الكابشن تلقائياً

**الأوامر المتاحة:**
- `/start` - ابدأ البوت
- `/help` - اعرض المساعدة

### Discord

**الأوامر:**
- `!download <URL>` - حمل الفيديو
- `!audio <URL>` - حمل الصوت فقط

**مثال:**
```
!download https://www.youtube.com/watch?v=dQw4w9WgXcQ
!audio https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

## 📂 هيكل المشروع

```
video-downloader-bot/
├── main.py                 # بوت Telegram الرئيسي
├── discord_bot.py          # بوت Discord
├── video_downloader.py     # فئة تحميل الفيديوهات
├── caption_extractor.py    # فئة استخراج الكابشن
├── requirements.txt        # المتطلبات
├── .env.example           # مثال ملف البيانات
├── README.md              # هذا الملف
└── .gitignore            # ملفات Git المتجاهلة
```

## 🔧 التخصيص

### تغيير جودة التحميل

عدّل في ملف `video_downloader.py`:
```python
'format': 'best[ext=mp4]',  # أفضل جودة
'format': 'worst[ext=mp4]', # أقل جودة
'format': '22',             # 720p
'format': '18',             # 360p
```

### إضافة لغات كابشن

عدّل في ملف `caption_extractor.py`:
```python
'subtitleslangs': ['ar', 'en', 'fr', 'es'],  # أضف اللغات المطلوبة
```

## 🐛 معالجة الأخطاء

إذا واجهت أي مشاكل:

1. **خطأ في تحميل الفيديو:**
   - تأكد من أن الرابط صحيح
   - تأكد من أن FFmpeg مثبت
   - تحقق من اتصال الإنترنت

2. **خطأ في الكابشن:**
   - قد يكون الفيديو لا يحتوي على كابشن
   - جرب فيديو آخر

3. **خطأ في التوكن:**
   - تأكد من أن التوكن صحيح في ملف `.env`
   - أعد تشغيل البوت بعد تعديل `.env`

## 📜 الترخيص

MIT License - اطلع على ملف `LICENSE` للتفاصيل

## 👨‍💻 الكاتب

تم إنشاؤه بواسطة [basantssayed1-a11y](https://github.com/basantssayed1-a11y)

## 🤝 المساهمة

نرحب بالمساهمات! يرجى إنشاء pull request أو فتح issue لأي مشاكل أو اقتراحات.

## ⭐ دعم المشروع

إذا أعجبك المشروع، لا تنسَ إضافة ⭐ Star
