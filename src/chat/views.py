import asyncio
import json

from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update, Bot

from chatapp import settings
from src.chat.bot import TelegramBot

bot = TelegramBot()
app = bot.build_application()
_init_lock = asyncio.Lock()


@csrf_exempt
async def webhook(request: HttpRequest) -> JsonResponse:
    async with _init_lock:
        if not app._initialized:
            await app.initialize()

    data = json.loads(request.body.decode('utf-8'))
    update = Update.de_json(data, app.bot)
    await app.process_update(update)
    return JsonResponse({"ok": True})


async def set_webhook(request: HttpRequest) -> JsonResponse:
    get = request.GET
    secret = get.get('secret')
    url = get.get('url')

    if secret != 'temp_secret':
        return JsonResponse({"ok": False})

    if url is None:
        url = f"{settings.APP_URL}/chat/webhook"

    bot = Bot(settings.TELEGRAM_BOT_TOKEN)
    await bot.set_webhook(url)
    return JsonResponse({"ok": True, 'url': url})
