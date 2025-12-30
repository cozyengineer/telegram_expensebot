import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import sqlite3
from currency import convert_to_sgd
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send the expense amount (default currency: SGD)")

async def amount_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data["amount"] = float(update.message.text)
        keyboard = [
            [InlineKeyboardButton("Food & Drink", callback_data="Food & Drink")],
            [InlineKeyboardButton("Leisure", callback_data="Leisure")],
            [InlineKeyboardButton("Transport", callback_data="Transport")],
            [InlineKeyboardButton("Necessities", callback_data="Necessities")],
            [InlineKeyboardButton("Shopping", callback_data="Shopping")],
            [InlineKeyboardButton("Subscription", callback_data="Subscription")],
            [InlineKeyboardButton("Other", callback_data="Other")]
        ]
        await update.message.reply_text("Select category:", reply_markup=InlineKeyboardMarkup(keyboard))
    except:
        await update.message.reply_text("Please enter a number.")

async def category_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    context.user_data["category"] = query.data
    await query.answer()
    await query.message.reply_text("Add remark or type 'skip'")

async def remark_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    remark = "" if update.message.text.lower() == "skip" else update.message.text
    amount = context.user_data["amount"]
    amount_sgd = convert_to_sgd(amount, "SGD")

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO expenses (amount, currency, amount_sgd, category, remark, date)
    VALUES (?, ?, ?, ?, ?, date('now'))
    """, (amount, "SGD", amount_sgd, context.user_data["category"], remark))
    conn.commit()
    conn.close()

    await update.message.reply_text("Expense saved.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(category_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, amount_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, remark_handler))
app.run_polling()
