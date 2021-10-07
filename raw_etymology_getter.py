from data_structures import RawEtymology
from wiktionaryparser import WiktionaryParser


class RawEtymologyGetter:
    def __init__(self):
        self.source = "wiktionary"

    @staticmethod
    def get(word: str, language: str) -> RawEtymology:
        parser = WiktionaryParser()
        content = parser.fetch(word, language)
        if not content:
            return RawEtymology(word=word, lang=language, text='')

        return RawEtymology(word=word, lang=language, text=content[0]['etymology'])

