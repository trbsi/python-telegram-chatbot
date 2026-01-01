from telegram import Bot

from chatapp import settings


class AutoReplyService:
    def reply_now(self, message: str, chat_id: int) -> None:
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        bot.send_message(chat_id=chat_id, text=message)
