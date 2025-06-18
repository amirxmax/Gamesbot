# handlers/start.py (نسخه نهایی و اصلاح شده)
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from database import add_user_if_not_exists

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """یک پیام خوشامدگویی و راهنمای ساده ارسال می‌کند."""
    user = update.effective_user
    add_user_if_not_exists(user.id, user.first_name, user.username)

    start_message = (
        f"سلام {user.first_name}!\nمن ربات سرگرمی و چالش جو هستم.\n\n"
        "🔹 برای دریافت جوک، کلمه `جوک` را ارسال کنید.\n"
        "🔹 برای دریافت بیو، کلمه `بیو` را ارسال کنید.\n\n"
        "⚡️ برای شروع بازی در هر چت یا گروه، دستور /games را ارسال کنید."
    )
    await update.message.reply_text(start_message, parse_mode='Markdown')


async def games_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """منوی انتخاب بازی را به صورت دکمه‌های شیشه‌ای نمایش می‌دهد."""
    keyboard = [
        [InlineKeyboardButton("🎯 دوز (Tic Tac Toe)", callback_data="lobby_tictactoe")],
        [InlineKeyboardButton("❓ چیستان", callback_data="start_riddle")],
        # دکمه‌های بازی‌های دیگر در مراحل بعد اضافه خواهند شد
        # [InlineKeyboardButton("🟥 سوالات دو گزینه‌ای", callback_data="setup_quiz")],
        # [InlineKeyboardButton("🎭 حقیقت یا جرأت", callback_data="start_truth_or_dare")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎮 یک بازی برای شروع انتخاب کنید:", reply_markup=reply_markup)