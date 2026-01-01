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
            auto_reply.delay('Hello', update, context)
        except Exception as e:
            bugsnag.notify(e)

    async def echo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            auto_reply.delay(update.message.text, update, context)
        except Exception as e:
            bugsnag.notify(e)

    def build_application(self) -> Application:
        app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.echo))

        return app
