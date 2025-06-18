# database.py (نسخه جدید با توابع مدیریت موجودی)
import sqlite3

def init_db():
    """دیتابیس و جداول را می‌سازد."""
    with sqlite3.connect('bot.db') as conn:
        cursor = conn.cursor()
        # جدول کاربران با ستون موجودی
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            user_id INTEGER UNIQUE NOT NULL,
            first_name TEXT,
            username TEXT,
            balance INTEGER DEFAULT 100
        )''')
        # جدول سوابق بازی
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_records (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            game_type TEXT,
            score INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )''')
        conn.commit()

def add_user_if_not_exists(user_id, first_name, username):
    """کاربر جدید را با موجودی اولیه به دیتابیس اضافه می‌کند."""
    with sqlite3.connect('bot.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO users (user_id, first_name, username) VALUES (?, ?, ?)",
                (user_id, first_name, username)
            )
            conn.commit()

def get_user_balance(user_id: int) -> int:
    """موجودی یک کاربر را برمی‌گرداند."""
    with sqlite3.connect('bot.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        return result[0] if result else 0

def update_user_balance(user_id: int, amount: int) -> bool:
    """موجودی کاربر را به مقدار مشخص شده (مثبت یا منفی) تغییر می‌دهد."""
    current_balance = get_user_balance(user_id)
    if current_balance + amount < 0:
        return False  # موجودی کافی نیست

    with sqlite3.connect('bot.db') as conn:
        cursor = conn.cursor()
        new_balance = current_balance + amount
        cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (new_balance, user_id))
        conn.commit()
    return True

def add_game_record(user_id, game_type, score):
    """یک رکورد بازی جدید ثبت می‌کند."""
    with sqlite3.connect('bot.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO game_records (user_id, game_type, score) VALUES (?, ?, ?)",
            (user_id, game_type, score)
        )
        conn.commit()