# 🎮 PUBG UC Store — Player Lookup

موقع بسيط لجلب اسم اللاعب في PUBG عن طريق الـ Player ID

## 🗂 هيكل المشروع

```
pubg-uc-store/
├── app.py              ← السيرفر (Flask)
├── requirements.txt    ← مكتبات Python
├── render.yaml         ← إعدادات Render
├── .gitignore
└── static/
    └── index.html      ← الواجهة
```

## 🚀 خطوات النشر على Render

### 1. رفع المشروع على GitHub
- أنشئ مستودع جديد على github.com
- ارفع كل الملفات

### 2. إنشاء Web Service على Render
- اذهب إلى render.com
- اضغط **New → Web Service**
- اربطه بمستودع GitHub
- اختر **Python** كـ Runtime

### 3. إعدادات Render
| الحقل | القيمة |
|-------|--------|
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app --bind 0.0.0.0:$PORT` |

### 4. متغيرات البيئة (Environment Variables)
في **Environment → Add Environment Variable**:

| Key | Value |
|-----|-------|
| `PUBG_API_KEY` | مفتاحك من developer.pubg.com |

## ⚙️ تشغيل محلي

```bash
pip install -r requirements.txt
export PUBG_API_KEY="your_key_here"
python app.py
```
ثم افتح: http://localhost:5000
