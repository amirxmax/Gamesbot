# handlers/tictactoe_handler.py
import random
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

# حافظه موقت برای نگهداری بازی‌های فعال
ACTIVE_GAMES = {}

PLAYER_X_SYMBOL = '❌'
PLAYER_O_SYMBOL = '⭕'

def generate_board_keyboard(board):
    """صفحه بازی را با دکمه‌ها می‌سازد."""
    keyboard = []
    row = []
    for i, cell in enumerate(board):
        text = cell if cell != ' ' else '➖'
        row.append(InlineKeyboardButton(text, callback_data=f"ttt_move_{i}"))
        if (i + 1) % 3 == 0:
            keyboard.append(row); row = []
    return InlineKeyboardMarkup(keyboard)

def check_winner(board):
    """برنده را بررسی می‌کند."""
    win_conditions = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    for c in win_conditions:
        if board[c[0]]==board[c[1]]==board[c[2]] and board[c[0]]!=' ': return board[c[0]]
    if ' ' not in board: return 'draw'
    return None

async def create_tictactoe_lobby(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پیام دعوت به بازی (لابی) را ایجاد می‌کند."""
    query = update.callback_query
    await query.answer()
    user = query.from_user

    keyboard = [[InlineKeyboardButton("🤝 پیوستن به بازی", callback_data=f"join_tictactoe_{user.id}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        f"یک چالش دوز توسط {user.first_name} ساخته شد!\nمنتظر حریف...",
        reply_markup=reply_markup
    )

async def join_and_start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پس از پیوستن حریف، بازی را شروع می‌کند."""
    query = update.callback_query
    chat_id = update.effective_chat.id

    if chat_id in ACTIVE_GAMES:
        await query.answer("یک بازی دیگر در این چت در حال اجراست!", show_alert=True)
        return

    try:
        initiator_id = int(query.data.split('_')[-1])
        joiner = query.from_user
        joiner_id = joiner.id

        if initiator_id == joiner_id:
            await query.answer("شما نمی‌توانید به بازی خودتان بپیوندید!", show_alert=True)
            return

        await query.answer()

        initiator = await context.bot.get_chat(initiator_id)

        ACTIVE_GAMES[chat_id] = {
            'game_type': 'tictactoe',
            'board': [' '] * 9,
            'player_x': initiator_id, 'player_o': joiner_id,
            'current_turn': initiator_id,
            'player_x_name': initiator.first_name, 'player_o_name': joiner.first_name
        }

        game_state = ACTIVE_GAMES[chat_id]
        message_text = f"بازی شروع شد!\n\n{PLAYER_X_SYMBOL} : {game_state['player_x_name']}\n{PLAYER_O_SYMBOL} : {game_state['player_o_name']}\n\nنوبت بازیکن {PLAYER_X_SYMBOL} ({game_state['player_x_name']})"
        keyboard = generate_board_keyboard(game_state['board'])
        await query.edit_message_text(text=message_text, reply_markup=keyboard)

    except Exception as e:
        await query.edit_message_text("خطایی در شروع بازی رخ داد. لطفاً دوباره با دستور /game تلاش کنید.")

async def player_move(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """حرکت بازیکنان را پردازش می‌کند."""
    query = update.callback_query
    user_id = query.from_user.id
    chat_id = update.effective_chat.id
    game_state = ACTIVE_GAMES.get(chat_id)

    if not game_state or game_state.get('game_type') != 'tictactoe':
        await query.answer("این بازی تمام شده یا فعال نیست.", show_alert=True)
        return

    if user_id != game_state['current_turn']:
        await query.answer("نوبت شما نیست!", show_alert=True)
        return

    await query.answer()
    board = game_state['board']; move = int(query.data.split('_')[-1])

    if board[move] != ' ':
        await query.answer("این خانه قبلا پر شده!", show_alert=True)
        return

    symbol = PLAYER_X_SYMBOL if user_id == game_state['player_x'] else PLAYER_O_SYMBOL
    board[move] = symbol
    winner_symbol = check_winner(board)

    player_x_name = game_state.get('player_x_name')
    player_o_name = game_state.get('player_o_name')

    if winner_symbol:
        if winner_symbol == 'draw': message = "بازی مساوی شد! 🤝"
        else:
            winner_name = player_x_name if winner_symbol == PLAYER_X_SYMBOL else player_o_name
            message = f"بازی تمام شد! برنده: {winner_name} 🏆"
        keyboard = generate_board_keyboard(board)
        await query.edit_message_text(text=message, reply_markup=keyboard)
        ACTIVE_GAMES.pop(chat_id, None) # پاک کردن بازی از حافظه
        return

    next_player_id = game_state['player_o'] if user_id == game_state['player_x'] else game_state['player_x']
    game_state['current_turn'] = next_player_id
    next_player_name = player_o_name if next_player_id == game_state['player_o'] else player_x_name
    next_player_symbol = PLAYER_O_SYMBOL if next_player_id == game_state['player_o'] else PLAYER_X_SYMBOL

    message_text = f"{PLAYER_X_SYMBOL} : {player_x_name}\n{PLAYER_O_SYMBOL} : {player_o_name}\n\nنوبت بازیکن {next_player_symbol} ({next_player_name})"
    keyboard = generate_board_keyboard(board)
    await query.edit_message_text(text=message_text, reply_markup=keyboard)