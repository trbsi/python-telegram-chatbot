from telegram import Bot

from chatapp import settings
from src.core.management.commands.base_command import BaseCommand


class Command(BaseCommand):
    help = 'Set webhook command'

    def add_arguments(self, parser):
        parser.add_argument("url", type=str, nargs='?', default=None)

    def handle(self, *args, **options):
        url = options['url']
        if url is None:
            url = f"{settings.APP_URL}/chat/webhook"
            
        bot = Bot(settings.TELEGRAM_BOT_TOKEN)
        bot.set_webhook(url)
        self.info(f'Webhook set successfully to {url}')
