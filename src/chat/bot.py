from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters, Application,
)

from chatapp import settings


class TelegramBot:
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Hello from Django 👋")

    async def echo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(update.message.text)

    def build_application(self) -> Application:
        app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.echo))

        return app
