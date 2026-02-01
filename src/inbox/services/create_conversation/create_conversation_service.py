from django.db.models import Q

from src.inbox.models import Conversation
from src.user.models import User


class CreateConversationService:
    def create_conversation(self, sender: User, recipient: User, external_chat_id: int) -> Conversation:
        conversation = (
            Conversation.objects
            .filter(Q(sender=sender, recipient=recipient) | Q(sender=recipient, recipient=sender))
            .first()
        )

        if conversation:
            conversation.deleted_by_sender = False
            conversation.deleted_by_recipient = False
            conversation.external_chat_id = external_chat_id
        else:
            conversation = Conversation.objects.create(
                sender=sender,
                recipient=recipient,
                external_chat_id=external_chat_id
            )

        if sender == conversation.sender:
            conversation.read_by_recipient = False
        else:
            conversation.read_by_sender = False

        conversation.save()
        return conversation
