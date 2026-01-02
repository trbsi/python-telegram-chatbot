import asyncio

import bugsnag
from telegram import Bot

from chatapp import settings


class AutoReplyService:
    def reply_now(self, message: str, chat_id: int) -> None:
        try:
            bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

            async def _send():
                await bot.send_message(chat_id=chat_id, text=message)

            asyncio.run(_send())
        except Exception as e:
            bugsnag.notify(e)
