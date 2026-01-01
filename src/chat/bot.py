import bugsnag
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters, Application,
)

from chatapp import settings
from src.chat.tasks import auto_reply


class TelegramBot:
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            chat_id = update.effective_chat.id
            auto_reply.delay('Hello', chat_id)
        except Exception as e:
            bugsnag.notify(e)

    async def echo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            chat_id = update.effective_chat.id
            text = update.message.text
            auto_reply.delay(text, chat_id)
        except Exception as e:
            bugsnag.notify(e)

    def build_application(self) -> Application:
        app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.echo))

        return app
