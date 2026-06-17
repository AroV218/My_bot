from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes, ConversationHandler

BOT_TOKEN = "8803040130:AAE-NUubcIXyWsjBcne_ZmgTFPMRO0ASpiw"
ADMIN_ID = 1547432883

WAITING_QUESTION = 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["📩 Отправить вопрос"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "👋 Привет!\n\n"
        "Здесь ты можешь задать анонимный вопрос.\n\n"
        "👇 Нажми кнопку внизу экрана — «📩 Отправить вопрос»\n"
        "✅ Потом напиши свой вопрос\n\n"
        "⚠️ Не пиши вопрос сразу — сначала нажми кнопку!",
        reply_markup=reply_markup
    )

async def ask_question_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Напиши свой вопрос:")
    return WAITING_QUESTION

async def receive_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Анонимный вопрос:\n\n{text}"
    )
    await update.message.reply_text("Спасибо! Ваш вопрос отправлен ✅")
    return ConversationHandler.END

app = ApplicationBuilder().token(BOT_TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^📩 Отправить вопрос$"), ask_question_button)],
    states={WAITING_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_question)]},
    fallbacks=[]
)

app.add_handler(CommandHandler("start", start))
app.add_handler(conv_handler)
app.run_polling()
