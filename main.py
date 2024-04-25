from token import TOKEN
import logging
import sqlite3
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    with sqlite3.connect('finance.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user.id,))
        result = cursor.fetchone()
        if not result:
            cursor.execute("INSERT INTO users (user_id, username) VALUES (?, ?)", (user.id, user.username))
            conn.commit()
    update.message.reply_text('Привет, я бот для контроля финансов')

def add_expense(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    expense = update.message.text.split(' ')[1:]
    amount = float(expense[0])
    category = ' '.join(expense[1:])
    with sqlite3.connect('finance.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (user_id, amount, category) VALUES (?, ?, ?)", (user_id, amount, category))
        conn.commit()
    update.message.reply_text(f'Расход добавлены: {amount} в категорию {category}')

def add_income(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    income = update.message.text.split(' ')[1:]
    amount = float(income[0])
    category = ' '.join(income[1:])
    with sqlite3.connect('finance.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO income (user_id, amount, category) VALUES (?, ?, ?)", (user_id, amount, category))
        conn.commit()
    update.message.reply_text(f'Доход добавлен: {amount} в категорию {category}')

def view_balance(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    with sqlite3.connect('finance.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ?", (user_id,))
        expenses = cursor.fetchone()[0] or 0
        cursor.execute("SELECT SUM(amount) FROM income WHERE user_id = ?", (user_id,))
        income = cursor.fetchone()[0] or 0
        balance = income - expenses
    update.message.reply_text(f'Баланс: {balance}')

def login(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    with sqlite3.connect('finance.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user.id,))
        result = cursor.fetchone()
        if result:
            update.message.reply_text('Вы уже в аккаунте')
        else:
            cursor.execute("INSERT INTO users (user_id, username) VALUES (?, ?)", (user.id, user.username))
            conn.commit()
            update.message.reply_text('Вы успешно вошли')

def register(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    with sqlite3.connect('finance.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user.id,))
        result = cursor.fetchone()
        if result:
            update.message.reply_text('Вы уже зарегистрированы')
        else:
            cursor.execute("INSERT INTO users (user_id, username) VALUES (?, ?)", (user.id, user.username))
            conn.commit()
            update.message.reply_text('Вы успешно зарегистрировались')

def main() -> None:
    with sqlite3.connect('finance.db') as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY, user_id INTEGER, amount REAL, category TEXT, FOREIGN KEY (user_id) REFERENCES users (user_id))")
        cursor.execute("CREATE TABLE IF NOT EXISTS income (id INTEGER PRIMARY KEY, user_id INTEGER, amount REAL, category TEXT, FOREIGN KEY (user_id) REFERENCES users (user_id))")
        conn.commit()

    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("add_expense", add_expense, pass_args=True))
    dispatcher.add_handler(CommandHandler("add_income", add_income, pass_args=True))
    dispatcher.add_handler(CommandHandler("view_balance", view_balance))
    dispatcher.add_handler(CommandHandler("login", login))
    dispatcher.add_handler(CommandHandler("register", register))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
