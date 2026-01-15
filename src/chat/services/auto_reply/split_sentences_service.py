import re


class SplitSentencesService():
    def split_sentences(self, sentence: str) -> list:
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