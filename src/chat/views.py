import json

from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update

from src.chat.bot import TelegramBot

bot = TelegramBot()
app = bot.build_application()


@csrf_exempt
async def webhook(request: HttpRequest) -> JsonResponse:
    data = json.loads(request.body.decode('utf-8'))
    update = Update.de_json(data, app.bot_data)
    await app.process_update(update)
    return JsonResponse({"ok": True})
