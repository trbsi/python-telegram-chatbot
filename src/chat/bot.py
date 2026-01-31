import bugsnag
from telegram import Update, Bot
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters, Application,
)

from chatapp import settings
from src.chat.tasks import auto_reply_task


class TelegramBot:
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            chat_id = update.effective_chat.id
            bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
            await bot.send_message(chat_id=chat_id, text='Hello fucker. What are you doing? Stroking your nice cock?');
        except Exception as e:
            bugsnag.notify(e)

    async def send(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            chat_id = update.effective_chat.id
            user_id = update.effective_user.id
            text = update.message.text
            auto_reply_task.delay(text, chat_id, user_id)
        except Exception as e:
            bugsnag.notify(e)

    def build_application(self) -> Application:
        app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.send))

        return app
