import asyncio
import random

import bugsnag
from telegram import Bot

from chatapp import settings
from src.chat.services.auto_reply.llm_reply import LlmReplyService
from src.chat.services.auto_reply.split_sentences_service import SplitSentencesService
from src.inbox.models import Conversation
from src.inbox.services.create_conversation.create_conversation_service import CreateConversationService
from src.inbox.services.send_message.send_message_service import SendMessageService
from src.user.models import User
from src.user.services.create_user.create_user_service import CreateUserService


class AutoReplyService:
    def __init__(self):
        self.llm_service = LlmReplyService()
        self.create_conversation_service = CreateConversationService()
        self.send_message_service = SendMessageService()
        self.split_sentences_service = SplitSentencesService()

    def reply_now(self, message: str, chat_id: int, user_id: int) -> None:
        try:
            admin = User.get_admin()
            sender = self._create_or_get_sender(user_id)
            conversation: Conversation = self.create_conversation_service.create_conversation(
                sender=sender,
                recipient=admin
            )
            self.send_message_service.send_message(
                sender=sender,
                conversation=conversation,
                message_content=message
            )

            if settings.AI_API_URL:
                sentence = self.llm_service.get_remote_reply(conversation)
            elif settings.IS_AI_ENABLED:
                sentence = self.llm_service.get_local_reply(conversation)
            else:
                sentence = "I want you so bad. mmm this is Hot. Like it, do you? I'm super good"

            sentences = self.split_sentences_service.split_sentences(sentence)
            number_of_sentences = random.randint(1, min(3, len(sentences)))
            for i in range(number_of_sentences):
                self.send_message_service.send_message(
                    sender=sender,
                    conversation=conversation,
                    message_content=sentences[i]
                )
            asyncio.run(self._send(sentences, chat_id, number_of_sentences))
        except Exception as e:
            bugsnag.notify(e)

    async def _send(self, sentences: list, chat_id: int, number_of_sentences: int) -> None:
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        for i in range(number_of_sentences):
            await asyncio.sleep(random.randint(1, 5))
            await bot.send_message(chat_id=chat_id, text=sentences[i])

    def _create_or_get_sender(self, user_id: int) -> User:
        sender = User.objects.filter(username=user_id).first()
        if not sender:
            sender = CreateUserService.create_random_user(user_id)

        return sender
