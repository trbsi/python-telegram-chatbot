from telegram import Update
from telegram.ext import (
    ContextTypes,
)


class AutoReplyService:
    async def reply_now(self, message: str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(message)
