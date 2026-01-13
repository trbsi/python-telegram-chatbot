import asyncio
import random
import time

import bugsnag
from telegram import Bot
import re
from chatapp import settings


class AutoReplyService:
    def reply_now(self, message: str, chat_id: int) -> None:
        try:
            bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

            sentence = 'I want you so bad. mmm this is Hot. I like it, do you?'
            sentences = self._split_sentences(sentence)
            number_of_sentences = random.randint(1, 2)

            async def _send():
                for i in range(number_of_sentences):
                    await asyncio.sleep(random.randint(1, 3))
                    await bot.send_message(chat_id=chat_id, text=sentences[i])

            asyncio.run(_send())
        except Exception as e:
            bugsnag.notify(e)

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
