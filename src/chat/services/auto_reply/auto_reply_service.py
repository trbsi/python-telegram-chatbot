import asyncio
import random

import bugsnag
from telegram import Bot

from chatapp import settings
from src.chat.models import SystemMessage
from src.chat.services.auto_reply.llm_reply import LlmReplyService
from src.chat.services.auto_reply.split_sentences_service import SplitSentencesService
from src.gpu.models import GpuInstance
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
            is_system_message = False
            admin = User.get_admin()
            sender = self._create_or_get_sender(user_id)
            conversation: Conversation = self.create_conversation_service.create_conversation(sender, admin, chat_id)
            self.send_message_service.send_message(sender, conversation, message)  # sender sent a message

            gpu_instance = GpuInstance.objects.filter(status=GpuInstance.STATUS_RUNNING).first()
            if gpu_instance:
                try:
                    sentence = self.llm_service.get_remote_reply(gpu_instance, conversation)
                except Exception as e:
                    bugsnag.notify(e)
                    is_system_message = True
                    sentence = self._get_system_message_and_update_conversation(
                        SystemMessage.TYPE_GPU_NOT_AVAILABLE,
                        conversation
                    )
            elif settings.IS_LOCAL_AI_ENABLED:
                sentence = self.llm_service.get_local_reply(conversation)
            else:
                is_system_message = True
                GpuInstance.objects.create(
                    instance_id=0,
                    ip_address='0',
                    port=0,
                    status=GpuInstance.STATUS_CREATE_NEW
                )
                sentence = self._get_system_message_and_update_conversation(
                    SystemMessage.TYPE_GPU_CREATING,
                    conversation
                )

            self._prepare_and_send_messages(sentence, chat_id, admin, conversation, is_system_message)
        except Exception as e:
            bugsnag.notify(e)

    def _prepare_and_send_messages(
            self,
            sentence: str,
            chat_id: int,
            admin: User,
            conversation: Conversation,
            is_system_message: bool
    ):
        sentences = self.split_sentences_service.split_sentences(sentence)
        number_of_sentences = random.randint(1, min(3, len(sentences)))

        if not is_system_message:
            for i in range(number_of_sentences):
                # admin sent a message
                self.send_message_service.send_message(
                    sender=admin,
                    conversation=conversation,
                    message_content=sentences[i]
                )

        asyncio.run(self._send(sentences, chat_id, number_of_sentences))

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

    def _get_system_message_and_update_conversation(self, type: str, conversation: Conversation) -> str:
        sentence: SystemMessage = SystemMessage.objects.filter(message_type=type).order_by('?').first()

        conversation.system_message_type = type
        conversation.save()

        return sentence.message
