import asyncio
import random
import re

import bugsnag
from telegram import Bot

from chatapp import settings
from src.chat.services.auto_reply.llm_reply import LlmReplyService
from src.chat.services.auto_reply.prepare_messages_service import PrepareMessagesService
from src.inbox.models import Conversation
from src.inbox.services.create_conversation.create_conversation_service import CreateConversationService
from src.inbox.services.send_message.send_message_service import SendMessageService
from src.user.models import User
from src.user.services.create_user.create_user_service import CreateUserService


class AutoReplyService:
    def __init__(self):
        self.llm_service = LlmReplyService()
        self.create_conversation_service = CreateConversationService()
        self.prepare_messages_service = PrepareMessagesService()
        self.send_message_service = SendMessageService()

    def reply_now(self, message: str, chat_id: int, user_id: int) -> None:
        try:
            sender = self._create_or_get_sender(user_id)
            conversation: Conversation = self.create_conversation_service.create_conversation(
                sender=sender,
                recipient=User.get_admin()
            )
            chat_history = self.prepare_messages_service.get_chat_history(conversation)
            self.send_message_service.send_message(
                sender=sender,
                conversation=conversation,
                message_content=message
            )

            if settings.IS_AI_ENABLED:
                sentence = self.llm_service.get_reply(chat_history)
            else:
                sentence = "I want you so bad. mmm this is Hot. I like it, do you? I'm super good"
            sentences = self._split_sentences(sentence)
            number_of_sentences = random.randint(1, 3)

            bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

            async def _send():
                for i in range(number_of_sentences):
                    await asyncio.sleep(random.randint(1, 5))
                    await bot.send_message(chat_id=chat_id, text=sentences[i])

            asyncio.run(_send())
        except Exception as e:
            bugsnag.notify(e)

    def _create_or_get_sender(self, user_id: int) -> User:
        sender = User.objects.filter(username=user_id).first()
        if not sender:
            sender = CreateUserService.create_random_user(user_id)

        return sender

    def _split_sentences(self, sentence: str) -> list:
        sentences = re.split(r'(?<=[.!?])\s+', sentence)
        protected_word = {'i'}
        startswith = {"i'"}

        for index, sentence in enumerate(sentences):
            if sentence.endswith('.'):
                sentence = sentence.removesuffix('.')

            sentence_split = sentence.lower().split()
            for i, word in enumerate(sentence_split):
                if word in protected_word:
                    sentence_split[i] = word.capitalize()

                for start in startswith:
                    if word.startswith(start):
                        sentence_split[i] = word.capitalize()

            sentence = " ".join(sentence_split)
            sentences[index] = sentence

        return sentences
