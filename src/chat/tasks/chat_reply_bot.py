import bugsnag
from celery import shared_task
from telegram import Update
from telegram.ext import (
    ContextTypes,
)

from src.chat.services.auto_reply.auto_reply_service import AutoReplyService


@shared_task
def auto_reply(message: str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        service = AutoReplyService()
        service.reply_now(message, update, context)
    except Exception as e:
        bugsnag.notify(e)
