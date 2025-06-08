mport logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler,
    filters, ContextTypes
)

# Настройка логгирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Чтение разрешённых пользователей
def load_allowed_users(filename='allowed_users.txt'):
    try:
        with open(filename, 'r') as f:
            return set(int(line.split('#')[0].strip()) for line in f if line.strip())
    except Exception as e:
        logging.error(f"Ошибка при чтении allowed_users.txt: {e}")
        return set()

allowed_users = load_allowed_users()
admin_id = next(iter(allowed_users), None)

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in allowed_users:
        await context.bot.send_message(
            chat_id=admin_id,
            text=f"Запрос на доступ от пользователя: {user_id} (@{update.effective_user.username})"
        )
        await update.message.reply_text("⏳ Ожидается подтверждение администратора...")
        return

    keyboard = [
        [InlineKeyboardButton("📘 Тест Дана", callback_data='dana')],
        [InlineKeyboardButton("📙 Тест Шынтасов", callback_data='shyntasov')]
    ]
    await update.message.reply_text("Выбери тест:", reply_markup=InlineKeyboardMarkup(keyboard))

# Заглушка для обработки теста
async def handle_quiz_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    quiz_name = query.data
    await query.edit_message_text(f"📋 Выбран тест: {quiz_name}\n(Тестирование начнётся здесь...)")

# Обработка текстовых сообщений
async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Пожалуйста, нажмите /start и выберите тест.")

# Запуск бота
if __name__ == '__main__':
    import os
    TOKEN = os.getenv("BOT_TOKEN", "7921542577:AAHq0tDhUeqs3aDJsmgNAdT613b4YLyMnpY")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_quiz_selection))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_message))

    print("Бот запущен...")
    app.run_polling()
