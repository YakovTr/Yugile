from config import TOKEN
import logging
import sqlite3
from telegram import Update
from telegram.ext import CommandHandler, Application, CallbackContext

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    with sqlite3.connect('finance.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user.id,))
        result = cursor.fetchone()
        if not result:
            cursor.execute("INSERT INTO users (user_id, username) VALUES (?, ?)", (user.id, user.username))
            conn.commit()
    await update.message.reply_text('Привет, я бот для контроля финансоn\n напишите @help')

async def add_expense(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    expense = update.message.text.split(' ')[1:]
    amount = float(expense[0])
    category = ' '.join(expense[1:])
    with sqlite3.connect('finance.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (user_id, amount, category) VALUES (?, ?, ?)", (user_id, amount, category))
        conn.commit()
    await update.message.reply_text(f'Расход добавлены: {amount} в категорию {category}')

async def add_income(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    income = update.message.text.split(' ')[1:]
    amount = float(income[0])
    category = ' '.join(income[1:])
    with sqlite3.connect('finance.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO income (user_id, amount, category) VALUES (?, ?, ?)", (user_id, amount, category))
        conn.commit()
    await update.message.reply_text(f'Доход добавлен: {amount} в категорию {category}')

async def view_balance(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    with sqlite3.connect('finance.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ?", (user_id,))
        expenses = cursor.fetchone()[0] or 0
        cursor.execute("SELECT SUM(amount) FROM income WHERE user_id = ?", (user_id,))
        income = cursor.fetchone()[0] or 0
        balance = income - expenses
    await update.message.reply_text(f'Баланс: {balance}')

async def help(update: Update, context: CallbackContext):
    help_text = 'Список команд:\n\n' \
                '/start - начать работу с ботом\n' \
                '/add_expense - добавить расход(чтобы добавить расход напишите в одном сообщении "@add_expense сумма категория)"\n' \
                '/add_income - добавить доход(чтобы добавить доход напишите в одном сообщении "@add_expense сумма категория)"\n' \
                '/view_balance - посмотреть баланс\n' \
                '/view_expenses - посмотреть расходы по категориям\n' \
                '/reset - очистить все доходы и расходы\n' \
                '/view_incomes - посмотреть доходы по категориям\n'
    await update.message.reply_text(help_text)

async def view_expenses(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    with sqlite3.connect('finance.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT category, SUM(amount) FROM expenses WHERE user_id = ? GROUP BY category", (user_id,))
        expenses = cursor.fetchall()
        if not expenses:
            await update.message.reply_text('Нет расходов')
            return
        expense_text = 'Расходы по категориям:\n\n'
        for category, amount in expenses:
            expense_text += f'{category}: {amount}\n'
        await update.message.reply_text(expense_text)

async def view_incomes(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    with sqlite3.connect('finance.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT category, SUM(amount) FROM income WHERE user_id = ? GROUP BY category", (user_id,))
        incomes = cursor.fetchall()
        if not incomes:
            await update.message.reply_text('Нет доходов')
            return
        income_text = 'Доходы по категориям:\n\n'
        for category, amount in incomes:
            income_text += f'{category}: {amount}\n'
        await update.message.reply_text(income_text)

async def reset_data(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    with sqlite3.connect('finance.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM income WHERE user_id = ?", (user_id,))
        conn.commit()
    await update.message.reply_text('Все данные обновлены')


def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("reset", reset_data))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("add_expense", add_expense))
    application.add_handler(CommandHandler("add_income", add_income))
    application.add_handler(CommandHandler("view_balance", view_balance))
    application.add_handler(CommandHandler("view_expenses", view_expenses))
    application.add_handler(CommandHandler("view_incomes", view_incomes))


    application.run_polling()


if __name__ == '__main__':
    main()
