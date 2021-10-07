import re

from parsers.word_relation_marker import WordRelationMarker


class Tokenizer:
    def __init__(self):
        self.marker = WordRelationMarker()
        self.text = ""
        self.tokens = []

    def tokenize(self, text: str):
        self.text = self.marker.mark(text)
        self.tokens = self.split()
        self.trimTokens()

        return self.tokens

    def trimTokens(self):
        self.tokens = [token.strip() for token in self.tokens]

    def split(self):
        return re.split(r"\[|\]", self.text)
