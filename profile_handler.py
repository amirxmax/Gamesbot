# handlers/profile_handler.py
import datetime
from telegram import Update
from telegram.ext import ContextTypes
from database import get_user_balance, update_user_balance

DAILY_GIFT_AMOUNT = 50

async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """پروفایل کاربر شامل نام و موجودی را نمایش می‌دهد."""
    user = update.effective_user
    balance = get_user_balance(user.id)

    profile_text = (
        f"👤 پروفایل شما\n\n"
        f"🏷 نام: {user.first_name}\n"
        f"💰 موجودی: {balance} امتیاز"
    )
    await update.message.reply_text(profile_text)

async def daily_gift(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """جایزه روزانه را به کاربر می‌دهد."""
    user_id = update.effective_user.id
    now = datetime.datetime.now()

    last_claim = context.user_data.get('last_daily_claim')

    if last_claim and (now - last_claim).total_seconds() < 86400: # 24 hours
        await update.message.reply_text("شما قبلاً جایزه روزانه خود را دریافت کرده‌اید. لطفاً ۲۴ ساعت دیگر دوباره تلاش کنید.")
        return

    # اضافه کردن جایزه به موجودی کاربر
    update_user_balance(user_id, DAILY_GIFT_AMOUNT)
    # ثبت زمان دریافت جایزه
    context.user_data['last_daily_claim'] = now

    await update.message.reply_text(f"🎁 تبریک! {DAILY_GIFT_AMOUNT} امتیاز به عنوان جایزه روزانه به حساب شما اضافه شد.")