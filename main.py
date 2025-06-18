# main.py (نسخه جدید با سیستم امتیاز)
import logging
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, 
    PicklePersistence, CallbackQueryHandler,
)
from config import BOT_TOKEN
from database import init_db
from handlers.start import start, games_menu
from handlers.entertainment import send_joke, send_bio
from handlers.riddle_handler import riddle_handler
from handlers.tictactoe_handler import create_tictactoe_lobby, join_and_start_game, player_move
# وارد کردن توابع جدید پروفایل
from handlers.profile_handler import show_profile, daily_gift

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def main() -> None:
    init_db()
    persistence = PicklePersistence(filepath="bot_persistence.pickle")
    application = Application.builder().token(BOT_TOKEN).persistence(persistence).build()

    # --- ثبت کنترل‌کننده‌ها ---

    # ۱. کنترل‌کننده‌های اصلی
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("games", games_menu))
    application.add_handler(CommandHandler("profile", show_profile)) # جدید
    application.add_handler(CommandHandler("daily", daily_gift))   # جدید

    # ۲. کنترل‌کننده‌های کلمات کلیدی
    application.add_handler(MessageHandler(filters.Text(['جوک', 'jok']), send_joke))
    application.add_handler(MessageHandler(filters.Text(['بیو', 'bio']), send_bio))

    # ۳. کنترل‌کننده بازی چیستان
    application.add_handler(riddle_handler)

    # ۴. کنترل‌کننده‌های بازی دوز
    application.add_handler(CallbackQueryHandler(create_tictactoe_lobby, pattern='^lobby_tictactoe$'))
    application.add_handler(CallbackQueryHandler(join_and_start_game, pattern='^join_tictactoe_'))
    application.add_handler(CallbackQueryHandler(player_move, pattern=r'^ttt_move_'))

    logger.info("Bot is starting with Phase 4 (Economy) enabled...")
    application.run_polling()

if __name__ == "__main__":
    main()