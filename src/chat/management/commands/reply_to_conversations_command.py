import asyncio

from django.db.models import QuerySet
from telegram import Bot

from chatapp import settings
from src.chat.models import SystemMessage
from src.core.management.commands.base_command import BaseCommand
from src.gpu.models import GpuInstance
from src.inbox.models import Conversation


class Command(BaseCommand):
    help = 'Find conversations which require chatbot to reply and reply to them'

    def handle(self, *args, **options):
        conversations: QuerySet[Conversation] = Conversation.objects.filter(system_message_type__isnull=False)
        print('Number of conversations: ', conversations.count())

        gpu_instance = GpuInstance.objects.filter(status=GpuInstance.STATUS_RUNNING).count()

        if gpu_instance == 0:
            print('GPU instance is not running yet')
            return

        for conversation in conversations:
            conversation.system_message_type = None
            conversation.save()

            system_message: SystemMessage = (
                SystemMessage.objects
                .filter(message_type=SystemMessage.TYPE_GPU_CREATED)
                .order_by('?')
                .first()
            )

            asyncio.run(self._send_message(conversation, system_message))

    async def _send_message(self, conversation: Conversation, system_message: SystemMessage):
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        await bot.send_message(
            chat_id=conversation.external_chat_id,
            text=system_message.message
        )
