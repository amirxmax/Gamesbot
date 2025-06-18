# handlers/entertainment.py (نسخه نهایی و هماهنگ با فایل شما)
import json
import random
from telegram import Update
from telegram.ext import ContextTypes

def _load_data(file_path: str) -> list:
    """یک تابع کمکی برای خواندن داده از فایل JSON."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

async def send_joke(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """یک جوک تصادفی از لیست آبجکت‌ها می‌خواند و ارسال می‌کند."""
    jokes_list = _load_data('data/jokes.json')
    if jokes_list:
        random_joke_object = random.choice(jokes_list)
        # === این خط اصلاح شد تا کلید "joke" را بخواند ===
        joke_text = random_joke_object.get('joke', 'متن جوک در فایل پیدا نشد!')
        await update.message.reply_text(joke_text)
    else:
        await update.message.reply_text("متاسفانه جوکی در انبار موجود نیست! (فایل خالی یا خراب است)")

async def send_bio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """یک بیو تصادفی از لیست آبجکت‌ها می‌خواند و ارسال می‌کند."""
    bios_list = _load_data('data/bios.json')
    if bios_list:
        random_bio_object = random.choice(bios_list)
        # کلید 'bio' از قبل صحیح بود
        bio_text = random_bio_object.get('bio', 'متن بیو در فایل پیدا نشد!')
        await update.message.reply_text(bio_text)
    else:
        await update.message.reply_text("متاسفانه بیوگرافی در انبار موجود نیست! (فایل خالی یا خراب است)")