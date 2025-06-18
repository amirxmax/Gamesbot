# handlers/riddle_handler.py (نسخه جدید با دو نقطه ورود)
import json
import random
from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler, # <-- این را به لیست import اضافه می‌کنیم
)

AWAITING_ANSWER = 1

def _load_riddles() -> list:
    """چیستان‌ها را از فایل JSON می‌خواند."""
    try:
        with open('data/puzzles.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

async def start_riddle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """بازی چیستان را از هر دو طریق (متن یا دکمه) شروع می‌کند."""
    
    # اگر بازی با دکمه شیشه‌ای شروع شده بود، ابتدا به آن پاسخ می‌دهیم
    if update.callback_query:
        await update.callback_query.answer()

    riddles = _load_riddles()
    if not riddles:
        reply_to = update.message or update.callback_query.message
        await reply_to.reply_text("متاسفانه چیستانی برای پرسیدن ندارم!")
        return ConversationHandler.END

    puzzle = random.choice(riddles)
    context.user_data['riddle_answer'] = puzzle['answer']
    
    message_text = (
        f"❓ چیستان:\n\n_{puzzle['riddle']}_\n\n"
        "برای پاسخ دادن، همین پیام را **ریپلای** کرده و جواب خود را بنویسید.\n"
        "برای لغو بازی، /cancel را ارسال کنید."
    )

    # بر اساس نوع ورودی، پیام را ارسال یا ویرایش می‌کنیم
    if update.callback_query:
        await update.callback_query.edit_message_text(text=message_text, parse_mode='Markdown')
    else: # اگر ورودی از نوع متن بود
        await update.message.reply_text(text=message_text, parse_mode='Markdown')
    
    return AWAITING_ANSWER

async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """پاسخ ریپلای شده کاربر را بررسی می‌کند."""
    correct_answer = context.user_data.get('riddle_answer')
    user_answer = update.message.text

    if user_answer.strip().lower() == correct_answer.lower():
        await update.message.reply_text("🎉 آفرین! پاسخ شما کاملاً درست بود.")
    else:
        await update.message.reply_text(f"❌ اشتباه بود! جواب صحیح: **{correct_answer}**", parse_mode='Markdown')
    
    context.user_data.pop('riddle_answer', None)
    await update.message.reply_text("برای یک چیستان دیگر، کلمه «چیستان» را بفرست یا از منوی /games استفاده کن.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """بازی را در هر مرحله‌ای لغو می‌کند."""
    if 'riddle_answer' in context.user_data:
        context.user_data.pop('riddle_answer', None)
    await update.message.reply_text("بازی چیستان لغو شد.")
    return ConversationHandler.END

# === این بخش مهم اصلاح شده است ===
riddle_handler = ConversationHandler(
    # ما به این لیست، یک ورودی دوم از نوع دکمه شیشه‌ای اضافه می‌کنیم
    entry_points=[
        MessageHandler(filters.Regex('^چیستان$'), start_riddle),          # ورودی از طریق متن
        CallbackQueryHandler(start_riddle, pattern='^start_riddle$')  # ورودی از طریق دکمه
    ],
    states={
        AWAITING_ANSWER: [MessageHandler(filters.REPLY & filters.TEXT & ~filters.COMMAND, check_answer)]
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)