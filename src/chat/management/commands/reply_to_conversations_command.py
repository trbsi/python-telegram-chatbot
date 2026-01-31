from django.db.models import QuerySet

from src.core.management.commands.base_command import BaseCommand
from src.inbox.models import Conversation


class Command(BaseCommand):
    help = 'Find conversations which require chatbot to reply and reply to them'

    def handle(self, *args, **options):
        conversations: QuerySet[Conversation] = Conversation.objects.filter(system_message_type__isnull=False)

        for conversation in conversations:
            pass
